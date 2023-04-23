# -*- coding: utf-8 -*-
"""Lexical_text_simplication.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17Pn_lXaosWRpnYXSEGJjIUdqKxzdHwNl
"""



import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
import pandas as pd
import numpy as np
import string
from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
import torch
import numpy as np
import tensorflow as tf
from transformers import BertTokenizer, TFBertForMaskedLM
from wordfreq import zipf_frequency
from sklearn.metrics.pairwise import cosine_similarity
import textstat
import gensim.downloader as api
from sentence_transformers import SentenceTransformer

tokenizer = BertTokenizer.from_pretrained('bert-large-uncased')
model = TFBertForMaskedLM.from_pretrained('bert-large-uncased')
bert_similarity_model = SentenceTransformer('bert-base-nli-mean-tokens')
synonym_model = api.load("glove-wiki-gigaword-50")

import string
import itertools
from nltk.corpus import wordnet
import gensim.downloader as api
def sentence_complexity(sentence):
    wpt = WordPunctTokenizer()
    tokens = wpt.tokenize(sentence)
    complexity_sum = 0
    num_tokens = len(tokens)
    for i in range(num_tokens):
      complexity_sum+= zipf_frequency(tokens[i], 'en')
    return complexity_sum
def user_interface_function(text):
  def get_top_k_predictions(input_string, k,tokenizer,model) -> str:
    tokenized_inputs = tokenizer(input_string, return_tensors="tf")
    outputs = model(tokenized_inputs["input_ids"])
    top_k_indices = tf.math.top_k(outputs.logits, 7).indices[0].numpy()
    decoded_output = tokenizer.batch_decode(top_k_indices)
    mask_token = tokenizer.encode(tokenizer.mask_token)[1:-1]
    mask_index = np.where(tokenized_inputs['input_ids'].numpy()[0]==mask_token)[0][0]

    decoded_output_words = decoded_output[mask_index]
    return decoded_output_words    
  def get_synonym(word):
    if(word not in synonym_model.key_to_index):
      return word
    max_zip_frequency = 0
    synonym_index = 0
    synonym_list = synonym_model.most_similar(word, topn=10)
    synonyms = [synonym[0] for synonym in synonym_list]
    synonyms_similarity_measure = [synonym[1] for synonym in synonym_list]
    remove_words_list = []
    for i in range(len(synonyms)):
      if(zipf_frequency(synonyms[i], 'en') < zipf_frequency(word, 'en')):
        remove_words_list.append(i)
    remove_words_list.sort(reverse=True)
    for i in range(len(remove_words_list)):
          synonyms.pop(remove_words_list[i])
          synonyms_similarity_measure.pop(remove_words_list[i])
    if(len(synonyms) == 0):
      return word

    print("synonyms")
    print(synonyms)
    zipf_frequency_arr = []
    for i in range(len(synonyms)):
      zipf_frequency_arr.append(zipf_frequency(synonyms[i], 'en'))

    indexed_synonyms_similarity_measure = list(enumerate(synonyms_similarity_measure))
    sorted_sim_arr = sorted(indexed_synonyms_similarity_measure, key=lambda x: x[1],reverse = True)
    indexed_zipf_frequency = list(enumerate(zipf_frequency_arr))
    sorted_complex_arr = sorted(indexed_zipf_frequency, key=lambda x: x[1],reverse = True)
    mydict_sim = {}
    mydict_complex = {}
    for i in range(len(sorted_complex_arr)):
      mydict_sim[sorted_sim_arr[i][0]] = i + 1
      mydict_complex[sorted_complex_arr[i][0]] = i + 1
    min_rank = 100000000000000000
    required_index = 0
    print(mydict_sim)
    print(mydict_complex)
    for i in range(len(sorted_sim_arr)):
      rank_val = mydict_sim[i] * mydict_complex[i]
      print("{} {}".format(rank_val,synonyms[i]))
      if(min_rank > rank_val):
        min_rank = rank_val
        required_index = i
      if(min_rank == rank_val and mydict_complex[i] < mydict_sim[i]):
        required_index = i
    return synonyms[required_index]
  text = text.lower()
  wpt = WordPunctTokenizer()
  tokens = wpt.tokenize(text)
  pos_tags = nltk.pos_tag(tokens)
  complex_words = []
  index_of_complex_word = []
  for i in range(len(tokens)):
    if(textstat.difficult_words(tokens[i]) == 1):
      complex_words.append(tokens[i])
      index_of_complex_word.append(i)
  sentence1_transformed = bert_similarity_model.encode(text)
  best_2_word_list = []
  if(len(tokens) < 6):
    simpler_words = []
    new_sentence = text
    for j in range(len(complex_words)):
       new_sentence = new_sentence.replace(complex_words[j],get_synonym(complex_words[j]))
    return new_sentence
  else:
    for j in range(len(complex_words)):
      if(index_of_complex_word[j] != (len(tokens) -1) and pos_tags[index_of_complex_word[j]][1] == "JJ" and pos_tags[index_of_complex_word[j] + 1][1] == "NN"):
        best_2_word_list.append([get_synonym(complex_words[j])])
      else:
        text_with_mask = text.replace(complex_words[j], '[MASK]')
        predictedWords = get_top_k_predictions(text_with_mask,10,tokenizer,model)
        predictedWords = predictedWords.split()
        word = ''
        remove_words_list = []
        for i in range(len(predictedWords)):
          if(zipf_frequency(predictedWords[i], 'en') < zipf_frequency(complex_words[j], 'en')):
            remove_words_list.append(i)
          else:
            for letter in predictedWords[i]:
              if(letter in string.punctuation):
                remove_words_list.append(i)
                break
        remove_words_list.sort(reverse=True)
        for i in range(len(remove_words_list)):
          predictedWords.pop(remove_words_list[i])
        similarity = []
        for i in range(len(predictedWords)):
          if(complex_words[j] == predictedWords[i]):
            similarity.append(0)
          else:
            simpler_text = text.replace(complex_words[j], predictedWords[i])
            sentence2_transformed = bert_similarity_model.encode(simpler_text)
            similarity_val = cosine_similarity([sentence1_transformed],[sentence2_transformed])[0][0]
            similarity.append(similarity_val)
        if(len(similarity) == 0):
          best_2_word_list.append([complex_words[j]])
        else:
          best_word = predictedWords[similarity.index(max(similarity))]
          predictedWords.pop(similarity.index(max(similarity)))
          similarity.pop(similarity.index(max(similarity)))
          if(len(predictedWords) != 0):
            best_word_2 = predictedWords[similarity.index(max(similarity))]
            best_2_word_list.append([best_word,best_word_2])
          else:
            best_2_word_list.append([complex_words[j]])
    similarity_arr = []
    possible_combinations = list(itertools.product(*best_2_word_list))
    possible_combinations_complexity = []
    simpler_text_arr = []
    for i in range(len(possible_combinations)):
      simpler_text = text
      words_complexity = 0
      for j in range(len(complex_words)):
        simpler_text = simpler_text.replace(complex_words[j], possible_combinations[i][j])
        words_complexity += zipf_frequency(possible_combinations[i][j], 'en')
      simpler_text_arr.append(simpler_text)
      possible_combinations_complexity.append(words_complexity)
      sentence2_transformed = bert_similarity_model.encode(simpler_text)
      similarity_val = cosine_similarity([sentence1_transformed],[sentence2_transformed])[0][0]
      similarity_arr.append(similarity_val)
    indexed_similarity_arr = list(enumerate(similarity_arr))
    sorted_sim_arr = sorted(indexed_similarity_arr, key=lambda x: x[1],reverse = True)
    indexed_possible_combinations_complexity = list(enumerate(possible_combinations_complexity))
    sorted_complex_arr = sorted(indexed_possible_combinations_complexity, key=lambda x: x[1],reverse = True)
    mydict_sim = {}
    mydict_complex = {}
    for i in range(len(sorted_sim_arr)):
      mydict_sim[sorted_sim_arr[i][0]] = i + 1
      mydict_complex[sorted_complex_arr[i][0]] = i + 1
    min_rank = 100000000000000000
    required_index = 0
    for i in range(len(sorted_sim_arr)):
      rank_val = mydict_sim[i] * mydict_complex[i]
      if(min_rank > rank_val):
        min_rank = rank_val
        required_index = i
      if(min_rank == rank_val and mydict_complex[i] < mydict_sim[i]):
        required_index = i
    new_sentence = text
    for j in range(len(complex_words)):
        new_sentence = new_sentence.replace(complex_words[j], possible_combinations[required_index][j])
    return new_sentence

input_text = "The door to his dilapidated residence was locked but the police knocked down the door with full force and captured him."
simplified_text = user_interface_function(input_text)

print(simplified_text)
print(sentence_complexity(input_text))
print(sentence_complexity(simplified_text))
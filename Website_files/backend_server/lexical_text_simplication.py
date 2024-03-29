import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
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
from sentence_transformers import SentenceTransformer

# !pip install transformers
# !pip install sentence-transformers
# !pip install wordfreq
# !pip install textstat

tokenizer = BertTokenizer.from_pretrained('bert-large-uncased')
model = TFBertForMaskedLM.from_pretrained('bert-large-uncased')
bert_similarity_model = SentenceTransformer('bert-base-nli-mean-tokens')
def user_interface_function(text):
  def get_top_k_predictions(input_string, k,tokenizer,model) -> str:
    tokenized_inputs = tokenizer(input_string, return_tensors="tf")
    outputs = model(tokenized_inputs["input_ids"])
    top_k_indices = tf.math.top_k(outputs.logits, k).indices[0].numpy()
    decoded_output = tokenizer.batch_decode(top_k_indices)
    mask_token = tokenizer.encode(tokenizer.mask_token)[1:-1]
    mask_index = np.where(tokenized_inputs['input_ids'].numpy()[0]==mask_token)[0][0]

    decoded_output_words = decoded_output[mask_index]
    return decoded_output_words   
  def sentence_complexity(sentence):
    wpt = WordPunctTokenizer()
    tokens = wpt.tokenize(sentence)
    complexity_sum = 0
    num_tokens = len(tokens)
    for i in range(num_tokens):
      complexity_sum+= zipf_frequency(tokens[i], 'en')
    return complexity_sum


  text = text.lower()
  wpt = WordPunctTokenizer()
  tokens = wpt.tokenize(text)
  complex_words = []
  index_of_complex_word = []
  for i in range(len(tokens)):
    if(textstat.difficult_words(tokens[i]) == 1):
      complex_words.append(tokens[i])
      index_of_complex_word.append(i)
  sentence1_transformed = bert_similarity_model.encode(text)
  for j in range(len(complex_words)):
    text_with_mask = text.replace(complex_words[j], '[MASK]')
    predictedWords = get_top_k_predictions(text_with_mask,5,tokenizer,model)
    predictedWords = predictedWords.split()
    word = ''
    similarity = []
    for i in range(len(predictedWords)):
      if(complex_words[j] == predictedWords[i]):
        similarity.append(0)
      simpler_text = text.replace(complex_words[j], predictedWords[i])
      sentence2_transformed = bert_similarity_model.encode(simpler_text)
      similarity_val = cosine_similarity([sentence1_transformed],[sentence2_transformed])[0][0]
      similarity.append(similarity_val)
    if(len(similarity) == 0):
      tokens[index_of_complex_word[j]] = complex_words[j]
    else:
      tokens[index_of_complex_word[j]] = predictedWords[similarity.index(max(similarity))]
  sentence = ""
  for token in tokens:
    sentence += token + " "
  return sentence

#sample use case  
# input_text = "Draconian laws made everybody miserable."
# simplified_text = user_interface_function(input_text)
# print(simplified_text) 
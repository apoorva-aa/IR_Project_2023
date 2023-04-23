from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import numpy as np
import spacy
import math

def paraphrase(context,sentence):

    sentences = []

    model = AutoModelForSeq2SeqLM.from_pretrained("ramsrigouthamg/t5-large-paraphraser-diverse-high-quality")
    tokenizer = AutoTokenizer.from_pretrained("ramsrigouthamg/t5-large-paraphraser-diverse-high-quality")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print ("device ",device)
    model = model.to(device)

    text = "paraphrase: "+ sentence + " "

    encoding = tokenizer.encode_plus(text,max_length =128, padding=True, return_tensors="pt")
    input_ids,attention_mask  = encoding["input_ids"].to(device), encoding["attention_mask"].to(device)
    model.eval()

    diverse_beam_outputs = model.generate(
        input_ids=input_ids,attention_mask=attention_mask,
        max_length=128,
        early_stopping=True,
        num_beams=5,
        num_beam_groups = 5,
        num_return_sequences=5,
        diversity_penalty = 0.70
    )

    for beam_output in diverse_beam_outputs:
        sent = tokenizer.decode(beam_output, skip_special_tokens=True,clean_up_tokenization_spaces=True)
        sentences.append(sent)
    return sentences



nlp = spacy.load('en_core_web_md')

  # function to get the similarity score between two words
def get_similarity(word1, word2):
    # create Doc objects for each word
    doc1 = nlp(word1)
    doc2 = nlp(word2)

    # get similarity score between the two Doc objects
    similarity = doc1.similarity(doc2)

    return similarity


file = open("toxic_words.txt", "r")
toxic_words = file.read()
file.close()

toxic_words_list = toxic_words.split()



file = open("neg_words.txt", "r")
neg_words = file.read()
file.close()

neg_words_list = neg_words.split()
     
def detoxify(sent):

    sent = sent.lower()
    sent_ = sent.split(" ")
    detoxified_sentence = ""
    for index in range(len(sent_)):
        word = sent_[index]
        if word in toxic_words_list:
          # print("toxic word found", word)
          sim = []
          for i in range(len(neg_words_list)):
            syn_word = neg_words_list[i]
            val = get_similarity(syn_word, word)
            sim.append(val)

          similarities = np.array(sim)
          idx = np.argmax(similarities) 
          sent_[index] = neg_words_list[idx]
          
    detoxified_sentence = ' '.join(sent_)
    return detoxified_sentence



def detoxification(toxic_sentence):
  detoxified_sentence = detoxify(toxic_sentence)
  print('detoxified sentence:', detoxified_sentence)
  sentences = paraphrase(toxic_sentence, detoxified_sentence)
  print('final_output_sentences:', sentences)
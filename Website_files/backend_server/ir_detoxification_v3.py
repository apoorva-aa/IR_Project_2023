import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
from nltk.tokenize import WhitespaceTokenizer
from nltk.corpus import stopwords
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('stopwords')
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import torch
from transformers import BertForSequenceClassification, BertTokenizer
from gensim.models import Word2Vec
import pickle


with open('my_list.pkl', 'rb') as f:
    X = pickle.load(f)
f.close()

def classify_toxicity(sent , model_2 ,tokenizer_2):
    # Load the pre-trained BERT model and tokenizer

    # Tokenize the input word
    tokenized = tokenizer_2(sent, padding=True, truncation=True, max_length=128, return_tensors="pt")
    input_ids = tokenized["input_ids"]
    attention_mask = tokenized["attention_mask"]

    # Classify the word
    model_2.eval()
    with torch.no_grad():
        outputs = model_2(input_ids, attention_mask=attention_mask)
        predictions = torch.softmax(outputs.logits, dim=1)
        toxic_score = predictions[0][1].item()

    # Return whether the word is toxic or not
    if toxic_score >= 0.5:
        return 1
    else:
        return 0


def detoxify(sent):

    # First we will check whether the sent is toxic or not using our SVM model

    # if the sent is not toxic then just return the original sentence

    # else
    sent = sent.split(" ")
    detoxified_sentence = ""
    for word in sent:
        model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        # temp_string = word + " is a ball."
        if(classify_toxicity(word,model,tokenizer) == 1):
            # We found a toxic word
            detoxified_sentence += '*'*len(word)
        else:
            detoxified_sentence += word
        detoxified_sentence += " "
    return detoxified_sentence

def main_function(sent):
    model_2 = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
    tokenizer_2 = BertTokenizer.from_pretrained('bert-base-uncased')
    # if(classify_toxicity(sent,model_2,tokenizer_2) == 0):
    #     # The sentence is not toxic so just return the sentence itself
    #     print("returning the sentence itself")
    #     return sent
    # else:
    res = detoxify(sent)
    print("returning "+ res)
    return res


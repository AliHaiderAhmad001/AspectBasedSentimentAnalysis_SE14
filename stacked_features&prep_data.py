# -*- coding: utf-8 -*-
"""stacked_features&prep_data.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1O3rPDECyPSYSrK5H4DpQWjE96MM56AQs
"""

#!pip install transformers
import warnings
warnings.filterwarnings("ignore")
import sys
sys.path.append('/content/drive/MyDrive/Colab Notebooks/AE')
import numpy as np
import json
from bert__features import BERTModelFeatures
from elmo_features import ELMoModelFeatures
from transformers import BertTokenizer, BertModel

def load__data(file_path):
    data,labels,words,tags = [],[],[],[]
    tag2idx={'B-A': 1, 'I-A': 2, 'O': 0}
    fh = open(file_path)
    for line in fh:
        line = line.strip()
        if line=='':
            #Sentence ended.
            if len(tags) <70:
              tags+=[0]*(70-len(tags))
            data.append(words)
            labels.append(tags)
            words,tags = [],[]
        else:
            word, tag = line.split("\t")
            words.append(word)
            tags.append(tag2idx[tag])
    fh.close()
    return data,labels

test_path = '/content/drive/MyDrive/Colab Notebooks/AE/AE_Datasets/Restaurants_Test_Gold_mod.iob'
train_path = '/content/drive/MyDrive/Colab Notebooks/AE/AE_Datasets/Restaurants_Train_v2_mod.iob'

train,train_labels = load__data(train_path)
test,test_labels = load__data(test_path)

out_fn='/content/drive/MyDrive/Colab Notebooks/AE/data/final_indomain_emb.npy'
word_idx_fn='/content/drive/MyDrive/Colab Notebooks/AE/data/worIdx_.json'

training_data_path='/content/drive/MyDrive/Colab Notebooks/AE/data/training_data.npy'
training_labels_path='/content/drive/MyDrive/Colab Notebooks/AE/data/training_labels.npy'
test_data_path='/content/drive/MyDrive/Colab Notebooks/AE/data/test_data.npy'
test_labels_path='/content/drive/MyDrive/Colab Notebooks/AE/data/test_labels.npy'

np.save(training_labels_path,train_labels)
np.save(test_labels_path,test_labels)

with open(word_idx_fn) as f:
    word_idx=json.load(f)
in_domain_emb=np.load(out_fn)
bf=BERTModelFeatures()
ef=ELMoModelFeatures()
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased',do_lower_case=True)
model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states = True)
zero_padding=np.zeros(1892,dtype='float32')

def stacked_emb(data,path):
    all=[]
    for i,sent in enumerate(data):
      sent=" ".join(sent)
      print(i,sent)
      v1=bf.tokenVecSum(sent)['token_vecs_sum']
      v2=ef.elmo_vectors([sent]).numpy()
      if v2.ndim==1:
        v2=v2.reshape(1,-1)
      v3=[]
      for token in sent.split():
        v3.append(in_domain_emb[word_idx[token]])
      v=np.concatenate((v1, v2, np.array(v3)), axis=1)
      if v.shape[0] !=70:
        v=np.concatenate((v,[zero_padding]*(70-v.shape[0])), axis=0)
      all.append(v)
    np.save(path,np.array(all))

stacked_emb(train,training_data_path)
stacked_emb(test,test_data_path)
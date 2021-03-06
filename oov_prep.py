# -*- coding: utf-8 -*-
"""oov_prep.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hKshjZkviSPJ8IpQ1LlhWZBcyBF0aG_R
"""

import json
import numpy as np
from gensim.models import FastText
# paths
word_idx_fn='/content/drive/MyDrive/Colab Notebooks/AE/data/worIdx_.json'
emb_file='/content/drive/MyDrive/Colab Notebooks/AE/data/restaurant_emb.npy'
oov_fn='/content/drive/MyDrive/Colab Notebooks/AE/data/restaurant_emb.oov.txt'
fast_text_model='/content/drive/MyDrive/Colab Notebooks/AE/models/fast-text-model'
out_fn='/content/drive/MyDrive/Colab Notebooks/AE/data/final_indomain_emb.npy'

# oov handling
def fill_np_embedding(emb_file, word_idx_fn, oov_fn,fast_text_model,out_fn):
    model = FastText.load(fast_text_model)
    with open(word_idx_fn) as f:
        word_idx=json.load(f)
    embedding=np.load(emb_file)
    for w in word_idx:
        if embedding[word_idx[w]].sum() == 0.:
          embedding[word_idx[w]]= model.wv[w]
    np.save(out_fn, embedding.astype('float32'))
    
fill_np_embedding(emb_file, word_idx_fn, oov_fn,fast_text_model,out_fn)
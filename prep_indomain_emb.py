# -*- coding: utf-8 -*-
"""prep_indomain_emb.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1g3emMx9ArTUzZP6KTMJ_Dc48a2rEtjfw
"""

# Extract all vocabulary from SE14-restaurants-datasets and form an index for it
import json 
def extract_all_vocabulary(file_path):
    words = []
    fh = open(file_path)
    for line in fh:
        line = line.strip()
        if line=='':
            continue
        else:
            word, _ = line.split()
            words.append(word)
    fh.close()
    return set(words)

train='/content/drive/MyDrive/Colab Notebooks/AE/AE_Datasets/Restaurants_Train_v2_mod.iob'
test='/content/drive/MyDrive/Colab Notebooks/AE/AE_Datasets/Restaurants_Test_Gold_mod.iob'
out_file='/content/drive/MyDrive/Colab Notebooks/AE/data/worIdx_.json'

# all vocab in SE14 dataset
w_train=extract_all_vocabulary(train)
w_test=extract_all_vocabulary(test)
vocab=w_train.union(w_test)  # 5304

# generate worIdx_ file
voca_d=dict(zip(vocab, range(len(vocab))))
with open(out_file, "w") as outfile:
    json.dump(voca_d, outfile)
    
###################################################
import numpy as np
import json

def gen_np_embedding(fn, word_idx_fn, out_fn, dim=100):
    with open(word_idx_fn) as f:
        word_idx = json.load(f)
    embedding = np.zeros((len(word_idx), dim))
    with open(fn) as f:
        for l in f:
            rec = l.rstrip().split(' ')
            if len(rec) == 2:  # skip the first line.
                continue
            if rec[0] in word_idx:
                embedding[word_idx[rec[0]]] = np.array([float(r) for r in rec[1:]])
    ovvCount=0
    with open(out_fn+".oov.txt", "w") as fw:
        for w in word_idx:
            if embedding[word_idx[w]].sum() == 0.:
                ovvCount+=1
                fw.write(w+"\n")
    np.save(out_fn+".npy", embedding.astype('float32'))
    return ovvCount

restaurant_emb_raw='/content/drive/MyDrive/Colab Notebooks/AE/data/restaurant_emb.vec'
word_idx_file='/content/drive/MyDrive/Colab Notebooks/AE/data/worIdx_.json'
restaurant_emb='/content/drive/MyDrive/Colab Notebooks/AE/data/restaurant_emb'

# There are 401 vocab that do not have emb (OOV)
ovvCount=gen_np_embedding(restaurant_emb_raw,word_idx_file,restaurant_emb)
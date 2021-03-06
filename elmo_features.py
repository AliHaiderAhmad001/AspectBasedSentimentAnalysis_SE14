# -*- coding: utf-8 -*-
"""elmo_features.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17NcmC0giMQBiD_l645uc6Bd03gVXvMeH
"""

import tensorflow_hub as hub
import tensorflow as tf
class ELMoModelFeatures():
    def __init__(self):
      self.model = hub.load("https://tfhub.dev/google/elmo/3")
    def elmo_vectors(self,sentence):
      embeddings = self.model.signatures["default"](tf.constant(sentence))["elmo"]
      return  tf.squeeze(embeddings)
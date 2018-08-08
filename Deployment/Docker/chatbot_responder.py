
import pickle
from numpy import array
import numpy as np
import random
import sys
import io
import os
#from keras.utils.data_utils import get_file
from keras.models import load_model
from keras.preprocessing.text import Tokenizer


class chatbot_responder():

    model = False
    words = False
    def __init__(self):
        self.words = self.load_words()
        self.model = load_model('./objects/keras_text_model.h5')


    def load_obj(self,name):
        with open('objects/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)

    def load_words(self):
        word_dict = self.load_obj('word_dictionary')
        ret_obj = [k for k, v in word_dict.items()]
        return ret_obj

    def decode_sequence(self,sequence):
        return [self.words[seq - 1] for seq in sequence]

    def load_tokenizer(self):
        return self.load_obj('word_tokenizer')


    def chatbot_response(self,in_message):
        tnizer = self.load_tokenizer()
        encoded_message = tnizer.texts_to_sequences([in_message])
        encoded_message = array(encoded_message)[0] #only take the first

        #call a model.predict
        pred = self.model.predict_classes(encoded_message,verbose=False)
        #retval = decode_outgoing(words)
        retval = str1 = ' '.join(self.decode_sequence(pred))
        return retval


resp = chatbot_responder()

resp.chatbot_response('Best')

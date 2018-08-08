import pandas as pd
from numpy import array
import numpy as np
import random
import pickle
import sys
import io
import os
import re
import math

from collections import Counter

class chatbot_responder():

    understanding_threshold = .25
    skit_lines = ''

    @classmethod
    def text_to_vector(cls,text):
        WORD = re.compile(r'\w+')
        words = WORD.findall(text)
        return Counter(words)

    @classmethod
    def get_cosine(cls,vec1, vec2):
         intersection = set(vec1.keys()) & set(vec2.keys())
         numerator = sum([vec1[x] * vec2[x] for x in intersection])

         sum1 = sum([vec1[x]**2 for x in vec1.keys()])
         sum2 = sum([vec2[x]**2 for x in vec2.keys()])
         denominator = math.sqrt(sum1) * math.sqrt(sum2)

         if not denominator:
            return 0.0
         else:
            return float(numerator) / denominator

    @classmethod
    def misunderstand_response(cls):
        response_list = [
            'I am not sure what you said. Could you rephrase the question?'
           ,'Many other people have asked that.'
           ,'That is a possibility.'
           ,'What do you mean?'
           ,'Please ask again in a different way.'
           ,'Hmmm, good question'
           ,'Say again, please'
        ]
        i = random.randint(0,len(response_list)-1)
        return response_list[i]

    def __init__(self,verbose=False):
        print('initialized')
        def open_ac():
            #file_name = "/Users/steve/Documents/DSI-US-4/Projects/project-5/baseball_oracle/2018_Official_Baseball_Rules/baseball_rules.txt"
            file_name = "baseball_rules.txt"
            lines = pd.read_csv(file_name,sep='/n'
                            ,engine='python'
                           )
            lines = lines[lines['Rule_Text'].str.len() > 25]
            lines['response'] = lines['Rule_Text']
            return lines

        chatbot_responder.skit_lines = open_ac()

    def get_response_line(self,text,verbose=False):
        search_vector = chatbot_responder.text_to_vector(text)
        df_lines = chatbot_responder.skit_lines
        best_line = ''
        best_response = ''
        closest_statement = ''
        score = 0.0
        best_score = 0.0
        for index,line in df_lines.iterrows():
            score,line_response,statement = chatbot_responder.get_cosine(search_vector,chatbot_responder.text_to_vector(line['Rule_Text'])),line['Rule_Text'],line['Rule_Text']
            if score > best_score:
                best_line = line
                best_score = score
                closest_statement = statement
                best_response = line_response
            if verbose == True:
                print('Input Text:',text)
                print('Eval Text:',line)
                print('Eval Score',score)
                print('Closest statement',closest_statement)
                print('Best Score',best_score)
                print('Best Response',best_response)
                print('-----------------')
        if best_score > chatbot_responder.understanding_threshold:
            return best_response.strip()
        else:
            return chatbot_responder.misunderstand_response()

if __name__ == "__main__":
    w2 = chatbot_responder()
    w2.get_response_line("What do teams change sides?")

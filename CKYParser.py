from collections import defaultdict
from os import PRIO_PGRP, lseek
import numpy as np
from numpy.lib.function_base import append
import pandas as pd
import json

import re

from pandas.core.algorithms import value_counts

class Agreement_Error():
    pass

class CKYParser():

    def __init__(self):
        self.grammar = open("linguistic/grammar",'r', encoding="utf-8").read()
        self.order = 0
        self.morphology = json.loads(open("/home/kara/Documents/Courses/Fall 2021/CMPE561 - NATURAL LANGUAGE PROCESSING/Application Projects/CFGTurkish/linguistic/morphology_map.json","r",encoding="utf-8").read())
        self.lexicon = json.loads(open("/home/kara/Documents/Courses/Fall 2021/CMPE561 - NATURAL LANGUAGE PROCESSING/Application Projects/CFGTurkish/lexicon/lexicon.txt","r",encoding="utf-8").read())

    def parse(self, sentence):
        """
        
        Arguments:

        """

        table = [{id: [] for id in range(1,len(sentence)+1)} for _ in range(len(sentence))]


        sent_dict = [self.extract_features(s) for s in sentence] 

        for j in range(1,len(sentence)+1):

            #print("j=",j)
            
            table[j-1][j].append(sent_dict[j-1])

            for i in range(j-1, -1, -1):

                #print("Table Node:",(i,j))
                
                for k in range(i, j-1):
                        
                    x = table[i][k+1]
                    y = table[k+1][j]
                    
                    #print((i,k+1), (k+1,j))
                    
                    for prev in x:
                        for forw in y:
                            constituent = self.create_constituent(prev,forw)
                            if constituent == Agreement_Error:
                                return Agreement_Error
                            else:
                                table[i][j].extend(constituent)
                             

        def simplfy(x):
            if x:
                return set(x[0]["POS"])

        return pd.DataFrame(table).rename(columns={id: word for id, word in enumerate(sentence,start=1)}).applymap(simplfy)

    def check_grammar(self,x,y):
        """
        Check whether two constituents create an another constituent

        Arguments:
            - x: former constituent
            - y: latter constituent
        """
        if re.findall(f"^(.+?) -> {x} {y}$", self.grammar, flags=re.MULTILINE):
            #print(f"^(.+?) -> {x} {y}$", "Results: ", re.findall(f"^(.+?) -> {x} {y}$", self.grammar, flags=re.MULTILINE))
            pass
        return re.findall(f"^(.+?) -> {x} {y}$", self.grammar, flags=re.MULTILINE)


    def inflect(self, x):
        try:
            #print(x)
            if x["Case"]:
                x["POS"] += "."+x["Case"]

            elif x["Tense"]:
                pass    
        except:
            pass

        return x

    def extract_features(self,token,order=0):
        """
        Arguments:
        - self: class
        - Token: str
        
        Output:
        - Set of Linguistic Features
            - POS: Possible Part-of-Speech Tags --type: list
            - Case, Number, Person..: Predefined at the morphology map  --type: str

        {
            Token: -str
            POS:  -list
            CASE: -str (Nom, Acc, Dat, Loc, Abl, Ins, Bare)
            Number: 
            Person: which
            Poss: possessee agreement (ben-Hm kitab-Hm) -> 1sg

            NP.1sg 
        }
        """
        
        token_dict = defaultdict(str)
        
        lemma = token.split('+')[0].lower()
    
        token_dict["Token"] = token
        token_dict["POS"] = self.lexicon[lemma]

        for morph in token.split('+')[1:]:

            feat_type, feat = self.morphology[morph]
            token_dict[feat_type] = feat

        if "NP" in token_dict["POS"]:

            if token_dict["Case"] == "":
                if self.order == 0:
                    token_dict["Case"] = "Nom"
                else:
                    token_dict["Case"] = "Bare"

            token_dict["POS"].append("NP."+token_dict["Case"])
        
        if "ADJP" in token_dict["POS"]:
            if token_dict["Tense"]:
                token_dict["POS"].append("ADJ.Pred")

        self.order += 1
        
        return token_dict

    def check_agreement(self,x,y):
        """""
        Check for: 
            - Subject Verb Agreement (Overtness)
                - Ben arkadaşıma hediye aldın. (Person) 
                - Tarihi bir romanlar okudum. (Number) (DET.Sing NOUN.Pl)
                - Dün babama yardım edeceğim. (Tense) (ADV.Pass VERB.Fut)
            - Verb Argument Structure Agreement
                - Ben okul gittim. (Noun Incorporation) --> Cannot be separated Argument Structure??
                - Ben okulda gittim. (Lexical Case) VP --> NP.Dat git / PP --> NP.Dat sonra /....
                - Ben kitap ok-un-du. (Number of Arguments) VP.Pass --> NP.Nom V.Pass!!
                
        """""

        for x_phrase in self.get_constituents(x):
            for y_phrase in y:
                
                print(x_phrase["POS"],y_phrase["POS"])

                if "NP.Nom" in x_phrase["POS"] and "VP" in y_phrase["POS"]:
                    if x_phrase["Person"] != y_phrase["Person"]:
                        return None
                    if "Pass" in y_phrase["Mod"]:
                        return None

                if ("Det" in x_phrase["POS"] and "bir" in x_phrase["Token"]) and "Noun" in y_phrase["POS"]:
                    if x_phrase["Number"] != y_phrase["Number"]: 
                        return None
                
                if "ADV.Temp" in x_phrase["POS"] and "V" in y_phrase["POS"]:
                    if x_phrase["Tense"] != y_phrase["Tense"]:
                        return None

        # Arg structure

        # Lexical Case
        return True

    def create_constituent(self,x,y):
        """"
        Creates new constituents for the given sentence
        - i: x
        - i: y
        """

        constituents = []

        try:
            x["POS"]
            y["POS"]
        except:
            return constituents

        constituents = {
                        "POS": [],
                        "Token": " ".join([x["Token"],y["Token"]]),
                        "Constituents": [x,y],
                        }

        for x_pos in x["POS"]:
            for y_pos in y["POS"]:
                if self.check_grammar(x_pos,y_pos): 
                    #if self.check_agreement(x,y):
                    constituents["POS"].extend(self.check_grammar(x_pos,y_pos))
                    # else:
                        # return Agreement_Error
        
        if constituents["POS"]:
            #print(constituents)
            return [constituents]
        else:
            return []

    def get_constituents(self,x):
        if type(x) == defaultdict:
            return [con for con in x["Constituents"]]
        else:
            return [x]

    def CFG_to_CNF(self):
        """
        Convert terminals to dummy non-terminals (Case 1)
            Replace each terminal with a new non-terminal and create a new rule
            Do this for all terminals in the rule one by one
        Convert unit productions (Case 2)
            Replace the RHS non-terminal to each non-unit production or terminal symbol
            Create a rule for each
        Make the rule binary (Case 3)
            If the RHS is longer than 2, decrease the length by one iteratively
            Create a new rule at each iteration
        """

        x = 0

        for rule, phrase in self.grammar.items():

            nodes = rule.split()

            # X -> to VP  "to VP": X
            # X -> TO VP  "TO VP": X
            # TO -> to    "to": "TO"     
            for idx, node in enumerate(nodes):
                if node.islower():
                    self.grammar.pop(rule)
                    nodes[idx] = node.upper()
                    self.grammar[node] = node.upper()


            # S -> VP "VP": S
            # VP -> X  "X": "VP"
            # X -> V NP "V NP": X
            if len(nodes) == 1:
                for a,b in self.grammar.items():
                    if b == nodes[0]:
                        self.grammar[a] = phrase
                    

            # S -> A B C
            # S -> A X1
            # X1 -> B C
            if len(nodes) > 2:
                while len(nodes) > 2:
                    self.grammar[" ".join(nodes[-2:])] = f"X{x}"
                    nodes = nodes[:-2]
                    self.grammar[" ".join(nodes.append(f"X{x}"))] = phrase
                    x += 1
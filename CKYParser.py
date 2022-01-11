from collections import defaultdict
import numpy as np
import pandas as pd
import json

import re

class Agreement_Error():
    pass

class CKYParser():

    def __init__(self):
        self.grammar = open("linguistic/grammar",'r', encoding="utf-8").read()
        self.CFG_to_CNF()
        self.order = 0
        self.morphology = json.loads(open("linguistic/morphology_map.json","r",encoding="utf-8").read())
        self.lexicon = json.loads(open("lexicon/lexicon.txt","r",encoding="utf-8").read())
        self.propbank = json.loads(open("linguistic/propbank.txt","r",encoding="utf-8").read())
        self.adverbs = json.loads(open("lexicon/open_category/adverbial.txt","r",encoding="utf-8").read())

    def parse(self, sentence):
        """
        
        Arguments:

        """

        table = [{id: [] for id in range(1,len(sentence)+1)} for _ in range(len(sentence))]


        sent_dict = [self.extract_features(s) for s in sentence]
        self.order = 0

        for j in range(1,len(sentence)+1):
            
            table[j-1][j].append(sent_dict[j-1])

            for i in range(j-1, -1, -1):

                for k in range(i, j-1):
                        
                    x = table[i][k+1] 
                    y = table[k+1][j]
                                       
                    for prev in x:
                        for forw in y:
                            constituent = self.create_constituent(prev,forw)
                            if type(constituent) == Agreement_Error:
                                return constituent
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
        return re.findall(f"^(.+?) -> {x} {y}$", self.grammar, flags=re.MULTILINE)

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
        
        token_dict = {}
        
        lemma = token.split('+')[0].lower()
    
        token_dict["Token"] = token
        token_dict["POS"] = self.lexicon[lemma]

        for morph in token.split('+')[1:]:

            feat_type, feat = self.morphology[morph]
            token_dict[feat_type] = feat

        for pos in token_dict["POS"]:
            phrase = re.findall(f"^(.+?) -> {pos}$", self.grammar, flags=re.MULTILINE)
            if phrase:
                token_dict["POS"].extend(phrase)

        if "NP" in token_dict["POS"]:

            if not ("Case" in token_dict.keys()):
                if self.order == 0:
                    token_dict["Case"] = "Nom"
                else:
                    token_dict["Case"] = "Bare"
            
            if ("Poss" in token_dict.keys()):
                token_dict["POS"] = [p+".Poss" if p.startswith("NP") else p for p in token_dict["POS"]]

            token_dict["POS"] = [p+"."+token_dict["Case"] if p.startswith("NP") else p for p in token_dict["POS"]]
                        
            pronouns = {"ben": "1Sg",
                        "sen": "2Sg",
                        "o": "3Sg",
                        "biz": "1Pl",
                        "siz": "2Pl",
                        "onlar": "3Pl"}

            if lemma in pronouns.keys():
                token_dict["Person"] = pronouns[lemma]
            
            if not ("Person" in token_dict.keys()):
                token_dict["Person"] = "3sg" 

            if not ("Number" in token_dict.keys()):
                    token_dict["Number"] = "Sg"

            
        if "Verb" in token_dict["POS"]:
            if not ("Person" in token_dict.keys()):
                token_dict["Person"] = "3sg"

            if not ("Voice" in token_dict.keys()):
                token_dict["Voice"] = "Active"

        if "Det" in token_dict["POS"]:
            if "bir" == lemma:
                token_dict["Number"] = "Sg"                

        if "ADJ" in token_dict["POS"]:
            if "Tense" in token_dict.keys():
                token_dict["POS"].append("ADJ.Pred")

        if "Date" in token_dict["POS"]:
            if lemma in self.adverbs.keys():
                token_dict["Tense"] = self.adverbs[lemma] 

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
            for y_phrase in self.get_constituents(y):

                if "Noun" in x_phrase["POS"] and "Verb" in y_phrase["POS"]:
                    if self.propbank[y_phrase["Token"].split("+")[0]]:
                        
                        if not (x_phrase["Case"] in self.propbank[y_phrase["Token"].split("+")[0]]):
                            print("Argument Error")
                            return False

                if "NP.Nom" in x_phrase["POS"] and "VP" in y_phrase["POS"]:
                    
                    if x_phrase["Person"] != y_phrase["Person"]:
                        print("Subject-Verb Agreement Error")
                        return False
                    
                    if y_phrase["Voice"] == "Pass":
                        print("Passive Arg Error")
                        return False

                if ("Det" in x_phrase["POS"] and "bir" in x_phrase["Token"]) and "Noun" in y_phrase["POS"]:
                    if x_phrase["Number"] != y_phrase["Number"]: 
                        print("Number Agreement Error")
                        return False
                
                if "Date" in x_phrase["POS"] and "Verb" in y_phrase["POS"]:
                    if x_phrase["Tense"] != y_phrase["Tense"]:
                        print("Tense Agreement Error")
                        return False
                
        return True

    def create_constituent(self,x,y):
        """"
        Creates new constituents for the given sentence
        - i: x
        - i: y
        """

        constituent = {
                        "POS": [],
                        "Token": " ".join([x["Token"],y["Token"]]),
                        "Constituents": []
                       }

        if "Constituents" in x.keys():
            constituent["Constituents"].extend(x["Constituents"])
        else:
            constituent["Constituents"].append(x)

        if "Constituents" in y.keys():
            constituent["Constituents"].extend(y["Constituents"])
        else:
            constituent["Constituents"].append(y)

        for x_pos in x["POS"]:
            for y_pos in y["POS"]:
                if self.check_grammar(x_pos,y_pos):
                    if self.check_agreement(x,y):
                        constituent["POS"].extend(self.check_grammar(x_pos,y_pos))
                    else:
                        return Agreement_Error()
        
        if constituent["POS"]:
            return [constituent]
        return []

    def get_constituents(self,x):
        if "Constituents" in x.keys():
            return [con for con in x["Constituents"]]
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

        self.grammar += "\n\n#Conversion rules\n" 

        for line in self.grammar.split("\n"):

            REGEX_RULE = r"^([\w\.]+) -> ([\w\.]+)((\s[\w\.]+)*?)$"
            rule = re.findall(REGEX_RULE,line)
            if rule:
                
                phrase = rule[0][0]
                nodes = []
                nodes.extend([c.strip().split() for c in rule[0][1:-1] if c])
                nodes = [item for sublist in nodes for item in sublist]

                # S -> VP "VP": S
                # VP -> X  "X": "VP"
                # X -> V NP "V NP": X
                if len(nodes) == 1:
                    _nodes = re.findall(f"\n{nodes[0]} -> ([\w\.]+)(\s[\w\.]+)*?\n", self.grammar)
      
                    if _nodes:
                        for n_s in _nodes:
                            
                            intermediate = nodes[0]
                            final_nodes = []
                            
                            while not(final_nodes):
                                
                                n_s = [n for n in n_s if n]

                                if len(n_s) >= 1:
                                    final_nodes = n_s

                                else:
                                    intermediate = n_s[0] 
                            
                                self.grammar += f"{phrase} -> {' '.join(final_nodes)}\n"
                        

                # S -> A B C
                # S -> A X1
                # X1 -> B C
                if len(nodes) > 2:
                    _nodes = nodes
                    while len(_nodes) > 2:
                        self.grammar += f"x{x} -> "+" ".join(_nodes[-2:])+"\n" 
                        _nodes = _nodes[:-2]
                        _nodes.append(f"x{x}")
                        self.grammar += (f"{phrase} -> " + " ".join(_nodes))+"\n"
                        x += 1
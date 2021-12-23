from collections import defaultdict
import numpy as np
import pandas as pd

class CKYParser():

    def __init__(self):
        self.grammar = {}
        self.morphology = {}
        self.lexicon = {}

    def parse(self, sentence):
        """
        
        Arguments:

        """

        table = np.zeros((len(sentence),len(sentence)))

        sent_dict = [self.extract_features(s) for s in sentence] 

        for j in range(1,len(sentence)+1):
            
            table[j-1][j-1] = sent_dict[j-1]["POS"]

            for i in range(j-2, 0, -1):
                for k in range(i+1, j-1):
                    
                    xToken = sent_dict[i]["Token"]
                    yToken = sent_dict[k]["Token"]

                    xPos = table[i][k]
                    yPos = table[k][j-1]
                  
                    for x in xPos:
                        for y in yPos:

                            if (x == "NP" and y == "VP") or (x == "DET" and y == "NP"):
                                if self.check_agreement(x, xToken, y, yToken):
                                    table[i][j-1] = self.check_grammar(x,y)
                                else:
                                    return "UNGRAMMATICAL"
                            else:
                                table[i][j-1] = self.check_grammar(x,y)

        return table

    def check_grammar(self,x,y):
        """
        Check whether two constituents create an another constituent

        Arguments:
            - x: former constituent
            - y: latter constituent
        """
        try:
            return self.grammar[f"{x} {y}"]
        except:
            return False

    def extract_features(self,token):
        """


        Arguments:
        - self: class
        - Token: str
        
        Output:
        - Set of Linguistic Features
            - POS: Possible Part-of-Speech Tags --type: list
            - Case, Number, Person..: Predefined at the morphology map  --type: str
        """
        
        token_dict = defaultdict(str)
        
        lemma = token.split('+')[0]
    
        token_dict["Token"] = token
        token_dict["POS"] = self.lexicon[lemma] 

        for morph in token.split('+')[1:]:
            feat_type, feat = self.morphology[morph]
            token_dict[feat_type] = feat

        return token_dict


    def check_agreement(self, xPOS, xToken ,yPOS, yToken):
        """""
        Check for: 
            - Subject Verb Agreement (Overtness)
                - Ben arkadaşıma hediye aldın. (Person) 
                - Tarihi bir romanlar okudum. (Number) (DET NOUN)
                - Dün babama yardım edeceğim. (Tense) (ADV VERB)
            - Verb Argument Structure Agreement
                - Ben okul gittim. (Noun Incorporation) --> Cannot be separated Argument Structure??
                - Ben okulda gittim. (Lexical Case) VP --> NP.Dat git / PP --> NP.Dat sonra /....
                - Ben kitap okundu. (Number of Arguments) VP.Pass --> NP.Nom V.Pass!!
                
                
                !!Problem with Case=Bare vs Case=Nom
        """""
        x_feats = self.extract_features(xToken)
        y_feats = self.extract_features(yToken)


        pass

    def CFG_to_CNF():
        """
        Case 1: Rules that mix terminals and non-terminals on the RHS
            - Introduce a new dummy non-terminal that covers only the original terminal
        
        Case 2: Rules that have a single non-terminal on the RHS (called unit productions)
            - Rewrite the RHS (say, B) with the RHS of all the non-unit productions or terminals that B leads to
              That is, given A → B, if B => *γ then rewrite as A → γ
        
        Case 3: Rules whose RHS is longer than 2
            - Introduce a new non-terminal that covers two consecutive symbols on the RHS
        
        """
        

        pass
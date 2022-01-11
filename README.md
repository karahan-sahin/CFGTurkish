# CFGTurkish

This is Context-Free Grammar for declarative, imperative, question sentences in Turkish. The default word order is SOV. The grammar also does
not include embedded structures but it does cover complex phenomena such as case agreement and subjec-verb agreement.

There is an implementation of a parser. Cocke-Kasami-Younger(CKY) parser implementation is also added with Chomsky Normal Form(CNF) Grammar transformation.

Lexicon for POS and Argument Structure are obtained from [Starlang Software](https://github.com/StarlangSoftware/Dictionary-Py/blob/master/Dictionary/data/turkish_dictionary.txt)

## Requirements

- `__version__ >= Python 3.6`

```bash
!python -m venv cfg_turkish
!source cfg_turkish/bin/activate
!python -m pip install -r requirements.txt
```
## Usage

After you set up your environment, you need to import package and create an instance of parser.

```python
from CFGTurkish.CKYParser import CKYParser

parser = CKYParser()
parser.parse([tokenized_sentence])
```

- However, the parsing output should be in morphological analysis output with no instance of ambiguous morphology. The original morphological output format is from the *An outline of Turkish Morphology* paper(Oflazer, 1994).
- An example of an input sentence is given below

```python
parser.parse(["Destan+lAr", "milli", "kültür+(H)mHz+(y)H", "ve", "tarih+(H)mHz+(y)H", "anlat+Hr", "."])
```

- The output is in the format below:

```tex
              Destan+lAr        milli kültür+(H)mHz+(y)H      ve tarih+(H)mHz+(y)H       anlat+Hr            .
0  {Noun, NP.Nom, Pnoun}         None               None    None              None           {VP}          {S}
1                   None  {ADJ, ADJP}           {NP.Acc}    None          {NP.Acc}        {VP, S}          {S}
2                   None         None     {Noun, NP.Acc}    None          {NP.Acc}        {VP, S}          {S}
3                   None         None               None  {CONJ}              {x4}           None         None
4                   None         None               None    None    {Noun, NP.Acc}        {VP, S}          {S}
5                   None         None               None    None              None  {Verb, VP, S}  {x1, x0, S}
6                   None         None               None    None              None           None      {PUNCT}
```



## Evaluation

- The evaluation metrics are standard Precision, Recall and F-measure implemented for parsing. The formulae is given below.
- `evalution() ` function is takes the parsed input and true outputs and returns the metric calculations

```
test_sentence = ["Destan+lAr", "milli", "kültür+(H)mHz+(y)H", "ve", "tarih+(H)mHz+(y)H", "anlat+Hr", "."]
y_true = ["NP.Nom", "NP.Bare", "NP.Acc", "Conj", "NP.Acc", "Verb", "PUNCT", "VP"]
y_pred = parser.parse(test_sentence)

p,r,f_1 = evaluation(y_pred,y_true, beta=1) # beta param is the f-1 harmonic parameter 
```


$$
Precision = \frac{S_{gold} \cap S_{model}}{S_{model}} \\

Recall = \frac{S_{gold} \cap S_{model}}{S_{gold}} \\

F-1 = \frac{2\times(P\times R)}{P+ R}
$$

- Results for 10 test instances are given below 

```
Precision: 0.18718288801577834
Recall: 0.8523478835978837
F_measure: 0.3051761973957813
```







TODO:

- [x] CKY Parser
- [x] CFG to CNF
- [x] Lexicon
    - [x] Open-class
    - [x] Close-class
- [x] Morphology Map
    - [x] Nominal
    - [x] Verbal
- [x] Agreement Checker
    - [x] SV Agreement
    - [x] Case Agreement
    - [x] NP Number Agreement
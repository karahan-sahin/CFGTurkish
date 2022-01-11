# CFGTurkish

This is Context-Free Grammar for declarative, imperative, question sentences in Turkish. The default word order is SOV. The grammar also does
not include embedded structures but it does cover complex phenomena such as case agreement and subjec-verb agreement.

There is an implementation of a parser. Cocke-Kasami-Younger(CKY) parser implementation is also added with Chomsky Normal Form(CNF) Grammar transformation.

Lexicon for POS and Argument Structure are obtained from [Starlang Software](https://github.com/StarlangSoftware/Dictionary-Py/blob/master/Dictionary/data/turkish_dictionary.txt)

## Requirements

- `__version__ >= Python 3.6`

```
!python -m venv cfg_turkish
!source cfg_turkish/bin/activate
!python -m pip install -r requirements.txt
```
## Usage

```
from CFGTurkish.CKYParser import CKYParser

parser = CKYParser()
parser.parse([tokenized_sentence])
```

TODO:
- [x] CKY Parser
- [ ] CFG to CNF
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
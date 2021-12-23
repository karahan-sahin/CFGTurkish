# CFGTurkish

This is Context-Free Grammar for declarative, imperative, question sentences in Turkish. The default word order is SOV. The grammar also does
not include embedded structures but it does cover complex phenomena such as case agreement and subjec-verb agreement.

There is an implementation of a parser. Cocke-Kasami-Younger(CKY) parser implementation is also added with Chomsky Normal Form(CNF) Grammar transformation.

Lexicon for POS is added from [Starlang Software](https://github.com/StarlangSoftware/Dictionary-Py/blob/master/Dictionary/data/turkish_dictionary.txt)

TODO:
- [x] CKY Parser
- [ ] CFG to CNF
- [ ] Lexicon
    - [ ] Open-class
    - [ ] Close-class
- [ ] Morphology Map
    - [ ] Nominal
    - [ ] Verbal
- [ ] Agreement Checker
    - [ ] SV Agreement
    - [ ] Case Agreement
    - [ ] NP Number Agreement

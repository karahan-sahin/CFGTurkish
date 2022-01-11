from CKYParser import CKYParser
import sys
def main():
    
    sentences = [

        # Grammatical
        ["Dün", "arkadaş+(H)m+(y)A", "bir", "hediye", "al+DH+(H)m", "."],
        ["Tarihi", "roman+lAr+(y)H", "keyif+(y)lA", "oku+(H)yor+(H)m", "."],
        ["Ben", "dün", "akşam", "yemek+(y)H", "için", "anne+(H)m+(y)A", "yardım", "et+DH+(H)m", "."],
        ["Destan+lAr", "milli", "kültür+(H)mHz+(y)H", "ve", "tarih+(H)mHz+(y)H", "anlat+Hr", "."],
        ["Yaz", "meyve+lAr+(H)n+DAn", "karpuz", "bence", "en", "güzel", "meyve+DHr", "."],
        ["Bu", "akşam+ki", "toplantı+(y)A", "katıl+(y)AcAk", "mi+(sH)nHz", "?"],
        ["Bu", "ağaç+(n)Hn", "alt+(n)H+nDA", "her", "gece", "mehtap+(y)H", "izle+Hr+DH+k", "." ],
        ["Siz", "bura+(y)A", "en", "son", "ne", "zaman", "gel+DH+(sH)nHz", "?"],
        ["Anadolu+(n)Hn", "dört", "yan+(n)H", "medeniyet+(n)Hn", "beşik+nH+DHr", "."],
        ["Orhun", "Abide+lAr+(n)H", "Türkçe+(n)Hn", "ilk", "yazılı", "örnek+lAr+(n)H+DHr", "."], 
        ["Okul", "biz+(H)m", "köy+(y)A", "epeyce", "uzak+DA+DH", "."],
        ["Yüksek", "ses+(y)lA", "müzik", "dinle+mA", "."],

        # Ungrammatical
        ["Ben", "arkadaş+(H)m+(y)A", "hediye","al+DH+(H)n", "."], 
        ["Tarihi", "bir", "roman+lAr", "oku+DH+(H)m", "."], 
        ["Dün", "baba+(H)m+(y)A", "yardım", "et+(y)AcAk+(H)m", "."], 
        ["Ben", "okul", "git+DH+(H)m", "." ],
        ["Ben", "kitap", "oku+Hl+DH", "." ],
        ["Ben", "okul+DA", "git+DH+(H)m", "."],

    ]

    for sentence in sentences:
        parser = CKYParser()
        print(sentence)
        print(parser.parse(sentence))
        print("******************************")

if __name__ == '__main__':
    main()
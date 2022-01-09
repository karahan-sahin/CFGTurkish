from CKYParser import CKYParser

def main():
    
    sentences = [

        # Grammatical
        ["Dün", "arkadaş+Im+yA", "bir", "hediye", "al+DI+Im", "."],
        ["Tarihi", "roman+lAr+yI", "keyif+ylA", "oku+Iyor+Im", "."],
        ["Ben", "dün", "akşam", "yemek+yI", "için", "anne+Im+yA", "yardım", "et+DI+Im", "."],
        ["Destan+lAr", "milli", "kültür+ImIz+yI", "ve", "tarih+ImIz+yI", "anlat+Ir", "."],
        ["Yaz", "meyve+lAr+In+DAn", "karpuz", "bence", "en", "güzel", "meyve+DIr", "."],
        ["Bu", "akşam+ki", "toplantı+yA", "katıl+AcAk", "mi+InIz", "?"],
        ["Bu", "ağaç+In", "alt+In+DA", "her", "gece", "mehtap+yI", "izle+Ir+DI+k", "." ],
        ["Siz", "bura+yA", "en", "son", "ne", "zaman", "gel+DI+InIz", "?"],
        ["Anadolu+nIn", "dört", "yan+yI", "medeniyet+nIn", "beşik+nI+DIr", "."],
        ["Orhun", "Abide+lAr+yI", "Türkçe+nIn", "ilk", "yazılı", "örnek+lAr+nI+DIr", "."], 
        ["Okul", "biz+Im", "köy+yA", "epeyce", "uzak+DA+DI", "."],
        ["Yüksek", "ses+ylA", "müzik", "dinle+mA", "."],

        # Ungrammatical
        ["Ben", "arkadaş+Im+yA", "hediye","al+DI+In", "."], 
        ["Tarihi", "bir", "roman+lAr", "oku+DI+Im", "."], 
        ["Dün", "baba+Im+yA", "yardım", "et+AcAk+Im", "."], 
        ["Ben", "okul", "git+DI+Im", "." ],
        ["Ben", "kitap", "oku+^In+DI", "." ],
        ["Ben", "okul+DA", "git+DI+Im", "."],

    ]

    for sentence in sentences:
        parser = CKYParser()
        print(parser.parse(sentence))
        print("******************************")

if __name__ == '__main__':
    main()
from CKYParser import CKYParser

def main():
    
    sentences = [

        # Grammatical
        ["Dün", "arkadaş+ım+a", "bir", "hediye", "al+dı+m", "."]
        ["Tarihi" "roman+lar+ı" "keyif+yle" "oku+yor+um", "." ],
        ["Ben" "dün" "akşam" "yemek+i" "için" "anne+m+e" "yardım" "et+ti+m" "." ],
        ["Destan+lar" "milli" "kültür+ümüz+ü" "ve" "tarih+imiz+i" "anlat+ır" "."],
        ["Yaz" "meyve+leri+nden" "karpuz" "ben+ce" "en" "güzel" "meyve+dir" "."],
        ["Bu" "akşam+ki" "toplantı+ya" "katıl+acak" "mısınız" "?" ],
        ["Bu" "ağaç+ın" "altı+nda" "her" "gece" "mehtap+ı" "izle+Ir+di+k" "." ],
        ["Siz" "bura+ya" "en" "son" "ne" "zaman" "gel+di+Iniz" "?"],
        ["Anadolu+nun" "dört" "yan+ı" "medeniyet+in" "beşik+i+dir" "."],
        ["Orhun" "Abide+ler+i" "Türkçe+nin" "ilk" "yazılı" "örnek+ler+i+dir" "."], 
        ["Okul" "biz+im" "köy+e" "epey+ce" "uzak+ta+ydı" "."],
        ["Yüksek" "ses+ylA" "müzik" "dinle+me" "."],

        # Ungrammatical
        ["Ben", "arkadaş+Im+a", "hediye","al+DI+In", "."] 
        ["Tarihi", "bir", "roman+lAr", "oku+DI+Im", "."] 
        ["Dün", "baba+Im+A", "yardım", "et+AcAK+Im", "."] 
        ["Ben", "okul", "git+DI+Im", "." ]
        ["Ben", "kitap", "oku+N+DI", "." ]
        ["Ben", "okul+Da", "git+DI+Im", "."]

    ]

    parser = CKYParser()

    for sentence in sentences:
        print(parser.parse(sentence))

if __name__ == '__main__':
    main()
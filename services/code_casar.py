#Цезарь шифровка

def caesar(key, mes):
    alfavit = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    message = mes.upper()
    res = ''

    for i in message:
        place = alfavit.find(i)
        new_place = place + key
        if i in alfavit:
            res += alfavit[new_place]
        else:
            res += i
    return res


#Цезарь дешифровка
def caesar_decod(key, mes):
    alfavit = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    message = mes.upper()
    res = ''

    for i in message:
        place = alfavit.find(i)
        new_place = place - key
        if i in alfavit:
            res += alfavit[new_place]
        else:
            res += i
    return res

#ATBASH
def atbash(mes):
    alfavit = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    return mes.translate(str.maketrans(alfavit + alfavit.upper(), alfavit[::-1] + alfavit.upper()[::-1]))
import pandas as pd

domains = [".com", ".org", ".net", ".biz", ".info"]

DB = pd.read_excel("../student_v.1.17.xlsx")
TN_DB = pd.read_excel("../vary_nice.xlsx")

OUT_DB = DB.copy()
OUT_DB["смещение"] = [0] * DB.shape[0]


def decode(email, address, step):
    ans = ""

    for symbol in email:
        if symbol == "@" or symbol == ".":
            ans += symbol
        else:
            ans += chr(97 + (ord(symbol) - 97 + step) % 26)

    ans += "----"

    for symbol in address:
        if 1039 < ord(symbol) < 1072:
            ans += chr(1040 + (ord(symbol) + step + 6 - 1040) % 32)
        elif 1072 <= ord(symbol) < 1104:
            ans += chr(1072 + (ord(symbol) + step + 6 - 1072) % 32)
        else:
            ans += symbol
    return ans


def main():
    for i in range(len(DB['email'])):
        final_step = -1

        for step in range(0, 33):
            email = decode(DB['email'][i], DB['Адрес'][i], step).split("----")[0]

            for domain in domains:
                if domain in email:
                    final_step = step
                    break

            if final_step >= 0:
                break

        email, address = decode(DB['email'][i], DB['Адрес'][i], final_step).split("----")

        ulala = OUT_DB["Телефон"][i]

        numberA = TN_DB[TN_DB['шифр'] == ulala]['номер'].array[0]
        print(numberA)
        OUT_DB["Телефон"][i] = numberA

        OUT_DB["email"][i] = email
        OUT_DB["Адрес"][i] = address
        OUT_DB["смещение"][i] = final_step

    OUT_DB.to_excel("../ready.xlsx")


if __name__ == '__main__':
    main()

'''

['adolfoas@oconner.biz', 'Кривоникольский пер.д.58 кв.354'] 1
['jmxuoxjb@xlxwwna.kri', 'Ущслчцсучфеъуст шощ.н.58 ул.354'] 2

['ismaeloo@yahoo.com', 'Куркинское ш.д.59 кв.311'] 20
['ueymqxaa@kmtaa.oay', 'Цяьцфщэцъс д.р.59 цо.311'] 8

['babernathy@yahoo.com', 'ул. Куинджид.13 кв.205'] 8
['ihilyuhaof@fhovv.jvt', 'ът. Съпфлнпл.13 сй.205'] 1
['josephzw@gmail.com', 'ул. Новинкид.88 кв.45'] 9
['qvzlwogd@nthps.jvt', 'ът. Фхйпфспл.88 сй.45'] 2

'''


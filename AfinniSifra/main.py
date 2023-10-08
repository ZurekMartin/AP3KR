# import knihoven
import unicodedata
import math
import tkinter as tk
from tkinter import *

# vytvoreni okna aplikace
# zakazani zmeny velikosti okna aplikace
# pojmenovani okna aplikace
root = tk.Tk()
root.resizable(False, False)
root.title("Afinní šifra")

# definovani jednotlivych casti abecedy
# spojeni casti do vychozi abecedy
# definovani promenne pro zjisteni velikosti abecedy
lowerCased = list(map(chr, range(ord('a'), ord('z') + 1)))
upperCased = list(map(chr, range(ord('A'), ord('Z') + 1)))
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alphabet = lowerCased + upperCased + numbers
alphabetLength = len(alphabet)


# funkce pro sifrovani textu, provede se kontrola zdali klice splnuji podminky (error je pripadne vypsan)
# vytvori se prazdny retec do ktereho se pozdeji ulozi sifrovany text
# aktualizuje se textbox pro zadavani textu
# retezec se rozdeli na jednotlive znaky a diakritiku a nasledne jsou znaky bez diakritiky opet spojeny
# kazdy znak je iterovan a jsou odstraneny vsechny nealfanumericke znaky, mezery jsou ponechany
# mezery jsou nahrazeny "XMEZERAX"
# vyfiltrovany text je vlozen do textboxu
# for cyklem je kazdy znak ve vyfiltrovanem retezci iterovan
# je zjisten index znaku v abecede
# je vypocitan index zasifrovaneho znaku
# znak s odpovidajicim zasifrovanym indexem je pridan do zasifrovaneho retezce
# zasifrovany text je vlozen do textboxu
def encrypt(plainText, keyA, keyB):
    if keyA == alphabetLength or math.gcd(keyA, keyB) != 1. or keyA % 2 == 0 or keyA < 1 or keyB < 1:
        error = "Zadejte jinou hodnotu klíče A!"
        textbox3.delete(0, END)
        textbox3.insert(0, error)
    else:
        cipherText = ""
        textbox1.delete(0, END)
        textbox1.insert(0, plainText)
        unfilteredText = ''.join(c for c in unicodedata.normalize('NFD', plainText) if unicodedata.category(c) != 'Mn')
        semifilteredText = ''.join(e for e in unfilteredText if e.isalnum() or e == ' ')
        filteredText = semifilteredText.replace(" ", "XMEZERAX")
        textbox2.delete(0, END)
        textbox2.insert(0, filteredText)
        for char in filteredText:
            characterIndex = alphabet.index(char)
            cipherIndex = (keyA * characterIndex + keyB) % alphabetLength
            cipherText += alphabet[cipherIndex]
        cipherText = ' '.join([cipherText[i:i + 5] for i in range(0, len(cipherText), 5)])
        # cipherText = cipherText.upper()
        textbox3.delete(0, END)
        textbox3.insert(0, cipherText)


# funkce pro desifrovani textu, provede se kontrola zdali klice splnuji podminky (error je pripadne vypsan)
# vytvori se prazdny retec do ktereho se pozdeji ulozi nefiltrovany text
# aktualizuje se textbox pro zadavani textu
# z retezce cipherText jsou odebrany mezery
# for cyklem je kazdy znak v retezci iterovan
# je zjisten index znaku v abecede
# je vypocitan index desifrovaneho znaku
# znak s odpovidajicim indexem je pridan do nefiltrovaneho retezce
# nefiltrovany text je vlozen do textboxu
# vytvori se retezec pro desifrovany text ve kterem je "XMEZERAX" nahrazena mezerou
# desifrovany text je vlozen do textboxu
def decrypt(cipherText, keyA, keyB):
    if keyA == alphabetLength or math.gcd(keyA, keyB) != 1 or keyA % 2 == 0 or keyA < 1 or keyB < 1:
        error = "Zadejte jinou hodnotu klíče A!"
        textbox10.delete(0, END)
        textbox10.insert(0, error)
    else:
        openText = ""
        textbox8.delete(0, END)
        textbox8.insert(0, cipherText)
        cipherText = cipherText.replace(" ", "")
        for char in cipherText:
            characterIndex = alphabet.index(char)
            plainIndex = pow(keyA, -1, alphabetLength) * (characterIndex - keyB) % alphabetLength
            openText += alphabet[plainIndex]
        textbox9.delete(0, END)
        textbox9.insert(0, openText)
        plainText = openText.replace("XMEZERAX", " ")
        textbox10.delete(0, END)
        textbox10.insert(0, plainText)


# funkce pro smazani veskereho textu v textboxech, krome klice A a klice B a vypisu abeced
def clearTextboxes():
    textbox1.delete(0, END)
    textbox2.delete(0, END)
    textbox3.delete(0, END)
    textbox8.delete(0, END)
    textbox9.delete(0, END)
    textbox10.delete(0, END)

# funkce pro smazani veskereho textu v textboxech, vlozeni zakladni hodnoty do klice A a B a resetovani slideru
def clearAllTextboxes():
    textbox1.delete(0, END)
    textbox2.delete(0, END)
    textbox3.delete(0, END)
    textbox4.delete(0, END)
    textbox4.insert(0, int(1))
    textbox5.delete(0, END)
    textbox5.insert(0, int(1))
    slider1.set(0)
    textbox6.delete(0, END)
    textbox7.delete(0, END)
    textbox8.delete(0, END)
    textbox9.delete(0, END)
    textbox10.delete(0, END)


# funkce pro zobrazeni znaku v zasifrovane abecede a ve vychozi abecede
def charactersCorespondingToIndex(index):
    if int(textbox4.get()) == alphabetLength or math.gcd(int(textbox4.get()), int(textbox5.get())) != 1 or int(
            textbox4.get()) % 2 == 0 or int(textbox4.get()) < 1 or int(textbox5.get()) < 1:
        error = "Zadejte jinou hodnotu klíče A!"
        textbox6.delete(0, END)
        textbox6.insert(0, error)
        textbox7.delete(0, END)
        textbox7.insert(0, error)
    else:
        plainIndex = int(index)
        cipherIndex = (int(textbox4.get()) * plainIndex + int(textbox5.get())) % alphabetLength
        cipherCharacter = alphabet[cipherIndex]
        plainCharacter = alphabet[plainIndex]
        textbox6.delete(0, END)
        textbox6.insert(0, cipherCharacter)
        textbox7.delete(0, END)
        textbox7.insert(0, plainCharacter)


# encryptPlainText
label1 = tk.Label(root, text="Text k šifrování")
label1.grid(row=1, column=0)
textbox1 = tk.Entry(root)
textbox1.grid(row=2, column=0)

# filteredText
label2 = tk.Label(root, text="Filtrovaný text")
label2.grid(row=3, column=0)
textbox2 = tk.Entry(root)
textbox2.grid(row=4, column=0)

# cipherText
label3 = tk.Label(root, text="Zašifrovaný text")
label3.grid(row=5, column=0)
textbox3 = tk.Entry(root)
textbox3.grid(row=6, column=0)

# encryptButton
button1 = tk.Button(root, text="Šifrovat", command=lambda: encrypt(
    textbox10.get() if len(textbox10.get()) > len(textbox1.get()) else textbox1.get(), int(textbox4.get()),
    int(textbox5.get())))
button1.grid(row=7, column=0)

# keyA
label4 = tk.Label(root, text="Klíč A")
label4.grid(row=0, column=1)
textbox4 = tk.Entry(root)
textbox4.grid(row=1, column=1)

# keyB
label5 = tk.Label(root, text="Klíč B")
label5.grid(row=0, column=2)
textbox5 = tk.Entry(root)
textbox5.grid(row=1, column=2)

# indexSlider
slider1 = tk.Scale(root, from_=0, to=alphabetLength - 1, orient="horizontal")
slider1.grid(row=3, column=1, columnspan=2)
slider1.config(command=charactersCorespondingToIndex)

# cipherIndex
label6 = tk.Label(root, text="Zašifrovaná abeceda")
label6.grid(row=5, column=1)
textbox6 = tk.Entry(root)
textbox6.grid(row=6, column=1)

# characterIndex
label7 = tk.Label(root, text="Výchozí abeceda")
label7.grid(row=5, column=2)
textbox7 = tk.Entry(root)
textbox7.grid(row=6, column=2)

# clearTextboxesButton
button2 = tk.Button(root, text="Smazat", command=lambda: clearTextboxes())
button2.grid(row=7, column=1)

# clearAllTextboxesButton
button3 = tk.Button(root, text="Smazat vše", command=lambda: clearAllTextboxes())
button3.grid(row=7, column=2)

# decryptCipherText
label8 = tk.Label(root, text="Text k dešifrování")
label8.grid(row=1, column=4)
textbox8 = tk.Entry(root)
textbox8.grid(row=2, column=4)

# unfilteredText
label9 = tk.Label(root, text="Nefiltrovaný text")
label9.grid(row=3, column=4)
textbox9 = tk.Entry(root)
textbox9.grid(row=4, column=4)

# plaintText
label10 = tk.Label(root, text="Dešifrovaný text")
label10.grid(row=5, column=4)
textbox10 = tk.Entry(root)
textbox10.grid(row=6, column=4)

# decryptButton
button4 = tk.Button(root, text="Dešifrovat", command=lambda: decrypt(
    textbox3.get() if len(textbox3.get()) > len(textbox8.get()) else textbox8.get(), int(textbox4.get()),
    int(textbox5.get())))
button4.grid(row=7, column=4)

root.mainloop()

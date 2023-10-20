# Libraries import
import unicodedata
import math
import tkinter as tk
from tkinter import *

# Application settings
root = tk.Tk()
root.resizable(False, False)
root.title("Affine Cipher")

# Defining alphabet and variable
lower_case = list(map(chr, range(ord('a'), ord('z') + 1)))
upper_case = list(map(chr, range(ord('A'), ord('Z') + 1)))
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alphabet = lower_case + upper_case + digits
alphabet_length = len(alphabet)


# Encrypt function
def encrypt(plain_text, key_a, key_b):
    if key_a == alphabet_length or math.gcd(key_a, key_b) != 1. or key_a % 2 == 0 or key_a < 1 or key_b < 1:
        error = "Change value of Key A!"
        textbox3.delete(0, END)
        textbox3.insert(0, error)
    else:
        cipher_text = ""
        textbox1.delete(0, END)
        textbox1.insert(0, plain_text)
        unfiltered_text = ''.join(
            c for c in unicodedata.normalize('NFD', plain_text) if unicodedata.category(c) != 'Mn')
        semifiltered_text = ''.join(e for e in unfiltered_text if e.isalnum() or e == ' ')
        filtered_text = semifiltered_text.replace(" ", "XSPACEX")
        textbox2.delete(0, END)
        textbox2.insert(0, filtered_text)
        for character in filtered_text:
            character_index = alphabet.index(character)
            cipher_index = (key_a * character_index + key_b) % alphabet_length
            cipher_text += alphabet[cipher_index]
        cipher_text = ' '.join([cipher_text[i:i + 5] for i in range(0, len(cipher_text), 5)])
        textbox3.delete(0, END)
        textbox3.insert(0, cipher_text)


# Decrypt function
def decrypt(cipher_text, key_a, key_b):
    if key_a == alphabet_length or math.gcd(key_a, key_b) != 1 or key_a % 2 == 0 or key_a < 1 or key_b < 1:
        error = "Change value of Key A!"
        textbox10.delete(0, END)
        textbox10.insert(0, error)
    else:
        open_text = ""
        textbox8.delete(0, END)
        textbox8.insert(0, cipher_text)
        cipher_text = cipher_text.replace(" ", "")
        for character in cipher_text:
            character_index = alphabet.index(character)
            plain_index = pow(key_a, -1, alphabet_length) * (character_index - key_b) % alphabet_length
            open_text += alphabet[plain_index]
        textbox9.delete(0, END)
        textbox9.insert(0, open_text)
        plain_text = open_text.replace("XSPACEX", " ")
        textbox10.delete(0, END)
        textbox10.insert(0, plain_text)


# Clear button function
def clear_button():
    textbox1.delete(0, END)
    textbox2.delete(0, END)
    textbox3.delete(0, END)
    textbox8.delete(0, END)
    textbox9.delete(0, END)
    textbox10.delete(0, END)


# Clear all button function
def clear_all_button():
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


# Show characters coresponding to index function
def show_characters_coresponding_to_index(index):
    if int(textbox4.get()) == alphabet_length or math.gcd(int(textbox4.get()), int(textbox5.get())) != 1 or int(
            textbox4.get()) % 2 == 0 or int(textbox4.get()) < 1 or int(textbox5.get()) < 1:
        error = "Change value of Key A!"
        textbox6.delete(0, END)
        textbox6.insert(0, error)
        textbox7.delete(0, END)
        textbox7.insert(0, error)
    else:
        plain_index = int(index)
        cipher_index = (int(textbox4.get()) * plain_index + int(textbox5.get())) % alphabet_length
        cipher_character = alphabet[cipher_index]
        plain_character = alphabet[plain_index]
        textbox6.delete(0, END)
        textbox6.insert(0, cipher_character)
        textbox7.delete(0, END)
        textbox7.insert(0, plain_character)


# Encrypt plain text
label1 = tk.Label(root, text="Text to encrypt")
label1.grid(row=1, column=0)
textbox1 = tk.Entry(root)
textbox1.grid(row=2, column=0)

# Filtered text
label2 = tk.Label(root, text="Filtered text")
label2.grid(row=3, column=0)
textbox2 = tk.Entry(root)
textbox2.grid(row=4, column=0)

# Cipher text
label3 = tk.Label(root, text="Cipher text")
label3.grid(row=5, column=0)
textbox3 = tk.Entry(root)
textbox3.grid(row=6, column=0)

# Encrypt button
button1 = tk.Button(root, text="Encrypt", command=lambda: encrypt(
    textbox10.get() if len(textbox10.get()) > len(textbox1.get()) else textbox1.get(), int(textbox4.get()),
    int(textbox5.get())))
button1.grid(row=7, column=0)

# Key a
label4 = tk.Label(root, text="Key A")
label4.grid(row=0, column=1)
textbox4 = tk.Entry(root)
textbox4.grid(row=1, column=1)

# Key b
label5 = tk.Label(root, text="Key B")
label5.grid(row=0, column=2)
textbox5 = tk.Entry(root)
textbox5.grid(row=1, column=2)

# Index slider
slider1 = tk.Scale(root, from_=0, to=alphabet_length - 1, orient="horizontal")
slider1.grid(row=3, column=1, columnspan=2)
slider1.config(command=show_characters_coresponding_to_index)

# Cipher index
label6 = tk.Label(root, text="Encrypted character")
label6.grid(row=5, column=1)
textbox6 = tk.Entry(root)
textbox6.grid(row=6, column=1)

# Character index
label7 = tk.Label(root, text="Default character")
label7.grid(row=5, column=2)
textbox7 = tk.Entry(root)
textbox7.grid(row=6, column=2)

# Clear button
button2 = tk.Button(root, text="Clear", command=lambda: clear_button())
button2.grid(row=7, column=1)

# Clear all button
button3 = tk.Button(root, text="Clear all", command=lambda: clear_all_button())
button3.grid(row=7, column=2)

# Decrypt cipher text
label8 = tk.Label(root, text="Text to decrypt")
label8.grid(row=1, column=4)
textbox8 = tk.Entry(root)
textbox8.grid(row=2, column=4)

# Unfiltered text
label9 = tk.Label(root, text="Unfiltered text")
label9.grid(row=3, column=4)
textbox9 = tk.Entry(root)
textbox9.grid(row=4, column=4)

# Plain text
label10 = tk.Label(root, text="Plain text")
label10.grid(row=5, column=4)
textbox10 = tk.Entry(root)
textbox10.grid(row=6, column=4)

# Decrypt button
button4 = tk.Button(root, text="Decrypt", command=lambda: decrypt(
    textbox3.get() if len(textbox3.get()) > len(textbox8.get()) else textbox8.get(), int(textbox4.get()),
    int(textbox5.get())))
button4.grid(row=7, column=4)

# Main loop
root.mainloop()

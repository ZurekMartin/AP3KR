# Libraries import
import random
import unicodedata
import tkinter as tk
import customtkinter as ctk
from CTkTable import *

# Application settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


# Defining application class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("ADFGVX Cipher")

        # Defining alphabets and variables
        upper_case = list(map(chr, range(ord('A'), ord('Z') + 1)))
        digits = list(map(chr, range(ord('0'), ord('9') + 1)))
        alphabet_25_cz = [chr(i) for i in range(ord('A'), ord('Z') + 1) if chr(i) != 'W']
        alphabet_25_en = [chr(i) for i in range(ord('A'), ord('Z') + 1) if chr(i) != 'J']
        alphabet_36 = upper_case + digits
        rows_25 = ['A', 'D', 'F', 'G', 'X']
        columns_25 = ['A', 'D', 'F', 'G', 'X']
        table_25 = ['(0) A', '(1) D', '(2) F', '(3) G', '(4) X']
        rows_36 = ['A', 'D', 'F', 'G', 'V', 'X']
        columns_36 = ['A', 'D', 'F', 'G', 'V', 'X']
        table_36 = ['(0) A', '(1) D', '(2) F', '(3) G', '(4) V', '(5) X']
        key_dictionary = ["NEJKULAŤOULINKATĚJŠÍ", "MOTHER-IN-LAW", "ŘEŘICHA", "APPLE", "KŮŇ", "CAT"]

        # Encrypt function for 25 characters
        def encrypt_25(plain_text, alphabet, key, table_alphabet):
            cipher_text = ''
            self.textbox1.set('')
            self.textbox1.set(plain_text)
            filtered_plain_text = plain_text_filter_25(plain_text, alphabet)
            self.textbox2.set('')
            self.textbox2.set(filtered_plain_text)
            filtered_key = key_filter(key, alphabet)
            substituted_text = ''
            substitution_matrix = [['' for _ in range(5)] for _ in range(5)]
            index = 0
            for i in range(5):
                for j in range(5):
                    substitution_matrix[i][j] = table_alphabet[index]
                    index += 1
            for character in filtered_plain_text:
                row, column = character_search(5, substitution_matrix, character)
                substituted_text += rows_25[row] + columns_25[column]
            substituted_text = " ".join([substituted_text[i:i + 2] for i in range(0, len(substituted_text), 2)])
            self.textbox3.set('')
            self.textbox3.set(substituted_text)
            substituted_text = substituted_text.replace(" ", "")
            columns = len(filtered_key)
            rows = len(substituted_text) // columns
            if len(substituted_text) % columns != 0:
                rows += 1
            transposition_matrix = [['' for _ in range(columns)] for _ in range(rows)]
            for i in range(rows):
                for j in range(columns):
                    if i * columns + j < len(substituted_text):
                        transposition_matrix[i][j] = substituted_text[i * columns + j]
                    else:
                        transposition_matrix[i][j] = 'ADFGX'
            key_index = [i for i in range(len(filtered_key))]
            key_index.sort(key=lambda i: filtered_key[i])
            for i in key_index:
                cipher_text += ''.join([row[i] for row in transposition_matrix])
            cipher_text = " ".join([cipher_text[i:i + 5] for i in range(0, len(cipher_text), 5)])
            self.textbox4.set('')
            self.textbox4.set(cipher_text)
            return substitution_matrix, transposition_matrix, filtered_key

        # Decrypt function for 25 characters
        def decrypt_25(cipher_text, alphabet, key, table_alphabet):
            plain_text = ''
            self.textbox7.set('')
            self.textbox7.set(cipher_text)
            cipher_text = cipher_text.replace(" ", "")
            cipher_text = cipher_text.replace("ADFGX", " ")
            filtered_key = key_filter(key, alphabet)
            transposition_matrix = [['' for _ in range(len(filtered_key))] for _ in
                                    range(len(cipher_text) // len(filtered_key))]
            key_index = [i for i in range(len(filtered_key))]
            key_index.sort(key=lambda i: filtered_key[i])
            index = 0
            for column in key_index:
                for row in range(len(cipher_text) // len(filtered_key)):
                    transposition_matrix[row][column] = cipher_text[index]
                    index += 1
            detransposed_text = ''
            for row in transposition_matrix:
                for character in row:
                    detransposed_text += character
            detransposed_text = " ".join([detransposed_text[i:i + 2] for i in range(0, len(detransposed_text), 2)])
            self.textbox8.set('')
            self.textbox8.set(detransposed_text)
            substituted_text = ''
            for row in transposition_matrix:
                for character in row:
                    if character != ' ':
                        substituted_text += character
            substitution_matrix = [['' for _ in range(5)] for _ in range(5)]
            index = 0
            for i in range(5):
                for j in range(5):
                    substitution_matrix[i][j] = table_alphabet[index]
                    index += 1
            for i in range(0, len(substituted_text), 2):
                row = rows_25.index(substituted_text[i])
                column = columns_25.index(substituted_text[i + 1])
                plain_text += substitution_matrix[row][column]
            self.textbox9.set('')
            self.textbox9.set(plain_text)
            plain_text = plain_text.replace("XZEROX", "0")
            plain_text = plain_text.replace("XONEX", "1")
            plain_text = plain_text.replace("XTVOX", "2")
            plain_text = plain_text.replace("XTHREEX", "3")
            plain_text = plain_text.replace("XFOURX", "4")
            plain_text = plain_text.replace("XFIVEX", "5")
            plain_text = plain_text.replace("XSIXX", "6")
            plain_text = plain_text.replace("XSEVENX", "7")
            plain_text = plain_text.replace("XEIGHTX", "8")
            plain_text = plain_text.replace("XNINEX", "9")
            plain_text = plain_text.replace("XSPACEX", " ")
            self.textbox10.set('')
            self.textbox10.set(plain_text)

        # Plain text filtering function for 25 characters
        def plain_text_filter_25(plain_text, alphabet):
            plain_text = plain_text.replace("0", "XZEROX")
            plain_text = plain_text.replace("1", "XONEX")
            plain_text = plain_text.replace("2", "XTVOX")
            plain_text = plain_text.replace("3", "XTHREEX")
            plain_text = plain_text.replace("4", "XFOURX")
            plain_text = plain_text.replace("5", "XFIVEX")
            plain_text = plain_text.replace("6", "XSIXX")
            plain_text = plain_text.replace("7", "XSEVENX")
            plain_text = plain_text.replace("8", "XEIGHTX")
            plain_text = plain_text.replace("9", "XNINEX")
            unfiltered_plain_text = ''.join(
                c for c in unicodedata.normalize('NFD', plain_text) if unicodedata.category(c) != 'Mn')
            semifiltered_plain_text = ''.join(e for e in unfiltered_plain_text if e.isalpha() or e == ' ')
            filtered_plain_text = semifiltered_plain_text.replace(" ", "XSPACEX")
            if alphabet == alphabet_25_cz:
                filtered_plain_text = filtered_plain_text.replace("W", "V")
            else:
                filtered_plain_text = filtered_plain_text.replace("J", "I")
            return filtered_plain_text

        # Encrypt function for 36 characters
        def encrypt_36(plain_text, alphabet, key, table_alphabet):
            cipher_text = ''
            self.textbox1.set('')
            self.textbox1.set(plain_text)
            filtered_plain_text = plain_text_filter_36(plain_text)
            self.textbox2.set('')
            self.textbox2.set(filtered_plain_text)
            filtered_key = key_filter(key, alphabet)
            substituted_text = ''
            substitution_matrix = [['' for _ in range(6)] for _ in range(6)]
            index = 0
            for i in range(6):
                for j in range(6):
                    substitution_matrix[i][j] = table_alphabet[index]
                    index += 1
            for character in filtered_plain_text:
                row, column = character_search(6, substitution_matrix, character)
                substituted_text += rows_36[row] + columns_36[column]
            substituted_text = " ".join([substituted_text[i:i + 2] for i in range(0, len(substituted_text), 2)])
            self.textbox3.set('')
            self.textbox3.set(substituted_text)
            substituted_text = substituted_text.replace(" ", "")
            columns = len(filtered_key)
            rows = len(substituted_text) // columns
            if len(substituted_text) % columns != 0:
                rows += 1
            transposition_matrix = [['' for _ in range(columns)] for _ in range(rows)]
            for i in range(rows):
                for j in range(columns):
                    if i * columns + j < len(substituted_text):
                        transposition_matrix[i][j] = substituted_text[i * columns + j]
                    else:
                        transposition_matrix[i][j] = 'ADFGVX'
            key_index = [i for i in range(len(filtered_key))]
            key_index.sort(key=lambda i: filtered_key[i])
            for i in key_index:
                cipher_text += ''.join([row[i] for row in transposition_matrix])
            cipher_text = " ".join([cipher_text[i:i + 5] for i in range(0, len(cipher_text), 5)])
            self.textbox4.set('')
            self.textbox4.set(cipher_text)
            return substitution_matrix, transposition_matrix, filtered_key

        # Decrypt function for 36 characters
        def decrypt_36(cipher_text, alphabet, key, table_alphabet):
            plain_text = ''
            self.textbox7.set('')
            self.textbox7.set(cipher_text)
            cipher_text = cipher_text.replace(" ", "")
            cipher_text = cipher_text.replace("ADFGVX", " ")
            filtered_key = key_filter(key, alphabet)
            transposition_matrix = [['' for _ in range(len(filtered_key))] for _ in
                                    range(len(cipher_text) // len(filtered_key))]
            key_index = [i for i in range(len(filtered_key))]
            key_index.sort(key=lambda i: filtered_key[i])
            index = 0
            for column in key_index:
                for row in range(len(cipher_text) // len(filtered_key)):
                    transposition_matrix[row][column] = cipher_text[index]
                    index += 1
            detransposed_text = ''
            for row in transposition_matrix:
                for character in row:
                    detransposed_text += character
            detransposed_text = " ".join([detransposed_text[i:i + 2] for i in range(0, len(detransposed_text), 2)])
            self.textbox8.set('')
            self.textbox8.set(detransposed_text)
            substituted_text = ''
            for row in transposition_matrix:
                for character in row:
                    if character != ' ':
                        substituted_text += character
            substitution_matrix = [['' for _ in range(6)] for _ in range(6)]
            index = 0
            for i in range(6):
                for j in range(6):
                    substitution_matrix[i][j] = table_alphabet[index]
                    index += 1
            for i in range(0, len(substituted_text), 2):
                row = rows_36.index(substituted_text[i])
                column = columns_36.index(substituted_text[i + 1])
                plain_text += substitution_matrix[row][column]
            self.textbox9.set('')
            self.textbox9.set(plain_text)
            plain_text = plain_text.replace("XSPACEX", " ")
            self.textbox10.set('')
            self.textbox10.set(plain_text)

        # Plain text filtering function for 36 characters
        def plain_text_filter_36(plain_text):
            unfiltered_plain_text = ''.join(
                c for c in unicodedata.normalize('NFD', plain_text) if unicodedata.category(c) != 'Mn')
            semifiltered_plain_text = ''.join(e for e in unfiltered_plain_text if e.isalnum() or e == ' ')
            filtered_plain_text = semifiltered_plain_text.replace(" ", "XSPACEX")
            return filtered_plain_text

        # Key filtering function
        def key_filter(key, alphabet):
            unfiltered_key = ''.join(c for c in unicodedata.normalize('NFD', key) if unicodedata.category(c) != 'Mn')
            semifiltered_key = ''.join(e for e in unfiltered_key if e.isalpha())
            if alphabet == alphabet_25_cz:
                temporary_key = semifiltered_key.replace("W", "V")
            else:
                temporary_key = semifiltered_key.replace("J", "I")
            filtered_key = []
            character_count = {}
            for character in temporary_key:
                if character not in character_count:
                    character_count[character] = 1
                    filtered_key.append(character)
                else:
                    character_count[character] += 1
                    filtered_key.append(character + str(character_count[character]))
            return filtered_key

        # Character searching function
        def character_search(size, matrix, character):
            for i in range(size):
                for j in range(size):
                    if matrix[i][j] == character:
                        return i, j

        # Encrypt button function
        def encrypt_button():
            if self.textbox1.get() == '' and self.textbox10.get() == '':
                error_encrypt = "Enter text to encrypt!"
                error = 'Enter value!'
                self.textbox1.set('')
                self.textbox1.set(error_encrypt)
            if self.textbox5.get() == '':
                self.textbox5.set('')
                self.textbox5.set(error)
            if self.textbox6.get() == '':
                self.textbox6.set('')
                self.textbox6.set(error)
            else:
                if self.segmented_button1.get() == "CZ" and self.segmented_button3.get() == "ADFGX":
                    encrypt_25(
                        self.textbox10.get() if len(self.textbox10.get()) > len(
                            self.textbox1.get()) else self.textbox1.get(),
                        alphabet_25_cz, self.textbox6.get(), self.textbox5.get())
                if self.segmented_button1.get() == "EN" and self.segmented_button3.get() == "ADFGX":
                    encrypt_25(
                        self.textbox10.get() if len(self.textbox10.get()) > len(
                            self.textbox1.get()) else self.textbox1.get(),
                        alphabet_25_en, self.textbox6.get(), self.textbox5.get())
                if self.segmented_button3.get() == "ADFGVX":
                    encrypt_36(
                        self.textbox10.get() if len(self.textbox10.get()) > len(
                            self.textbox1.get()) else self.textbox1.get(),
                        alphabet_36, self.textbox6.get(), self.textbox5.get())

        # Clear button function
        def clear_button():
            self.textbox1.set('')
            self.textbox2.set('')
            self.textbox3.set('')
            self.textbox4.set('')
            self.textbox7.set('')
            self.textbox8.set('')
            self.textbox9.set('')
            self.textbox10.set('')

        # Show table button function
        def show_table_button():
            if hasattr(self, 'table'):
                self.table.destroy()
            if self.textbox5.get() == '' and self.textbox6.get() == '':
                error = "Enter value!"
                self.textbox5.set('')
                self.textbox5.set(error)
                self.textbox6.set('')
                self.textbox6.set(error)
            if self.segmented_button2.get() == "Substitution":
                if self.segmented_button1.get() == "CZ" and self.segmented_button3.get() == "ADFGX" and len(
                        self.textbox5.get()) == 25:
                    substitution_matrix, _, filtered_key = encrypt_25(
                        self.textbox10.get() if len(self.textbox10.get()) > len(
                            self.textbox1.get()) else self.textbox1.get(), alphabet_25_cz, self.textbox6.get(),
                        self.textbox5.get())
                    substitution_matrix.insert(0, [''] + table_25)
                    for i in range(1, 6):
                        substitution_matrix[i] = [table_25[i - 1]] + substitution_matrix[i]
                    self.table = CTkTable(self, values=substitution_matrix)
                    self.table.grid(row=2, column=2, rowspan=7, columnspan=2)
                if self.segmented_button1.get() == "EN" and self.segmented_button3.get() == "ADFGX" and len(
                        self.textbox5.get()) == 25:
                    substitution_matrix, _, filtered_key = encrypt_25(
                        self.textbox10.get() if len(self.textbox10.get()) > len(
                            self.textbox1.get()) else self.textbox1.get(), alphabet_25_en, self.textbox6.get(),
                        self.textbox5.get())
                    substitution_matrix.insert(0, [''] + table_25)
                    for i in range(1, 6):
                        substitution_matrix[i] = [table_25[i - 1]] + substitution_matrix[i]
                    self.table = CTkTable(self, values=substitution_matrix)
                    self.table.grid(row=2, column=2, rowspan=7, columnspan=2)
                if self.segmented_button3.get() == "ADFGVX" and len(self.textbox5.get()) == 36:
                    substitution_matrix, _, filtered_key = encrypt_36(
                        self.textbox10.get() if len(self.textbox10.get()) > len(
                            self.textbox1.get()) else self.textbox1.get(), alphabet_36, self.textbox6.get(),
                        self.textbox5.get())
                    substitution_matrix.insert(0, [''] + table_36)
                    for i in range(1, 7):
                        substitution_matrix[i] = [table_36[i - 1]] + substitution_matrix[i]
                    self.table = CTkTable(self, values=substitution_matrix)
                    self.table.grid(row=2, column=2, rowspan=7, columnspan=2)
                else:
                    self.label7.configure(text="Invalid alphabet length!")
            if self.segmented_button2.get() == "Transposition":
                if self.textbox1.get() == '' and self.textbox10.get() == '':
                    error = "Enter text to encrypt!"
                    self.textbox1.set('')
                    self.textbox1.set(error)
                else:
                    if self.segmented_button1.get() == "CZ" and self.segmented_button3.get() == "ADFGX" and len(
                            self.textbox5.get()) == 25:
                        _, transposition_matrix, filtered_key = encrypt_25(
                            self.textbox10.get() if len(self.textbox10.get()) > len(
                                self.textbox1.get()) else self.textbox1.get(), alphabet_25_cz, self.textbox6.get(),
                            self.textbox5.get())
                        transposition_matrix = [[''.join(['( ', c, ' )']) for c in filtered_key]] + transposition_matrix
                        self.table = CTkTable(self, values=transposition_matrix)
                        self.table.grid(row=2, column=2, rowspan=7, columnspan=2)
                    if self.segmented_button1.get() == "EN" and self.segmented_button3.get() == "ADFGX" and len(
                            self.textbox5.get()) == 25:
                        _, transposition_matrix, filtered_key = encrypt_25(
                            self.textbox10.get() if len(self.textbox10.get()) > len(
                                self.textbox1.get()) else self.textbox1.get(), alphabet_25_en, self.textbox6.get(),
                            self.textbox5.get())
                        transposition_matrix = [[''.join(['( ', c, ' )']) for c in filtered_key]] + transposition_matrix
                        self.table = CTkTable(self, values=transposition_matrix)
                        self.table.grid(row=2, column=2, rowspan=7, columnspan=2)
                    if self.segmented_button3.get() == "ADFGVX" and len(self.textbox5.get()) == 36:
                        _, transposition_matrix, filtered_key = encrypt_36(
                            self.textbox10.get() if len(self.textbox10.get()) > len(
                                self.textbox1.get()) else self.textbox1.get(), alphabet_36, self.textbox6.get(),
                            self.textbox5.get())
                        transposition_matrix = [[''.join(['( ', c, ' )']) for c in filtered_key]] + transposition_matrix
                        self.table = CTkTable(self, values=transposition_matrix)
                        self.table.grid(row=2, column=2, rowspan=7, columnspan=2)
                    else:
                        self.label7.configure(text="Invalid alphabet length!")

        # Random values button function
        def random_values_button():
            if self.textbox5.get() == '':
                if self.segmented_button1.get() == "CZ" and self.segmented_button3.get() == "ADFGX":
                    random_alphabet = ''
                    alphabet = alphabet_25_cz.copy()
                    for _ in range(len(alphabet)):
                        character = random.choice(alphabet)
                        alphabet.remove(character)
                        random_alphabet += character
                    self.textbox5.set('')
                    self.textbox5.set(random_alphabet)
                if self.segmented_button1.get() == "EN" and self.segmented_button3.get() == "ADFGX":
                    random_alphabet = ''
                    alphabet = alphabet_25_en.copy()
                    for _ in range(len(alphabet)):
                        character = random.choice(alphabet)
                        alphabet.remove(character)
                        random_alphabet += character
                    self.textbox5.set('')
                    self.textbox5.set(random_alphabet)
                if self.segmented_button3.get() == "ADFGVX":
                    random_alphabet = ''
                    alphabet = alphabet_36.copy()
                    for _ in range(len(alphabet)):
                        character = random.choice(alphabet)
                        alphabet.remove(character)
                        random_alphabet += character
                    self.textbox5.set('')
                    self.textbox5.set(random_alphabet)
            if self.textbox6.get() == '':
                random_key = random.choice(key_dictionary)
                self.textbox6.set('')
                self.textbox6.set(random_key)

        # Clear all button function
        def clear_all_button():
            self.textbox1.set('')
            self.textbox2.set('')
            self.textbox3.set('')
            self.textbox4.set('')
            self.segmented_button1.set("CZ")
            self.textbox5.set('')
            self.textbox6.set('')
            if hasattr(self, 'table'):
                self.table.destroy()
            self.segmented_button2.set("Substitution")
            self.segmented_button3.set("ADFGX")
            self.textbox7.set('')
            self.textbox8.set('')
            self.textbox9.set('')
            self.textbox10.set('')

        # Decrypt button function
        def decrypt_button():
            if self.textbox7.get() == '' and self.textbox4.get() == '':
                error_decrypt = "Enter text to decrypt!"
                error = 'Enter value!'
                self.textbox7.set('')
                self.textbox7.set(error_decrypt)
            if self.textbox5.get() == '':
                self.textbox5.set('')
                self.textbox5.set(error)
            if self.textbox6.get() == '':
                self.textbox6.set('')
                self.textbox6.set(error)
            else:
                if self.segmented_button1.get() == "CZ" and self.segmented_button3.get() == "ADFGX":
                    decrypt_25(
                        self.textbox4.get() if len(self.textbox4.get()) > len(
                            self.textbox7.get()) else self.textbox7.get(),
                        alphabet_25_cz, self.textbox6.get(), self.textbox5.get())
                if self.segmented_button1.get() == "EN" and self.segmented_button3.get() == "ADFGX":
                    decrypt_25(
                        self.textbox4.get() if len(self.textbox4.get()) > len(
                            self.textbox7.get()) else self.textbox7.get(),
                        alphabet_25_en, self.textbox6.get(), self.textbox5.get())
                if self.segmented_button3.get() == "ADFGVX":
                    decrypt_36(
                        self.textbox4.get() if len(self.textbox4.get()) > len(
                            self.textbox7.get()) else self.textbox7.get(),
                        alphabet_36, self.textbox6.get(), self.textbox5.get())

        # Encrypt plain text
        self.label1 = ctk.CTkLabel(self, text="Text to encrypt")
        self.label1.grid(row=0, column=0)
        self.textbox1 = tk.StringVar()
        self.textbox1.trace_add("write", self.update_textboxes_encrypt)
        self.entry1 = ctk.CTkEntry(self, textvariable=self.textbox1)
        self.entry1.grid(row=1, column=0)

        # Filtered text
        self.label2 = ctk.CTkLabel(self, text="Filtered text")
        self.label2.grid(row=2, column=0)
        self.textbox2 = tk.StringVar()
        self.textbox2.trace_add("write", self.update_textboxes_encrypt)
        self.entry2 = ctk.CTkEntry(self, textvariable=self.textbox2)
        self.entry2.grid(row=3, column=0)

        # Substituted text
        self.label3 = ctk.CTkLabel(self, text="Substituted text")
        self.label3.grid(row=4, column=0)
        self.textbox3 = tk.StringVar()
        self.textbox3.trace_add("write", self.update_textboxes_encrypt)
        self.entry3 = ctk.CTkEntry(self, textvariable=self.textbox3)
        self.entry3.grid(row=5, column=0)

        # Cipher text
        self.label4 = ctk.CTkLabel(self, text="Cipher text")
        self.label4.grid(row=6, column=0)
        self.textbox4 = tk.StringVar()
        self.textbox4.trace_add("write", self.update_textboxes_encrypt)
        self.entry4 = ctk.CTkEntry(self, textvariable=self.textbox4)
        self.entry4.grid(row=7, column=0)

        # Empty label 5
        self.label5 = ctk.CTkLabel(self, text=" ")
        self.label5.grid(row=8, column=0)

        # Encrypt button
        self.button1 = ctk.CTkButton(self, text="Encrypt", command=encrypt_button)
        self.button1.grid(row=9, column=0)

        # Language selection button
        self.segmented_button1 = ctk.CTkSegmentedButton(self, values=["CZ", "EN"])
        self.segmented_button1.grid(row=9, column=1)
        self.segmented_button1.set("CZ")

        # Empty label 6
        self.label6 = ctk.CTkLabel(self, text=" ")
        self.label6.grid(row=10, column=1)

        # Clear button
        self.button2 = ctk.CTkButton(self, text="Clear", command=clear_button)
        self.button2.grid(row=11, column=1)

        # Table alphabet
        self.label7 = ctk.CTkLabel(self, text="Table alphabet")
        self.label7.grid(row=0, column=2)
        self.textbox5 = tk.StringVar()
        self.textbox5.trace("w", self.update_label7)
        self.entry5 = ctk.CTkEntry(self, textvariable=self.textbox5)
        self.entry5.grid(row=1, column=2, sticky="ew")

        # Key
        self.label8 = ctk.CTkLabel(self, text="Key")
        self.label8.grid(row=0, column=3)
        self.textbox6 = tk.StringVar()
        self.textbox6.trace_add("write", self.update_textbox6)
        self.entry6 = ctk.CTkEntry(self, textvariable=self.textbox6)
        self.entry6.grid(row=1, column=3, sticky="ew")

        # Show table button
        self.button3 = ctk.CTkButton(self, text="Show table", command=show_table_button)
        self.button3.grid(row=9, column=2, columnspan=2, sticky="ew")

        # Table type selection button
        self.segmented_button2 = ctk.CTkSegmentedButton(self, values=["Substitution", "Transposition"])
        self.segmented_button2.grid(row=10, column=2, columnspan=2)
        self.segmented_button2.set("Substitution")

        # Random values button
        self.button4 = ctk.CTkButton(self, text="Random values", command=random_values_button)
        self.button4.grid(row=11, column=2, columnspan=2)

        # Cipher type selection button
        self.segmented_button3 = ctk.CTkSegmentedButton(self, values=["ADFGX", "ADFGVX"])
        self.segmented_button3.grid(row=9, column=4)
        self.segmented_button3.set("ADFGX")

        # Empty label 9
        self.label9 = ctk.CTkLabel(self, text=" ")
        self.label9.grid(row=10, column=4)

        # Clear all button
        self.button5 = ctk.CTkButton(self, text="Clear all", command=clear_all_button)
        self.button5.grid(row=11, column=4)

        # Decrypt cipher text
        self.label10 = ctk.CTkLabel(self, text="Text to decrypt")
        self.label10.grid(row=0, column=5)
        self.textbox7 = tk.StringVar()
        self.textbox7.trace_add("write", self.update_textboxes_decrypt)
        self.entry7 = ctk.CTkEntry(self, textvariable=self.textbox7)
        self.entry7.grid(row=1, column=5)

        # Detransposed text
        self.label11 = ctk.CTkLabel(self, text="Detransposed text")
        self.label11.grid(row=2, column=5)
        self.textbox8 = tk.StringVar()
        self.textbox8.trace_add("write", self.update_textboxes_decrypt)
        self.entry8 = ctk.CTkEntry(self, textvariable=self.textbox8)
        self.entry8.grid(row=3, column=5)

        # Unfiltered text
        self.label12 = ctk.CTkLabel(self, text="Unfiltered text")
        self.label12.grid(row=4, column=5)
        self.textbox9 = tk.StringVar()
        self.textbox9.trace_add("write", self.update_textboxes_decrypt)
        self.entry9 = ctk.CTkEntry(self, textvariable=self.textbox9)
        self.entry9.grid(row=5, column=5)

        # Plain text
        self.label13 = ctk.CTkLabel(self, text="Plain text")
        self.label13.grid(row=6, column=5)
        self.textbox10 = tk.StringVar()
        self.textbox10.trace_add("write", self.update_textboxes_decrypt)
        self.entry10 = ctk.CTkEntry(self, textvariable=self.textbox10)
        self.entry10.grid(row=7, column=5)

        # Empty label 14
        self.label14 = ctk.CTkLabel(self, text=" ")
        self.label14.grid(row=8, column=5)

        # Decrypt button
        self.button6 = ctk.CTkButton(self, text="Decrypt", command=decrypt_button)
        self.button6.grid(row=9, column=5)

    # Update label 7 function
    def update_label7(self, *args):
        alphabet_table = self.textbox5.get().upper()
        self.textbox5.set('')
        self.textbox5.set(alphabet_table)
        length = len(alphabet_table)
        if len(alphabet_table) != len(set(alphabet_table)):
            self.label7.configure(text="Two identical characters!")
        else:
            self.label7.configure(text=f"Table alphabet ({length})")

    # Update textboxes for encryption function
    def update_textboxes_encrypt(self, *args):
        textboxes = [self.textbox1, self.textbox2, self.textbox3, self.textbox4]
        for textbox in textboxes:
            textbox.set(textbox.get().upper())

    # Update textbox for key function
    def update_textbox6(self, *args):
        self.textbox6.set(self.textbox6.get().upper())

    # Update textboxes for decryption function
    def update_textboxes_decrypt(self, *args):
        textboxes = [self.textbox7, self.textbox8, self.textbox9, self.textbox10]
        for textbox in textboxes:
            textbox.set(textbox.get().upper())


# Main loop
if __name__ == "__main__":
    app = App()
    app.mainloop()

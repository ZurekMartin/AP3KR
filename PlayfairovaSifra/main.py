# Libraries import
import unicodedata
import customtkinter as ctk
from CTkTable import *

# Application settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


# Defining application class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Playfair Cipher")

        # Defining alphabets
        lower_case = list(map(chr, range(ord('a'), ord('z') + 1)))
        upper_case = list(map(chr, range(ord('A'), ord('Z') + 1)))
        digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        alphabet_25_cz = [chr(i) for i in range(ord('A'), ord('Z') + 1) if chr(i) != 'W']
        alphabet_25_en = [chr(i) for i in range(ord('A'), ord('Z') + 1) if chr(i) != 'J']
        alphabet_64 = lower_case + upper_case + digits + ['.'] + ['?']

        # Encrypt function for 25 characters
        def encrypt_25(plain_text, key, alphabet):
            cipher_text = ""
            self.textbox1.delete(0, "end")
            self.textbox1.insert(0, plain_text)
            filtered_plain_text = plain_text_filter_25(plain_text, alphabet)
            diagraphs = [filtered_plain_text[i:i + 2] for i in range(0, len(filtered_plain_text), 2)]
            self.textbox2.delete(0, "end")
            self.textbox2.insert(0, diagraphs)
            filtered_key = key_filter_25(key, alphabet)
            matrix = create_matrix_25(filtered_key, alphabet)
            i = 0
            while i < len(filtered_plain_text):
                character1, character2 = filtered_plain_text[i], filtered_plain_text[i + 1]
                row1, column1 = index_search_25(matrix, character1)
                row2, column2 = index_search_25(matrix, character2)
                if row1 == row2:
                    cipher_text += matrix[row1][(column1 + 1) % 5] + matrix[row2][(column2 + 1) % 5]
                elif column1 == column2:
                    cipher_text += matrix[(row1 + 1) % 5][column1] + matrix[(row2 + 1) % 5][column2]
                else:
                    cipher_text += matrix[row1][column2] + matrix[row2][column1]
                i += 2
            cipher_text = " ".join([cipher_text[i:i + 5] for i in range(0, len(cipher_text), 5)])
            self.textbox3.delete(0, "end")
            self.textbox3.insert(0, cipher_text)

        # Decrypt function for 25 characters
        def decrypt_25(cipher_text, key, alphabet):
            plain_text = ""
            cipher_text = cipher_text.replace(" ", "")
            self.textbox5.delete(0, "end")
            self.textbox5.insert(0, cipher_text)
            filtered_key = key_filter_25(key, alphabet)
            matrix = create_matrix_25(filtered_key, alphabet)
            i = 0
            while i < len(cipher_text):
                character1, character2 = cipher_text[i], cipher_text[i + 1]
                row1, column1 = index_search_25(matrix, character1)
                row2, column2 = index_search_25(matrix, character2)
                if row1 == row2:
                    plain_text += matrix[row1][(column1 - 1) % 5] + matrix[row2][(column2 - 1) % 5]
                elif column1 == column2:
                    plain_text += matrix[(row1 - 1) % 5][column1] + matrix[(row2 - 1) % 5][column2]
                else:
                    plain_text += matrix[row1][column2] + matrix[row2][column1]
                i += 2
            plain_text = plain_text.replace("Q", "")
            self.textbox6.delete(0, "end")
            self.textbox6.insert(0, plain_text)
            plain_text = plain_text.replace("XZEX", "0")
            plain_text = plain_text.replace("XONX", "1")
            plain_text = plain_text.replace("XTVX", "2")
            plain_text = plain_text.replace("XTHX", "3")
            plain_text = plain_text.replace("XFOX", "4")
            plain_text = plain_text.replace("XFIX", "5")
            plain_text = plain_text.replace("XSIX", "6")
            plain_text = plain_text.replace("XSEX", "7")
            plain_text = plain_text.replace("XEIX", "8")
            plain_text = plain_text.replace("XNIX", "9")
            plain_text = plain_text.replace("XSPACEX", " ")
            self.textbox7.delete(0, "end")
            self.textbox7.insert(0, plain_text)

        # Plain text filtering function for 25 characters
        def plain_text_filter_25(plain_text, alphabet):
            plain_text = plain_text.replace("0", "XZEX")
            plain_text = plain_text.replace("1", "XONX")
            plain_text = plain_text.replace("2", "XTVX")
            plain_text = plain_text.replace("3", "XTHX")
            plain_text = plain_text.replace("4", "XFOX")
            plain_text = plain_text.replace("5", "XFIX")
            plain_text = plain_text.replace("6", "XSIX")
            plain_text = plain_text.replace("7", "XSEX")
            plain_text = plain_text.replace("8", "XEIX")
            plain_text = plain_text.replace("9", "XNIX")
            unfiltered_plain_text = plain_text.upper()
            semifiltered_plain_text = ''.join(
                c for c in unicodedata.normalize('NFD', unfiltered_plain_text) if unicodedata.category(c) != 'Mn')
            filtered_plain_text = ''.join(e for e in semifiltered_plain_text if e.isalpha() or e == ' ')
            filtered_plain_text = filtered_plain_text.replace(" ", "XSPACEX")
            if len(filtered_plain_text) % 2 == 1:
                filtered_plain_text += "Q"
            if alphabet == alphabet_25_cz:
                filtered_plain_text = filtered_plain_text.replace("W", "V")
            else:
                filtered_plain_text = filtered_plain_text.replace("J", "I")
            return filtered_plain_text

        # Key filtering function for 25 characters
        def key_filter_25(key, alphabet):
            unfiltered_key = key.upper()
            semifiltered_key = ''.join(
                c for c in unicodedata.normalize('NFD', unfiltered_key) if unicodedata.category(c) != 'Mn')
            filtered_key = ''.join(e for e in semifiltered_key if e.isalpha())
            if alphabet == alphabet_25_cz:
                filtered_key = filtered_key.replace("W", "V")
            else:
                filtered_key = filtered_key.replace("J", "I")
            filtered_key = ''.join(sorted(set(filtered_key), key=filtered_key.index))
            return filtered_key

        # Create matrix function for 25 characters
        def create_matrix_25(key, alphabet):
            filtered_key = key_filter_25(key, alphabet)
            matrix = list(filtered_key)
            for character in alphabet:
                if character not in matrix:
                    matrix.append(character)
            matrix = [matrix[i:i + 5] for i in range(0, 25, 5)]
            return matrix

        # Index searching function for 25 characters
        def index_search_25(matrix, character):
            for i in range(5):
                for j in range(5):
                    if matrix[i][j] == character:
                        return i, j

        # Encrypt function for 64 characters
        def encrypt_64(plain_text, key, alphabet):
            cipher_text = ""
            self.textbox1.delete(0, "end")
            self.textbox1.insert(0, plain_text)
            filtered_plain_text = plain_text_filter_64(plain_text)
            diagraphs = [filtered_plain_text[i:i + 2] for i in range(0, len(filtered_plain_text), 2)]
            self.textbox2.delete(0, "end")
            self.textbox2.insert(0, diagraphs)
            filtered_key = key_filter_64(key)
            matrix = create_matrix_64(filtered_key, alphabet)
            i = 0
            while i < len(filtered_plain_text):
                character1, character2 = filtered_plain_text[i], filtered_plain_text[i + 1]
                row1, column1 = index_search_64(matrix, character1)
                row2, column2 = index_search_64(matrix, character2)
                if row1 == row2:
                    cipher_text += matrix[row1][(column1 + 1) % 8] + matrix[row2][(column2 + 1) % 8]
                elif column1 == column2:
                    cipher_text += matrix[(row1 + 1) % 8][column1] + matrix[(row2 + 1) % 8][column2]
                else:
                    cipher_text += matrix[row1][column2] + matrix[row2][column1]
                i += 2
            cipher_text = " ".join([cipher_text[i:i + 5] for i in range(0, len(cipher_text), 5)])
            self.textbox3.delete(0, "end")
            self.textbox3.insert(0, cipher_text)

        # Decrypt function for 64 characters
        def decrypt_64(cipher_text, key, alphabet):
            plain_text = ""
            cipher_text = cipher_text.replace(" ", "")
            self.textbox5.delete(0, "end")
            self.textbox5.insert(0, cipher_text)
            filtered_key = key_filter_64(key)
            matrix = create_matrix_64(filtered_key, alphabet)
            i = 0
            while i < len(cipher_text):
                character1, character2 = cipher_text[i], cipher_text[i + 1]
                row1, column1 = index_search_64(matrix, character1)
                row2, column2 = index_search_64(matrix, character2)
                if row1 == row2:
                    plain_text += matrix[row1][(column1 - 1) % 8] + matrix[row2][(column2 - 1) % 8]
                elif column1 == column2:
                    plain_text += matrix[(row1 - 1) % 8][column1] + matrix[(row2 - 1) % 8][column2]
                else:
                    plain_text += matrix[row1][column2] + matrix[row2][column1]
                i += 2
            plain_text = plain_text.replace("Q", "")
            self.textbox6.delete(0, "end")
            self.textbox6.insert(0, plain_text)
            plain_text = plain_text.replace("XSPACEX", " ")
            self.textbox7.delete(0, "end")
            self.textbox7.insert(0, plain_text)

        # Plain text filtering function for 64 characters
        def plain_text_filter_64(plain_text):
            unfiltered_plain_text = ''.join(
                c for c in unicodedata.normalize('NFD', plain_text) if unicodedata.category(c) != 'Mn')
            semifiltered_plain_text = ''.join(
                e for e in unfiltered_plain_text if e.isalnum() or e == ' ' or e == '.' or e == '?')
            filtered_plain_text = semifiltered_plain_text.replace(" ", "XSPACEX")
            if len(filtered_plain_text) % 2 == 1:
                filtered_plain_text += "Q"
            return filtered_plain_text

        # Key filtering function for 64 characters
        def key_filter_64(key):
            unfiltered_key = ''.join(c for c in unicodedata.normalize('NFD', key) if unicodedata.category(c) != 'Mn')
            semifiltered_key = ''.join(e for e in unfiltered_key if e.isalpha())
            filtered_key = ''.join(sorted(set(semifiltered_key), key=semifiltered_key.index))
            return filtered_key

        # Create matrix function for 64 characters
        def create_matrix_64(key, alphabet):
            filtered_key = key_filter_64(key)
            matrix = list(filtered_key)
            for character in alphabet:
                if character not in matrix:
                    matrix.append(character)
            matrix = [matrix[i:i + 8] for i in range(0, len(matrix) - 3, 8)]
            return matrix

        # Index searching function for 64 characters
        def index_search_64(matrix, character):
            for i in range(8):
                for j in range(8):
                    if matrix[i][j] == character:
                        return i, j

        # Encrypt button function
        def encrypt_button():
            if self.segmented_button1.get() == "CZ" and self.segmented_button2.get() == "5x5":
                if len(self.textbox7.get()) > len(self.textbox1.get()):
                    encrypt_25(self.textbox7.get(), self.textbox4.get(), alphabet_25_cz)
                else:
                    encrypt_25(self.textbox1.get(), self.textbox4.get(), alphabet_25_cz)
            if self.segmented_button1.get() == "EN" and self.segmented_button2.get() == "5x5":
                if len(self.textbox7.get()) > len(self.textbox1.get()):
                    encrypt_25(self.textbox7.get(), self.textbox4.get(), alphabet_25_en)
                else:
                    encrypt_25(self.textbox1.get(), self.textbox4.get(), alphabet_25_en)
            if self.segmented_button1.get() == "CZ" and self.segmented_button2.get() == "8x8":
                if len(self.textbox7.get()) > len(self.textbox1.get()):
                    encrypt_64(self.textbox7.get(), self.textbox4.get(), alphabet_64)
                else:
                    encrypt_64(self.textbox1.get(), self.textbox4.get(), alphabet_64)
            if self.segmented_button1.get() == "EN" and self.segmented_button2.get() == "8x8":
                if len(self.textbox7.get()) > len(self.textbox1.get()):
                    encrypt_64(self.textbox7.get(), self.textbox4.get(), alphabet_64)
                else:
                    encrypt_64(self.textbox1.get(), self.textbox4.get(), alphabet_64)

        # Show table button function
        def show_table_button():
            if self.segmented_button1.get() == "CZ" and self.segmented_button2.get() == "5x5":
                filtered_key = key_filter_25(self.textbox4.get(), alphabet_25_cz)
                matrix = create_matrix_25(filtered_key, alphabet_25_cz)
                if hasattr(self, 'table'):
                    self.table.destroy()
                self.table = CTkTable(master=self, values=matrix)
                self.table.grid(row=2, column=2, rowspan=5, sticky="ew")
            if self.segmented_button1.get() == "EN" and self.segmented_button2.get() == "5x5":
                filtered_key = key_filter_25(self.textbox4.get(), alphabet_25_en)
                matrix = create_matrix_25(filtered_key, alphabet_25_en)
                if hasattr(self, 'table'):
                    self.table.destroy()
                self.table = CTkTable(master=self, values=matrix)
                self.table.grid(row=2, column=2, rowspan=5, sticky="ew")
            if self.segmented_button1.get() == "CZ" and self.segmented_button2.get() == "8x8":
                filtered_key = key_filter_64(self.textbox4.get())
                matrix = create_matrix_64(filtered_key, alphabet_64)
                if hasattr(self, 'table'):
                    self.table.destroy()
                self.table = CTkTable(master=self, values=matrix)
                self.table.grid(row=2, column=2, rowspan=5, sticky="ew")
            if self.segmented_button1.get() == "EN" and self.segmented_button2.get() == "8x8":
                filtered_key = key_filter_64(self.textbox4.get())
                matrix = create_matrix_64(filtered_key, alphabet_64)
                if hasattr(self, 'table'):
                    self.table.destroy()
                self.table = CTkTable(master=self, values=matrix)
                self.table.grid(row=2, column=2, rowspan=5, sticky="ew")

        # Clear button function
        def clear_button():
            self.textbox1.delete(0, "end")
            self.textbox2.delete(0, "end")
            self.textbox3.delete(0, "end")
            self.textbox5.delete(0, "end")
            self.textbox6.delete(0, "end")
            self.textbox7.delete(0, "end")

        # Clear all button function
        def clear_all_button():
            self.textbox1.delete(0, "end")
            self.textbox2.delete(0, "end")
            self.textbox3.delete(0, "end")
            self.textbox4.delete(0, "end")
            if hasattr(self, 'table'):
                self.table.destroy()
            self.segmented_button1.set("CZ")
            self.segmented_button2.set("5x5")
            self.textbox5.delete(0, "end")
            self.textbox6.delete(0, "end")
            self.textbox7.delete(0, "end")

        # Decrypt button function
        def decrypt_button():
            if self.segmented_button1.get() == "CZ" and self.segmented_button2.get() == "5x5":
                if len(self.textbox3.get()) > len(self.textbox5.get()):
                    decrypt_25(self.textbox3.get(), self.textbox4.get(), alphabet_25_cz)
                else:
                    decrypt_25(self.textbox5.get(), self.textbox4.get(), alphabet_25_cz)
            if self.segmented_button1.get() == "EN" and self.segmented_button2.get() == "5x5":
                if len(self.textbox3.get()) > len(self.textbox5.get()):
                    decrypt_25(self.textbox3.get(), self.textbox4.get(), alphabet_25_en)
                else:
                    decrypt_25(self.textbox5.get(), self.textbox4.get(), alphabet_25_en)
            if self.segmented_button1.get() == "CZ" and self.segmented_button2.get() == "8x8":
                if len(self.textbox3.get()) > len(self.textbox5.get()):
                    decrypt_64(self.textbox3.get(), self.textbox4.get(), alphabet_64)
                else:
                    decrypt_64(self.textbox5.get(), self.textbox4.get(), alphabet_64)
            if self.segmented_button1.get() == "EN" and self.segmented_button2.get() == "8x8":
                if len(self.textbox3.get()) > len(self.textbox5.get()):
                    decrypt_64(self.textbox3.get(), self.textbox4.get(), alphabet_64)
                else:
                    decrypt_64(self.textbox5.get(), self.textbox4.get(), alphabet_64)

        # Encrypt plain text
        self.label1 = ctk.CTkLabel(self, text="Text to encrypt")
        self.label1.grid(row=0, column=0)
        self.textbox1 = ctk.CTkEntry(self)
        self.textbox1.grid(row=1, column=0)

        # Filtered diagraphs
        self.label2 = ctk.CTkLabel(self, text="Diagraphs")
        self.label2.grid(row=2, column=0)
        self.textbox2 = ctk.CTkEntry(self)
        self.textbox2.grid(row=3, column=0)

        # Cipher text
        self.label3 = ctk.CTkLabel(self, text="Cipher text")
        self.label3.grid(row=4, column=0)
        self.textbox3 = ctk.CTkEntry(self)
        self.textbox3.grid(row=5, column=0)

        # Empty label4
        self.label4 = ctk.CTkLabel(self, text=" ")
        self.label4.grid(row=6, column=0)

        # Encrypt button
        self.button1 = ctk.CTkButton(self, text="Encrypt", command=encrypt_button)
        self.button1.grid(row=7, column=0)

        # Key
        self.label5 = ctk.CTkLabel(self, text="Key")
        self.label5.grid(row=0, column=2)
        self.textbox4 = ctk.CTkEntry(self)
        self.textbox4.grid(row=1, column=2, sticky="ew")

        # Language selection button
        self.segmented_button1 = ctk.CTkSegmentedButton(self, values=["CZ", "EN"])
        self.segmented_button1.grid(row=7, column=1)
        self.segmented_button1.set("CZ")

        # Show table button
        self.button2 = ctk.CTkButton(self, text="Show table", command=show_table_button)
        self.button2.grid(row=7, column=2, sticky="ew")

        # Table size selection button
        self.segmented_button2 = ctk.CTkSegmentedButton(self, values=["5x5", "8x8"])
        self.segmented_button2.grid(row=7, column=3)
        self.segmented_button2.set("5x5")

        # Empty label6
        self.label6 = ctk.CTkLabel(self, text=" ")
        self.label6.grid(row=8, column=1)

        # Clear button
        self.button3 = ctk.CTkButton(self, text="Clear", command=clear_button)
        self.button3.grid(row=9, column=1)

        # Empty label7
        self.label7 = ctk.CTkLabel(self, text=" ")
        self.label7.grid(row=8, column=3)

        # Clear all button
        self.button4 = ctk.CTkButton(self, text="Clear all", command=clear_all_button)
        self.button4.grid(row=9, column=3)

        # Decrypt cipher text
        self.label8 = ctk.CTkLabel(self, text="Text to decrypt")
        self.label8.grid(row=0, column=4)
        self.textbox5 = ctk.CTkEntry(self)
        self.textbox5.grid(row=1, column=4)

        # Unfiltered text
        self.label9 = ctk.CTkLabel(self, text="Unfiltered text")
        self.label9.grid(row=2, column=4)
        self.textbox6 = ctk.CTkEntry(self)
        self.textbox6.grid(row=3, column=4)

        # Plain text
        self.label10 = ctk.CTkLabel(self, text="Plain text")
        self.label10.grid(row=4, column=4)
        self.textbox7 = ctk.CTkEntry(self)
        self.textbox7.grid(row=5, column=4)

        # Empty label11
        self.label11 = ctk.CTkLabel(self, text=" ")
        self.label11.grid(row=6, column=4)

        # Decrypt button
        self.button5 = ctk.CTkButton(self, text="Decrypt", command=decrypt_button)
        self.button5.grid(row=7, column=4)


# Main loop
if __name__ == "__main__":
    app = App()
    app.mainloop()

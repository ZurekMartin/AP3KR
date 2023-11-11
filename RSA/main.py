# Libraries import
import math
import random
import unicodedata
import tkinter as tk
import customtkinter as ctk

# Application settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


# Defining application class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("RSA")
        self.resizable(False, False)

        # Encrypt function
        def encrypt(plain_text, n, e, size):
            n = int(n)
            e = int(e)
            block_size = size // 16
            filtered_plain_text = plain_text_filter(plain_text)
            binary_plain_text = text_to_binary(filtered_plain_text)
            padding_length = block_size - (len(binary_plain_text) % block_size)
            binary_plain_text += '0' * (padding_length - 8)
            binary_plain_text += format(padding_length, '08b')
            plain_block = [binary_plain_text[i:i + block_size] for i in range(0, len(binary_plain_text), block_size)]
            cipher_block = [str(pow(int(block, 2), e, n)).zfill(len(str(n))) for block in plain_block]
            cipher_text = ''.join(cipher_block)
            binary_cipher_text = text_to_binary(cipher_text)
            binary_cipher_text = ' '.join([binary_cipher_text[i:i + 8] for i in range(0, len(binary_cipher_text), 8)])
            return cipher_text, binary_cipher_text

        # Decrypt function
        def decrypt(cipher_text, n, d, size):
            n = int(n)
            d = int(d)
            block_size = str(size // 16)
            modulus_length = len(str(n))
            cipher_block = [cipher_text[i:i + modulus_length] for i in range(0, len(cipher_text), modulus_length)]
            plain_block = [format(pow(int(block), d, n), '0' + block_size + 'b') for block in cipher_block]
            binary_plain_text = ''.join(plain_block)
            binary_padding_length = binary_plain_text[-8:]
            padding_length = int(binary_padding_length, 2)
            binary_plain_text = binary_plain_text[:-padding_length]
            plain_text = binary_to_text(binary_plain_text)
            binary_plain_text = ' '.join([binary_plain_text[i:i + 8] for i in range(0, len(binary_plain_text), 8)])
            return plain_text, binary_plain_text
            
        # Plain text filtering function
        def plain_text_filter(plain_text):
            unfiltered_plain_text = ''.join(
                c for c in unicodedata.normalize('NFD', plain_text) if unicodedata.category(c) != 'Mn')
            filtered_plain_text = ''.join(c if 0 <= ord(c) <= 255 else '' for c in unfiltered_plain_text)
            return filtered_plain_text

        # Text to binary function
        def text_to_binary(text):
            binary_text = ''.join(format(ord(character), '08b') for character in text)
            return binary_text

        # Binary to text function
        def binary_to_text(binary_text):
            text = ''.join([chr(int(binary_text[i:i + 8], 2)) for i in range(0, len(binary_text), 8)])
            return text

        # Key generating function
        def generate_key(size):
            p = generate_prime_number(size // 2)
            q = generate_prime_number(size // 2)
            while p == q:
                q = generate_prime_number(size // 2)
            n = p * q
            phi = (p - 1) * (q - 1)
            e = 65537
            g = math.gcd(e, phi)
            while g != 1:
                e = random.randrange(1, phi)
                g = math.gcd(e, phi)
            d = pow(e, -1, phi)
            return e, p, n, q, d

        # Prime number generating function
        def generate_prime_number(size):
            while True:
                minimal_number = pow(2, size - 1)
                maximal_number = pow(2, size)
                number = random.randrange(minimal_number, maximal_number) | 1
                if prime_number_check(number):
                    return number

        # Prime number checking function
        def prime_number_check(n):
            if n in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
                return True
            if n < 2 or n % 2 == 0:
                return False
            s = 0
            d = n - 1
            while d % 2 == 0:
                d //= 2
                s += 1
            number_of_attempts = 128
            for _ in range(number_of_attempts):
                a = random.randrange(2, n - 1)
                x = pow(a, d, n)
                if x == 1 or x == n - 1:
                    continue
                for _ in range(s - 1):
                    x = pow(x, 2, n)
                    if x == n - 1:
                        break
                else:
                    return False
            return True

        # Encrypt button function
        def encrypt_button():
            size_mapping = {
                "1024 bits": 1024,
                "2048 bits": 2048,
                "3072 bits": 3072,
            }
            size = size_mapping.get(self.segmented_button1.get())
            textbox1_value = self.textbox1.get()
            textbox5_value = self.textbox5.get()
            textbox7_value = self.textbox7.get()
            textbox9_value = self.textbox9.get()
            if not textbox1_value and not textbox5_value and not textbox7_value and not textbox9_value:
                error_encrypt = 'Enter text to encrypt!'
                error = 'Enter value!'
                if not textbox1_value:
                    self.update_textbox(self.textbox1, error_encrypt)
                if not textbox5_value:
                    self.update_textbox_var(self.textbox5, error)
                if not textbox7_value:
                    self.update_textbox_var(self.textbox7, error)
                if not textbox9_value:
                    self.update_textbox_var(self.textbox9, error)
            else:
                plain_text = self.textbox8.get() if len(self.textbox8.get()) > len(textbox1_value) else textbox1_value
                (cipher_text, binary_text) = encrypt(plain_text, self.textbox7.get(), self.textbox3.get(), size)
                self.update_textbox(self.textbox1, plain_text)
                self.update_textbox(self.textbox4, cipher_text)
                self.update_textbox(self.textbox6, binary_text)

        # Clear button function
        def clear_button():
            self.update_textbox(self.textbox1, '')
            self.update_textbox(self.textbox4, '')
            self.update_textbox(self.textbox6, '')
            self.update_textbox(self.textbox8, '')
            self.update_textbox(self.textbox10, '')

        # Random values button function
        def random_values_button():
            size_mapping = {
                "1024 bits": 1024,
                "2048 bits": 2048,
                "3072 bits": 3072,
            }
            size = size_mapping.get(self.segmented_button1.get())
            (e, p, n, q, d) = generate_key(size)
            temporary_n = str(n)[:6]
            temporary_e = str(e)[:6]
            temporary_d = str(d)[:6]
            if len(temporary_e) < 6:
                public_key = temporary_n + '..., ' + temporary_e
            else:
                public_key = temporary_n + '..., ' + temporary_e + '...'
            private_key = temporary_n + '..., ' + temporary_d + '...'
            self.update_textbox(self.textbox2, public_key)
            self.update_textbox_var(self.textbox3, e)
            self.update_textbox_var(self.textbox5, p)
            self.update_textbox_var(self.textbox7, n)
            self.update_textbox_var(self.textbox9, q)
            self.update_textbox(self.textbox11, private_key)
            self.update_textbox_var(self.textbox12, d)

        # Clear all button function
        def clear_all_button():
            self.update_textbox(self.textbox1, '')
            self.update_textbox(self.textbox2, '')
            self.update_textbox_var(self.textbox3, '')
            self.update_textbox(self.textbox4, '')
            self.update_textbox_var(self.textbox5, '')
            self.update_textbox(self.textbox6, '')
            self.segmented_button1.set("2048 bits")
            self.update_textbox_var(self.textbox7, '')
            self.update_textbox(self.textbox8, '')
            self.update_textbox_var(self.textbox9, '')
            self.update_textbox(self.textbox10, '')
            self.update_textbox(self.textbox11, '')
            self.update_textbox_var(self.textbox12, '')

        # Decrypt button function
        def decrypt_button():
            size_mapping = {
                "1024 bits": 1024,
                "2048 bits": 2048,
                "3072 bits": 3072,
            }
            size = size_mapping.get(self.segmented_button1.get())
            textbox5_value = self.textbox5.get()
            textbox7_value = self.textbox7.get()
            textbox9_value = self.textbox9.get()
            textbox10_value = self.textbox10.get()
            if not textbox5_value and not textbox7_value and not textbox9_value and not textbox10_value:
                error = 'Enter value!'
                error_decrypt = "Enter text to decrypt!"
                if not textbox5_value:
                    self.update_textbox_var(self.textbox5, error)
                if not textbox7_value:
                    self.update_textbox_var(self.textbox7, error)
                if not textbox9_value:
                    self.update_textbox_var(self.textbox9, error)
                if not textbox10_value:
                    self.update_textbox(self.textbox10, error_decrypt)
            else:
                cipher_text = self.textbox4.get() if len(self.textbox4.get()) > len(
                    textbox10_value) else textbox10_value
                (plain_text, binary_text) = decrypt(cipher_text, self.textbox7.get(), self.textbox12.get(), size)
                self.update_textbox(self.textbox10, cipher_text)
                self.update_textbox(self.textbox8, plain_text)
                self.update_textbox(self.textbox6, binary_text)

        # Encrypt plain text
        self.label1 = ctk.CTkLabel(self, text="Text to encrypt")
        self.label1.grid(row=0, column=0)
        self.textbox1 = ctk.CTkEntry(self)
        self.textbox1.grid(row=1, column=0)

        # Public key
        self.label2 = ctk.CTkLabel(self, text="Public key ( n, e )")
        self.label2.grid(row=2, column=0)
        self.textbox2 = ctk.CTkEntry(self)
        self.textbox2.grid(row=3, column=0)

        # e
        self.label3 = ctk.CTkLabel(self, text="Public exponent ( e )")
        self.label3.grid(row=4, column=0)
        self.textbox3 = ctk.StringVar()
        self.textbox3.trace("w", lambda *args: self.update_empty_label(self.textbox3, self.label4))
        self.entry1 = ctk.CTkEntry(self, textvariable=self.textbox3)
        self.entry1.grid(row=5, column=0)

        # Empty label 4
        self.label4 = ctk.CTkLabel(self, text="")
        self.label4.grid(row=6, column=0)

        # Encrypt button
        self.button1 = ctk.CTkButton(self, text="Encrypt", command=encrypt_button)
        self.button1.grid(row=7, column=0)

        # Cipher text
        self.label5 = ctk.CTkLabel(self, text="Cipher text")
        self.label5.grid(row=0, column=1)
        self.textbox4 = ctk.CTkEntry(self)
        self.textbox4.grid(row=1, column=1)

        # p
        self.label6 = ctk.CTkLabel(self, text="Prime number ( p )")
        self.label6.grid(row=4, column=1)
        self.textbox5 = ctk.StringVar()
        self.textbox5.trace("w", lambda *args: self.update_empty_label(self.textbox5, self.label7))
        self.entry2 = ctk.CTkEntry(self, textvariable=self.textbox5)
        self.entry2.grid(row=5, column=1)

        # Empty label 7
        self.label7 = ctk.CTkLabel(self, text="")
        self.label7.grid(row=6, column=1)

        # Clear button
        self.button2 = ctk.CTkButton(self, text="Clear", width=86, command=clear_button)
        self.button2.grid(row=7, column=1)

        # Binary output
        self.label8 = ctk.CTkLabel(self, text="Binary output")
        self.label8.grid(row=0, column=1, columnspan=3)
        self.textbox6 = ctk.CTkEntry(self)
        self.textbox6.grid(row=1, column=1, columnspan=3)

        # Key size selection button
        self.label9 = ctk.CTkLabel(self, text="Key size")
        self.label9.grid(row=2, column=1, columnspan=3)
        self.segmented_button1 = ctk.CTkSegmentedButton(self, values=["1024 bits", "2048 bits", "3072 bits"])
        self.segmented_button1.grid(row=3, column=1, columnspan=3)
        self.segmented_button1.set("2048 bits")

        # n
        self.label10 = ctk.CTkLabel(self, text="Modulus ( n )")
        self.label10.grid(row=4, column=2)
        self.textbox7 = ctk.StringVar()
        self.textbox7.trace("w", lambda *args: self.update_empty_label(self.textbox7, self.label11))
        self.entry3 = ctk.CTkEntry(self, textvariable=self.textbox7)
        self.entry3.grid(row=5, column=2)

        # Empty label 11
        self.label11 = ctk.CTkLabel(self, text="")
        self.label11.grid(row=6, column=2)

        # Random values button
        self.button3 = ctk.CTkButton(self, text="Random values", command=random_values_button)
        self.button3.grid(row=7, column=2)

        # Plain text
        self.label12 = ctk.CTkLabel(self, text="Plain text")
        self.label12.grid(row=0, column=3)
        self.textbox8 = ctk.CTkEntry(self)
        self.textbox8.grid(row=1, column=3)

        # q
        self.label13 = ctk.CTkLabel(self, text="Prime number ( q )")
        self.label13.grid(row=4, column=3)
        self.textbox9 = ctk.StringVar()
        self.textbox9.trace("w", lambda *args: self.update_empty_label(self.textbox9, self.label14))
        self.entry4 = ctk.CTkEntry(self, textvariable=self.textbox9)
        self.entry4.grid(row=5, column=3)

        # Empty label 14
        self.label14 = ctk.CTkLabel(self, text="")
        self.label14.grid(row=6, column=3)

        # Clear all button
        self.button4 = ctk.CTkButton(self, text="Clear all", width=86, command=clear_all_button)
        self.button4.grid(row=7, column=3)

        # Decrypt cipher text
        self.label15 = ctk.CTkLabel(self, text="Text to decrypt")
        self.label15.grid(row=0, column=4)
        self.textbox10 = ctk.CTkEntry(self)
        self.textbox10.grid(row=1, column=4)

        # Private key
        self.label16 = ctk.CTkLabel(self, text="Private key ( n, d )")
        self.label16.grid(row=2, column=4)
        self.textbox11 = ctk.CTkEntry(self)
        self.textbox11.grid(row=3, column=4)

        # d
        self.label17 = ctk.CTkLabel(self, text="Private exponent ( d )")
        self.label17.grid(row=4, column=4)
        self.textbox12 = tk.StringVar()
        self.textbox12.trace("w", lambda *args: self.update_empty_label(self.textbox12, self.label18))
        self.entry5 = ctk.CTkEntry(self, textvariable=self.textbox12)
        self.entry5.grid(row=5, column=4)

        # Empty label 18
        self.label18 = ctk.CTkLabel(self, text="")
        self.label18.grid(row=6, column=4)

        # Decrypt button
        self.button5 = ctk.CTkButton(self, text="Decrypt", command=decrypt_button)
        self.button5.grid(row=7, column=4)

    # Update label function
    def update_empty_label(self, textbox, label):
        decimal_text = textbox.get()
        try:
            binary_text = bin(int(decimal_text))
            binary_length = len(binary_text) - 2
            self.update_label(label, f"Length: {binary_length} bits")
        except ValueError:
            self.update_label(label, "")

    # Update textbox function
    def update_textbox(self, textbox, value):
        textbox.delete(0, tk.END)
        textbox.insert(0, value)

    # Update textbox var function
    def update_textbox_var(self, textbox, value):
        textbox.set('')
        textbox.set(value)

    # Update label function
    def update_label(self, label, text):
        label.configure(text=text)


# Main loop
if __name__ == "__main__":
    app = App()
    app.mainloop()

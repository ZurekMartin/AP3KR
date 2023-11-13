# Libraries import
import os
import math
import base64
import random
import os.path
import hashlib
import zipfile
import customtkinter as ctk
from datetime import datetime
from tkinter import filedialog

# Application settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


# Defining application class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Digital signature")
        self.resizable(False, False)

        # Encrypt function
        def encrypt(hex_string, n, e, size):
            n = int(n)
            e = int(e)
            block_size = size // 16
            binary_plain_text = bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4)
            padding_length = block_size - (len(binary_plain_text) % block_size)
            binary_plain_text += '0' * (padding_length - 8)
            binary_plain_text += format(padding_length, '08b')
            plain_block = [binary_plain_text[i:i + block_size] for i in range(0, len(binary_plain_text), block_size)]
            cipher_block = [str(pow(int(block, 2), e, n)).zfill(len(str(n))) for block in plain_block]
            cipher_text = ''.join(cipher_block)
            return cipher_text

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
            hex_string = hex(int(binary_plain_text, 2))[2:].zfill(len(binary_plain_text) // 4)
            return hex_string

        # Key generating function
        def generate_key():
            number_of_attempts = 3072
            p = generate_prime_number(2048 // 2)
            q = generate_prime_number(2048 // 2)
            for _ in range(number_of_attempts):
                if p != q:
                    break
                q = generate_prime_number(2048 // 2)
            else:
                raise Exception('Prime numbers p and q are equal')
            n = p * q
            phi = (p - 1) * (q - 1)
            e = 65537
            g = math.gcd(e, phi)
            for _ in range(number_of_attempts):
                if g == 1:
                    break
                e = random.randrange(1, phi)
                g = math.gcd(e, phi)
            else:
                raise Exception('GCD of e and phi is not 1')
            d = pow(e, -1, phi)
            return e, p, n, q, d

        # Prime number generating function
        def generate_prime_number(size):
            number_of_attempts = 3072
            for _ in range(number_of_attempts):
                minimal_number = pow(2, size - 1)
                maximal_number = pow(2, size)
                number = random.randrange(minimal_number, maximal_number) | 1
                if prime_number_check(number):
                    return number
            raise Exception('Prime number not found within maximum iterations')

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

        # Function for creating keypair
        def create_keypair():
            e, p, n, q, d = generate_key()
            directory_path = filedialog.askdirectory(title="Select directory for saving keys")
            public_key_path = os.path.join(directory_path, 'public_key.pub')
            private_key_path = os.path.join(directory_path, 'private_key.priv')
            with open(public_key_path, 'w') as public_key_file:
                public_key_file.write('RSA ' + base64.b64encode((str(e) + ' ' + str(n)).encode()).decode())
            with open(private_key_path, 'w') as private_key_file:
                private_key_file.write('RSA ' + base64.b64encode((str(d) + ' ' + str(n)).encode()).decode())

        # Function for getting file
        def get_file():
            file_path = filedialog.askopenfilename(title="Select file")
            file_name = file_path.split('/')[-1]
            file_extension = file_name.split('.')[-1]
            file_size = os.path.getsize(file_path)
            date_of_creation = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
            date_of_modification = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
            return file_path, file_name, file_extension, file_size, date_of_creation, date_of_modification

        # Function for getting hash
        def get_hash(file):
            sha3_512_hash = hashlib.sha3_512()
            with open(file, "rb") as f:
                for byte_block in iter(lambda: f.read(2048), b""):
                    sha3_512_hash.update(byte_block)
            hash_content = sha3_512_hash.hexdigest()
            return hash_content

        # Function for signing file
        def sign_file(file_path):
            hash_content = get_hash(file_path)
            private_key_path = filedialog.askopenfilename(title="Select private key")
            with open(private_key_path, 'r') as private_file:  # open private key in read mode
                private_key = private_file.read()
                d, n = [int(i) for i in base64.b64decode(private_key.split(' ')[1]).decode().split()]
            signature = encrypt(hash_content, n, d, 2048)
            directory_path = filedialog.askdirectory(title="Select directory for saving compressed file")
            signed_file_directory = os.path.join(directory_path,
                                                 'digital_signature')  # create directory for saving signed file
            if os.path.exists(signed_file_directory):  # check if directory exists
                for file in os.listdir(signed_file_directory):  # iterate through all files in directory
                    os.remove(os.path.join(signed_file_directory, file))  # remove all files in directory
            else:
                os.makedirs(signed_file_directory, exist_ok=True)  # if directory doesn't exist, create it
            with open(file_path, 'rb') as source_file:  # open file in read binary mode
                with open(os.path.join(signed_file_directory, os.path.basename(file_path)),
                          'wb') as destination_file:  # open file in write binary mode
                    destination_file.write(source_file.read())  # write file content to destination file
            signed_file_path = os.path.join(signed_file_directory,
                                            os.path.splitext(os.path.basename(file_path))[
                                                0] + '.sign')  # create path for saving signed file
            with open(signed_file_path, 'w') as signed_file:  # open signed file in write mode
                signed_file.write('RSA_SHA3-512 ' + base64.b64encode(signature.encode()).decode())
            compressed_file_path = os.path.join(directory_path,
                                                'digital_signature.zip')  # create path for saving compressed file
            with zipfile.ZipFile(compressed_file_path, 'w',
                                 zipfile.ZIP_DEFLATED) as compressed_file:  # open compressed file in write mode
                for root, dirs, files in os.walk(signed_file_directory):  # iterate through all files in directory
                    for file in files:  # iterate through all files in directory
                        compressed_file.write(os.path.join(root, file),
                                              arcname=os.path.relpath(os.path.join(root, file),
                                                                      signed_file_directory))
                        # add file to compressed file

        # Function for verifying signature
        def verify_signature(compressed_file_path):
            directory = os.path.dirname(compressed_file_path)
            new_folder_path = os.path.join(directory, 'uncompressed_file')  # create path for saving uncompressed file
            if os.path.exists(new_folder_path):  # check if directory exists
                for file in os.listdir(new_folder_path):  # iterate through all files in directory
                    os.remove(os.path.join(new_folder_path, file))  # remove all files in directory
            else:
                os.makedirs(new_folder_path)  # if directory doesn't exist, create it
            with zipfile.ZipFile(compressed_file_path, 'r') as compressed_file:  # open compressed file in read mode
                compressed_file.extractall(
                    path=new_folder_path)  # extract all files from compressed file to directory uncompressed_file
                file_list = compressed_file.namelist()  # get list of all files in compressed file
                file_path = [os.path.join(new_folder_path, file) for file in file_list if not file.endswith('.sign')][
                    0]  # get path of file without .sign extension
                signed_file_path = \
                    [os.path.join(new_folder_path, file) for file in file_list if file.endswith('.sign')][
                        0]  # get path of file with .sign extension
            public_key_path = filedialog.askopenfilename(title="Select public key")
            with open(public_key_path, 'r') as public_file:  # open public key in read mode
                public_key = public_file.read()
                e, n = [int(i) for i in base64.b64decode(public_key.split(' ')[1]).decode().split()]
            hash_content = get_hash(file_path)
            with open(signed_file_path, 'r') as signed_file:  # open signed file in read mode
                signature = base64.b64decode(signed_file.read().split(' ')[1]).decode()
            decrypted_signature = decrypt(signature, n, e, 2048)
            if hash_content == decrypted_signature:
                verification_result = 'Verification successful!'
                return verification_result
            else:
                verification_result = 'Verification failed!'
                return verification_result

        # Select file button
        def select_file_button():
            clear_button()
            file_path, file_name, file_extension, file_size, date_of_creation, date_of_modification = get_file()
            self.file_info_label.configure(
                text=f"File path: {file_path}\n" + f"File name: {file_name}\n" + f"File extension: {file_extension}\n" +
                     f"File size: {file_size} bytes\n" + f"Date of creation: {date_of_creation}\n" +
                     f"Date of modification: {date_of_modification}")

        # Sign file button
        def sign_file_button():
            label_text = self.file_info_label.cget("text")
            file_path = label_text.split("\n")[0][len("File path: "):]
            sign_file(file_path)
            self.function_result_label.configure(text="File signed successfully!")

        # Random values button
        def random_values_button():
            create_keypair()

        # Clear button
        def clear_button():
            self.file_info_label.configure(text="File info")
            self.function_result_label.configure(text="Function result")
            self.compressed_file_info_label.configure(text="Compressed file info")

        # Select compressed file button
        def select_compressed_file_button():
            clear_button()
            compressed_file_path, file_name, file_extension, file_size, date_of_creation, date_of_modification = (
                get_file())
            self.compressed_file_info_label.configure(
                text=f"File path: {compressed_file_path}\n" + f"File name: {file_name}\n" +
                     f"File extension: {file_extension}\n" + f"File size: {file_size} bytes\n" +
                     f"Date of creation: {date_of_creation}\n" + f"Date of modification: {date_of_modification}")

        # Verify signature button
        def verify_signature_button():
            label_text = self.compressed_file_info_label.cget("text")
            compressed_file_path = label_text.split("\n")[0][len("File path: "):]
            verification_result = verify_signature(compressed_file_path)
            self.function_result_label.configure(text=verification_result)

        # Select file button
        self.select_file_button = ctk.CTkButton(self, text="Select file", command=select_file_button)
        self.select_file_button.grid(row=0, column=0, padx=16, pady=16)

        # File info label
        self.file_info_label = ctk.CTkLabel(self, text="File info")
        self.file_info_label.grid(row=1, column=0)

        # Sign file button
        self.sign_file_button = ctk.CTkButton(self, text="Sign file", command=sign_file_button)
        self.sign_file_button.grid(row=2, column=0, padx=16, pady=16)

        # Random values button
        self.random_values_button = ctk.CTkButton(self, text="Random values", command=random_values_button)
        self.random_values_button.grid(row=0, column=1, padx=16, pady=16)

        # Function result label
        self.function_result_label = ctk.CTkLabel(self, text="Function result")
        self.function_result_label.grid(row=1, column=1)

        # Clear button
        self.clear_button = ctk.CTkButton(self, text="Clear", width=86, command=clear_button)
        self.clear_button.grid(row=2, column=1, padx=16, pady=16)

        # Select compressed file button
        self.select_compressed_file_button = ctk.CTkButton(self, text="Select compressed file",
                                                           command=select_compressed_file_button)
        self.select_compressed_file_button.grid(row=0, column=2, padx=16, pady=16)

        # Compressed file info label
        self.compressed_file_info_label = ctk.CTkLabel(self, text="Compressed file info")
        self.compressed_file_info_label.grid(row=1, column=2)

        # Verify signature button
        self.verify_signature_button = ctk.CTkButton(self, text="Verify signature", command=verify_signature_button)
        self.verify_signature_button.grid(row=2, column=2, padx=16, pady=16)


# Main loop
if __name__ == "__main__":
    app = App()
    app.mainloop()

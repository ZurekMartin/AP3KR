# Libraries import
import os
import unicodedata
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk, ExifTags

# Application settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


# Defining application class
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Steganography")
        self.resizable(False, False)

        # Encode function
        def encode(image, message):
            encoded_image = image.copy()
            width, height = encoded_image.size
            unfiltered_message = ''.join(
                c for c in unicodedata.normalize('NFD', message) if unicodedata.category(c) != 'Mn')
            filtered_message = ''.join(c if 0 <= ord(c) <= 255 else '' for c in unfiltered_message)
            binary_filtered_message = ''.join(format(ord(ch), '08b') for ch in filtered_message)
            binary_message_length = len(binary_filtered_message)
            binary_message_length = format(binary_message_length, '024b')
            binary_message = binary_message_length + binary_filtered_message
            index = 0
            for row in range(height):
                for col in range(width):
                    r, g, b = encoded_image.getpixel((col, row))
                    if index < len(binary_message):
                        r = (r & 0xFE) | int(binary_message[index])
                        index += 1
                    if index < len(binary_message):
                        g = (g & 0xFE) | int(binary_message[index])
                        index += 1
                    if index < len(binary_message):
                        b = (b & 0xFE) | int(binary_message[index])
                        index += 1
                    encoded_image.putpixel((col, row), (r, g, b))
                    if index >= len(binary_message):
                        break
                if index >= len(binary_message):
                    break
            return filtered_message, encoded_image

        # Decode function
        def decode(encoded_image):
            width, height = encoded_image.size
            binary_message = ''
            message_length = 0
            for row in range(height):
                for col in range(width):
                    r, g, b = encoded_image.getpixel((col, row))
                    binary_message += format(r & 0x01, '01b')
                    binary_message += format(g & 0x01, '01b')
                    binary_message += format(b & 0x01, '01b')
                    if len(binary_message) >= 24:
                        binary_message_length = binary_message[:24]
                        message_length = int(binary_message_length, 2)
                        if len(binary_message) - 24 >= message_length:
                            break
            binary_encoded_message = binary_message[24:24 + message_length]
            encoded_message = ''.join(
                chr(int(binary_encoded_message[i:i + 8], 2)) for i in range(0, len(binary_encoded_message), 8))
            return encoded_message

        # Function for getting image
        def get_image():
            file_path = filedialog.askopenfilename()
            _, extension = os.path.splitext(file_path)
            size = os.path.getsize(file_path)
            suffixes = ['B', 'kB', 'MB']
            suffix_index = 0
            while size > 1024 and suffix_index < 3:
                suffix_index += 1
                size = size / 1024.0
            file_size = "%.*f %s" % (0, size, suffixes[suffix_index])
            image = Image.open(file_path)
            width, height = image.size
            return file_path, extension, file_size, image, width, height

        # Function for getting exif data
        def get_exif_data(image):
            exif_data = image.getexif()
            formatted_exif_data = ""
            if exif_data is not None:
                for tag, value in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag, tag)
                    if tag_name in ["Make", "Model", "DateTime", "XResolution", "YResolution", "Software",
                                    "Orientation", "ExposureTime", "FNumber", "ISOSpeedRatings", "ShutterSpeedValue",
                                    "ApertureValue", "BrightnessValue", "ExposureBiasValue", "MaxApertureValue",
                                    "MeteringMode", "Flash", "FocalLength", "ColorSpace", "ExifImageWidth",
                                    "ExifImageHeight", "WhiteBalance", "DigitalZoomRatio", "SceneCaptureType",
                                    "Contrast", "Saturation", "Sharpness", "GPSLatitude", "GPSLongitude", "GPSAltitude",
                                    "InteropIndex", "InteropVersion", "ProcessingSoftware", "SubfileType",
                                    "OldSubfileType", "ImageWidth", "ImageHeight", "BitsPerSample", "Compression",
                                    "PhotometricInterpretation", "Thresholding", "CellWidth", "CellLength", "FillOrder",
                                    "DocumentName", "ImageDescription", "StripOffsets", "Orientation",
                                    "SamplesPerPixel", "RowsPerStrip", "StripByteCounts", "MinSampleValue",
                                    "MaxSampleValue", "XResolution"]:
                        formatted_exif_data += f"{tag_name}: {value}\n"
            else:
                formatted_exif_data = "No EXIF data"
            return formatted_exif_data

        # Show image function
        def show_image(image, label):
            maximum_size = (256, 256)
            image_copy = image.copy()
            image_copy.thumbnail(maximum_size)
            tk_image = ImageTk.PhotoImage(image_copy)
            label.configure(image=tk_image)
            label.image = tk_image
            label.pil_image = image

        # Select image button
        def select_image_button():
            clear_button()
            self.file_path_label.configure(text=" ")
            filepath, extension, file_size, image, width, height = get_image()
            show_image(image, self.image_label)
            exif_data = get_exif_data(image)
            transparent_image = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
            tk_transparent_image = ImageTk.PhotoImage(transparent_image)
            self.encoded_image_label.configure(image=tk_transparent_image, text=exif_data)
            self.encoded_image_label.image = tk_transparent_image
            number_of_pixels = width * height
            number_of_pixels = "{:,}".format(number_of_pixels).replace(",", " ")
            self.image_properties_label.configure(text=f"{number_of_pixels} px, {extension}, {file_size}")
            self.file_path_label.configure(text=f"{filepath}")

        # Encode button
        def encode_button():
            error = self.file_path_label.cget("text")
            if error == "Select image first!" or error == "Select image first! !":
                error = error + " !"
                self.file_path_label.configure(text=error)
            elif error == "Select image first! ! !":
                error = "Select image first!"
                self.file_path_label.configure(text=error)
            else:
                plain_text = self.textbox1.get()
                self.textbox1.set(plain_text)
                filtered_text, encoded_image = encode(self.image_label.pil_image, plain_text)
                self.textbox2.delete(0, tk.END)
                self.textbox2.insert(0, filtered_text)
                self.textbox3.delete(0, tk.END)
                self.encoded_image_label.configure(image=None, text="")
                show_image(encoded_image, self.encoded_image_label)

        # Clear button
        def clear_button():
            if self.file_path_label.cget("text") == "Select image first!" or self.file_path_label.cget(
                    "text") == "Select image first! !" or self.file_path_label.cget(
                    "text") == "Select image first! ! !":
                self.file_path_label.configure(text="Select image first!")
            self.textbox1.set("")
            self.textbox2.delete(0, tk.END)
            self.textbox3.delete(0, tk.END)

        # Save image button
        def save_image_button():
            if self.file_path_label.cget("text") == "Select image first!" or self.file_path_label.cget(
                    "text") == "Select image first! !" or self.file_path_label.cget(
                    "text") == "Select image first! ! !":
                error = "Select image first!"
                self.file_path_label.configure(text=error)
            else:
                file_format = self.segmented_button1.get()[1:]
                file_path = filedialog.asksaveasfilename(defaultextension=file_format)
                if file_path:
                    encoded_image = self.encoded_image_label.pil_image
                    encoded_image.save(file_path, format=file_format)

        # Decode button
        def decode_button():
            error = self.file_path_label.cget("text")
            if error == "Select image first!" or error == "Select image first! !":
                error = error + " !"
                self.file_path_label.configure(text=error)
            elif error == "Select image first! ! !":
                error = "Select image first!"
                self.file_path_label.configure(text=error)
            else:
                self.textbox1.set("")
                self.textbox2.delete(0, tk.END)
                decoded_text = decode(self.image_label.pil_image)
                self.textbox3.delete(0, tk.END)
                self.textbox3.insert(0, decoded_text)

        # Image
        self.image_label = ctk.CTkLabel(self, text=" ")
        self.image_label.grid(row=1, column=0, rowspan=8, padx=32)

        # Empty label 1
        self.empty_label1 = ctk.CTkLabel(self, text=" ")
        self.empty_label1.grid(row=9, column=0)

        # Image properties
        self.image_properties_label = ctk.CTkLabel(self, text=" ")
        self.image_properties_label.grid(row=10, column=0)

        # Empty label 2
        self.empty_label2 = ctk.CTkLabel(self, text=" ")
        self.empty_label2.grid(row=11, column=0, columnspan=5)

        # Empty label 3
        self.empty_label3 = ctk.CTkLabel(self, text=" ")
        self.empty_label3.grid(row=0, column=1, columnspan=3)

        # Select image button
        self.select_image_button = ctk.CTkButton(self, text="Select image", command=select_image_button)
        self.select_image_button.grid(row=1, column=1)

        # File path
        self.file_path_label = ctk.CTkLabel(self, text="Select image first!")
        self.file_path_label.grid(row=2, column=1, columnspan=3)

        # Empty label 4
        self.empty_label4 = ctk.CTkLabel(self, text=" ")
        self.empty_label4.grid(row=9, column=1, columnspan=3)

        # Encode button
        self.encode_button = ctk.CTkButton(self, text="Encode", command=encode_button)
        self.encode_button.grid(row=10, column=1)

        # Image extension selection button
        self.segmented_button1 = ctk.CTkSegmentedButton(self, values=[".png", ".bmp"])
        self.segmented_button1.grid(row=1, column=2)
        self.segmented_button1.set(".png")

        # Text to encode
        self.text_to_encode_label = ctk.CTkLabel(self, text="Text to encode")
        self.text_to_encode_label.grid(row=3, column=1, columnspan=3)
        self.textbox1 = tk.StringVar()
        self.textbox1.trace("w", self.update_text_to_encode_label)
        self.entry1 = ctk.CTkEntry(self, textvariable=self.textbox1)
        self.entry1.grid(row=4, column=1, columnspan=3, sticky="ew")

        # Filtered text
        self.filtered_text_label = ctk.CTkLabel(self, text="Filtered text")
        self.filtered_text_label.grid(row=5, column=1, columnspan=3)
        self.textbox2 = ctk.CTkEntry(self)
        self.textbox2.grid(row=6, column=1, columnspan=3, sticky="ew")

        # Decoded text
        self.decoded_text_label = ctk.CTkLabel(self, text="Decoded text")
        self.decoded_text_label.grid(row=7, column=1, columnspan=3)
        self.textbox3 = ctk.CTkEntry(self)
        self.textbox3.grid(row=8, column=1, columnspan=3, sticky="ew")

        # Capacity
        self.capacity = ctk.CTkLabel(self, text=" ")
        self.capacity.grid(row=9, column=1, columnspan=3)

        # Clear button
        self.clear_button = ctk.CTkButton(self, text="Clear", width=64, command=clear_button)
        self.clear_button.grid(row=10, column=2)

        # Save image button
        self.save_image_button = ctk.CTkButton(self, text="Save image", command=save_image_button)
        self.save_image_button.grid(row=1, column=3)

        # Decode button
        self.decode_button = ctk.CTkButton(self, text="Decode", command=decode_button)
        self.decode_button.grid(row=10, column=3)

        # Encoded image
        self.encoded_image_label = ctk.CTkLabel(self, text=" ")
        self.encoded_image_label.grid(row=1, column=4, rowspan=8, padx=32)

        # Empty label 5
        self.empty_label5 = ctk.CTkLabel(self, text=" ")
        self.empty_label5.grid(row=9, column=4)

        # Empty label 6
        self.empty_label6 = ctk.CTkLabel(self, text=" ")
        self.empty_label6.grid(row=10, column=4)

    # Update text to encode label function
    def update_text_to_encode_label(self, *args):
        plain_text = self.textbox1.get()
        self.textbox1.set(plain_text)
        length = len(plain_text)
        number_of_pixels = 0
        image_properties = self.image_properties_label.cget("text")
        px_index = image_properties.find("px")
        if px_index != -1:
            number_of_pixels = image_properties[:px_index]
            number_of_pixels = "".join(number_of_pixels.split())
            number_of_pixels = int(number_of_pixels)
        capacity = ((number_of_pixels - 8) * 3) // 8
        capacity = "{:,}".format(capacity).replace(",", " ")
        capacity_number = int(capacity.replace(" ", ""))
        if self.file_path_label.cget("text") == "Select image first!" or self.file_path_label.cget(
                "text") == "Select image first! !" or self.file_path_label.cget("text") == "Select image first! ! !":
            if length == 0:
                self.text_to_encode_label.configure(text="Text to encode")
            elif length == 1:
                self.text_to_encode_label.configure(text=f"Text to encode: {length} character")
            else:
                self.text_to_encode_label.configure(text=f"Text to encode: {length} characters")
        else:
            if length == 0:
                self.text_to_encode_label.configure(text=f"Text to encode (Maximum: {capacity} characters)")
            elif length == 1:
                self.text_to_encode_label.configure(
                    text=f"Text to encode: {length} character (Maximum: {capacity} characters)")
            else:
                if length > capacity_number:
                    self.text_to_encode_label.configure(
                        text=f"Text is too long! {length} characters (Maximum: {capacity} characters)")
                else:
                    self.text_to_encode_label.configure(
                        text=f"Text to encode: {length} characters (Maximum: {capacity} characters)")


# Main loop
if __name__ == "__main__":
    app = App()
    app.mainloop()

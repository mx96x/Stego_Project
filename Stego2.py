import streamlit as st
from PIL import Image
import io

# Function to convert a message string to binary format (UTF-8)
def message_to_bin(message):
    return ''.join(format(byte, '08b') for byte in message.encode('utf-8'))

# Function to convert binary to a string (UTF-8)
def bin_to_message(binary):
    byte_array = bytearray(int(binary[i:i+8], 2) for i in range(0, len(binary), 8))
    return byte_array.decode('utf-8', errors='ignore')

# Function to check if the image can hold the message
def can_encode_message(image, message):
    max_capacity = image.width * image.height  # 1 bit per pixel
    message_binary_length = len(message_to_bin(message))
    return message_binary_length <= max_capacity

# Function to embed a message in an image
def encode_message(image, message):
    binary_message = message_to_bin(message) + '1111111111111110'  # EOF marker
    pixels = list(image.getdata())
    
    for i in range(len(binary_message)):
        pixel = list(pixels[i])
        pixel[0] = pixel[0] & 0xFE | int(binary_message[i])  # Modify the LSB of the red channel
        pixels[i] = tuple(pixel)
    
    new_image = Image.new(image.mode, image.size)
    new_image.putdata(pixels)
    return new_image

# Function to extract the message from an image
def decode_message(image):
    pixels = list(image.getdata())
    
    binary_message = ''
    for pixel in pixels:
        binary_message += str(pixel[0] & 1)  # Extract the LSB of the red channel
    
    # Split the binary string at the EOF marker and convert to message
    binary_message = binary_message.split('1111111111111110')[0]
    return bin_to_message(binary_message)

# Streamlit interface
st.title("Image Steganography")

option = st.selectbox(
    "What would you like to do?",
    ("Encode a Message", "Decode a Message")
)

if option == "Encode a Message":
    uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        message = st.text_area("Enter the message you want to encode")
        if st.button("Encode Message"):
            if message:
                if can_encode_message(image, message):
                    encoded_image = encode_message(image, message)
                    buf = io.BytesIO()
                    encoded_image.save(buf, format='PNG')
                    byte_im = buf.getvalue()

                    st.success("Message encoded successfully!")
                    st.download_button(
                        label="Download Encoded Image",
                        data=byte_im,
                        file_name="encoded_image.png",
                        mime="image/png"
                    )
                else:
                    st.error("The message is too long to encode in this image.")
            else:
                st.error("Please enter a message to encode.")

elif option == "Decode a Message":
    uploaded_image = st.file_uploader("Upload an encoded image", type=["png", "jpg", "jpeg"])
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        if st.button("Decode Message"):
            decoded_message = decode_message(image)
            st.text_area("Decoded Message", decoded_message)
 
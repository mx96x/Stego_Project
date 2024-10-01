# Image Steganography Web App

This is a simple web application built with Streamlit that allows users to encode and decode messages in images using steganography techniques.

## Features

- **Encode a Message:** Embed a hidden message inside an image by modifying the least significant bits of the red channel of the image.
- **Decode a Message:** Extract and decode a hidden message from an image that was encoded with this program.
- **Download Encoded Image:** After encoding a message, download the image with the hidden message as a `.png` file.

## How It Works

### Message Encoding:

1. The message is first converted into binary format.
2. The program embeds the binary message into the least significant bits (LSBs) of the red color channel of the image pixels.
3. A special marker `1111111111111110` is added to the end of the message to indicate the end of the binary message.

### Message Decoding:

1. The program reads the LSBs from the red channel of each pixel in the image.
2. The binary data is collected and converted back into a string up to the EOF marker `1111111111111110`.

## How to Run Locally

### Prerequisites

Make sure you have Python installed. You will also need the following Python packages:

- Streamlit
- Pillow (PIL)

### Installation

1. Clone the repository or download the project files.
2. Navigate to the project directory in your terminal.
3. Install the required packages using the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

### Running the App

To run the app locally, use the following command:

```bash
streamlit run stego.py
```

## Using the App

### Encoding a Message:

1. Upload an image (`.png`, `.jpg`, `.jpeg`).
2. Enter the message you want to hide in the image.
3. Click "Encode Message" to generate and download the new image with the hidden message.

### Decoding a Message:

1. Upload an image that has a hidden message.
2. Click "Decode Message" to extract and display the hidden message.

## License

All Rights Reserved

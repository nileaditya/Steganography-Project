# 🔒 Advanced AES-256 Steganography Engine

**Live Demo:** [https://stagonography.onrender.com/](https://stagonography.onrender.com/)

## 🚀 Overview
This project is a full-stack cryptographic web application designed to securely conceal text data within image files. Unlike standard steganography tools that leave hidden text in plain sight, this engine adds a layer of military-grade security by encrypting the payload before embedding it.

This tool was built to demonstrate advanced understanding of **Bitwise Operations**, **Symmetric Cryptography**, and **Full-Stack Web Deployment**.

## 🧠 Under the Hood (How it Works)

1. **Key Derivation (PBKDF2):** User passwords are mathematically hashed 100,000 times with a random 16-byte salt to prevent brute-force attacks, generating a secure 256-bit key.
2. **Encryption (AES-256-CBC):** The secret message is padded and encrypted using Advanced Encryption Standard in Cipher Block Chaining mode.
3. **Data Header Injection:** A 32-bit (4-byte) header is generated to store the exact length of the encrypted payload, preventing the extraction of image noise during decryption.
4. **Image Processing (LSB Math):** Using OpenCV, the image is flattened into a 1D pixel array. The Least Significant Bit (LSB) of the image's RGB values is isolated using bitwise AND (`& 0xFE`), and the encrypted binary payload is seamlessly injected using bitwise OR (`|`). 

## 🛠️ Tech Stack
* **Backend:** Python, Flask
* **Cryptography:** PyCryptodome (AES-256, PBKDF2)
* **Computer Vision:** OpenCV (`opencv-python-headless`)
* **Frontend:** HTML5, CSS3 (Responsive Dark Mode UI)
* **Deployment:** Gunicorn, Render (Cloud Hosting)

## 💻 Run it Locally

1. Clone the repository:
```bash
   git clone [https://github.com/nileaditya/Steganography-Project.git](https://github.com/nileaditya/Steganography-Project.git)
   cd Steganography-Project

2. Create and activate a virtual environment:
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install dependencies:
```bash
   pip install -r requirements.txt

4. Start the server:
```bash
   python app.py
Open http://127.0.0.1:5000 in your browser.

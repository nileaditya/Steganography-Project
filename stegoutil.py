import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def encrypt_message(image_path, message, password, output_path):
    # 1. CRYPTOGRAPHY: Generate secure key and encrypt
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32, count=100000)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    
    # 2. THE PAYLOAD
    payload = salt + cipher.iv + ct_bytes
    
    # ⭐ THE FIX: Calculate payload length and convert it to a 4-byte (32-bit) header
    payload_len_bytes = len(payload).to_bytes(4, byteorder='big')
    
    # Stick the length header onto the front of the payload
    full_payload = payload_len_bytes + payload
    
    # Convert to binary string
    binary_payload = ''.join(f"{byte:08b}" for byte in full_payload)

    # 3. IMAGE PROCESSING
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found. Please upload a valid image.")

    max_bytes = (img.shape[0] * img.shape[1] * 3) // 8
    if len(full_payload) > max_bytes:
        raise ValueError("Message is too large to hide inside this specific image.")

    flat = img.flatten()

    # 4. THE LSB MATH
    for i in range(len(binary_payload)):
        flat[i] = (flat[i] & 0xFE) | int(binary_payload[i])

    encoded_img = flat.reshape(img.shape)
    
    # Save as PNG to ensure lossless compression (JPEG destroys LSBs!)
    cv2.imwrite(output_path, encoded_img)
    return True


def decrypt_message(image_path, password):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or corrupted.")

    flat = img.flatten()

    # ⭐ THE FIX: Read ONLY the first 32 bits to find out how long our payload is
    length_binary = ''.join(str(flat[i] & 1) for i in range(32))
    payload_len = int(length_binary, 2)
    
    # Calculate the exact number of bits to extract (32 header bits + payload bits)
    total_bits = 32 + (payload_len * 8)
    
    # Security check: If the length is crazy, the image doesn't have our stego data
    if total_bits > len(flat) or payload_len <= 0:
        raise ValueError("Decryption failed. Incorrect password or no hidden data.")

    # Read exactly the payload bits, stopping before the image noise
    payload_binary = ''.join(str(flat[i] & 1) for i in range(32, total_bits))

    # Convert binary back to bytes
    payload_bytes = [int(payload_binary[i:i+8], 2) for i in range(0, len(payload_binary), 8)]
    payload = bytes(payload_bytes)

    if len(payload) < 32:
        raise ValueError("Corrupted data.")

    salt = payload[:16]
    iv = payload[16:32]
    ct = payload[32:]

    # 4. CRYPTOGRAPHY: Decrypt
    try:
        key = PBKDF2(password, salt, dkLen=32, count=100000)
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')
    except (ValueError, KeyError):
        raise ValueError("Decryption failed. Incorrect password or no hidden data.")
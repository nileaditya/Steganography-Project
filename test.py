from stegoutil import encrypt_message, decrypt_message

# 1. Setup your test variables
original_image = "try.png"  # Ensure this matches your actual image name!
encoded_image = "secret_image.png"
secret_text = "Falcon Tourism, I got the job! 💪😎"
password = "SuperSecretPassword123"

print("🔒 Encrypting and hiding message...")
try:
    # Hide the message
    encrypt_message(original_image, secret_text, password, encoded_image)
    print(f"✅ Success! Message hidden inside '{encoded_image}'.\n")

    # 2. Test the extraction and decryption
    print("🔓 Extracting and decrypting message...")
    extracted_text = decrypt_message(encoded_image, password)
    print(f"🎉 Extracted Message: {extracted_text}\n")

    # 3. Test the security (Intentionally using the wrong password)
    print("🚨 Testing security with the WRONG password...")
    decrypt_message(encoded_image, "HackerPassword999")

except Exception as e:
    # This will catch the intentional error from step 3
    print(f"🛑 Security Working! Error caught: {e}")
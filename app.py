import os
from flask import Flask, render_template, request, send_file
from stegoutil import encrypt_message, decrypt_message

# Initialize the Flask application
app = Flask(__name__)

# Create a temporary folder to store images while we process them
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route 1: The Homepage (GET Request)
# When someone visits your website, this serves the HTML page.
@app.route('/')
def index():
    return render_template('index.html')

# Route 2: The Encoding Endpoint (POST Request)
# This receives the image, message, and password from the frontend form.
@app.route('/encode', methods=['POST'])
def encode():
    try:
        # 1. Grab the data from the user's form
        image = request.files['image']
        message = request.form['message']
        password = request.form['password']

        # Security check
        if not image.filename or not message or not password:
            return "Missing data! Please provide an image, message, and password.", 400

        # 2. Save the uploaded image temporarily
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_path)

        # 3. Define where to save the new, encoded image
        output_filename = 'encoded_' + image.filename
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)

        # 4. Call our battle-tested engine!
        encrypt_message(image_path, message, password, output_path)

        # 5. Send the new image back to the user to download
        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return f"An error occurred during encryption: {e}", 500

# Route 3: The Decoding Endpoint (POST Request)
# This receives the stego-image and password to unlock it.
@app.route('/decode', methods=['POST'])
def decode():
    try:
        # 1. Grab the image and password
        image = request.files['stego_image']
        password = request.form['password']

        if not image.filename or not password:
            return "Missing data! Please provide an image and password.", 400

        # 2. Save the image temporarily
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_path)

        # 3. Call the engine to extract the hidden text
        hidden_message = decrypt_message(image_path, password)
        
        # 4. Display the success message to the user
        return f"<h3>🎉 Hidden Message Extracted Successfully:</h3><p><b>{hidden_message}</b></p><br><a href='/'>Go Back</a>"

    except Exception as e:
        # If they use the wrong password, our stegoutil throws an error, and we catch it here!
        return f"<h3>🛑 Decryption Failed:</h3><p>{e}</p><br><a href='/'>Go Back</a>", 400

# Start the development server
if __name__ == '__main__':
    app.run(debug=True)
import os
from flask import Flask, request, jsonify, make_response
from PIL import Image
from rembg import remove
from io import BytesIO

app = Flask(__name__)

@app.route('/remove-background', methods=['POST'])
def remove_background():
    # Check if the request contains an image file
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'})

    image_file = request.files['image']

    try:
        # Open the image file
        input_image = Image.open(image_file)

        # Perform background removal
        output_image = remove(input_image, auto_max=True)

        # Convert to RGB mode
        output_image = output_image.convert('RGB')

        # Create a BytesIO object to hold the image data
        output_data = BytesIO()

        # Save the image data to the BytesIO object
        output_image.save(output_data, 'JPEG')

        # Delete the processed image from local storage
        os.remove(image_file.filename)

        # Return the image data as a response
        response = make_response(output_data.getvalue())
        response.headers['Content-Type'] = 'image/jpeg'
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port='5000', host='0.0.0.0')

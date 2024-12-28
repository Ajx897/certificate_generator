from flask import Flask, request, jsonify, send_from_directory, render_template, send_file
import os
import json
from PIL import Image, ImageDraw, ImageFont
import qrcode

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CERTIFICATE_FOLDER = os.path.join(BASE_DIR, 'certi', 'certificates')
TEMPLATE_PATH = os.path.join(BASE_DIR, 'certi', 'your_organization.png')
FONT_PATH = os.path.join(BASE_DIR, 'certi', 'Montserrat-Bold.ttf')
OUTPUT_FOLDER = CERTIFICATE_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_certificate', methods=['POST'])
def generate_certificate():
    recipient_name = request.form['recipient_name']
    location = request.form['location']
    district = request.form['district']
    UserId = request.form['UserID']
    Issued_Date= request.form['Issued_Date']

    if not recipient_name or not location or not district or not UserId or not Issued_Date:
        return render_template('index.html', error="Please fill in all fields.")

    try:
        # Load the certificate template
        certificate_template = Image.open(TEMPLATE_PATH)

        # Make a copy of the template
        certificate = certificate_template.copy()
        draw = ImageDraw.Draw(certificate)

        # Define fonts
        font_large = ImageFont.truetype(FONT_PATH, 60)
        font_medium = ImageFont.truetype(FONT_PATH, 30)

        # Define text positions (approximate, adjust as needed)
        recipient_position = (580, 856)  # Centered on the certificate
        location_position = (520, 1136)
        district_position = (962, 1134)
        UserId_position=(497,1249)
        Issued_Date_position=(967,1245)

        # Add text to the certificate
        draw.text(recipient_position, recipient_name, font=font_large, fill="#000000", anchor="mm")
        draw.text(location_position, location, font=font_medium, fill="#000000", anchor="mm")
        draw.text(district_position, district, font=font_medium, fill="#000000", anchor="mm")
        draw.text(UserId_position,UserId,font=font_medium, fill="#000000", anchor="mm")
        draw.text(Issued_Date_position,Issued_Date,font=font_medium, fill="#000000", anchor="mm")
        # Generate the QR code
        qr_data = f"http://your_domain/certificate/{recipient_name.replace(' ', '_')}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill='black', back_color='white')

        # Resize the QR code to fit the certificate
        qr_img = qr_img.resize((200, 200))  # Adjust size as needed

        # Position the QR code at the specified coordinates
        qr_position = (1125,1738)
        certificate.paste(qr_img, qr_position)

        # Save the certificate
        output_filename = f"certificate_{recipient_name.replace(' ', '_')}.jpg"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        certificate.save(output_path)

        # Save certificate details in a JSON file
        details_path = os.path.join(CERTIFICATE_FOLDER, f"{recipient_name.replace(' ', '_')}.json")
        certificate_details = {
            "recipient_name": recipient_name,
            "location": location,
            "district": district,
            "Issued_Date":Issued_Date,
            "UserId":UserId,
            "certificate_url": qr_data.replace('/certificate/', '/certificates/certificate_') + '.jpg'
        }
        with open(details_path, 'w') as f:
            json.dump(certificate_details, f)

        # Render success.html with the certificate URL and filename
        return render_template('success.html', certificate_url=certificate_details["certificate_url"], certificate_filename=output_filename)
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/certificate/<recipient_name>')
def get_certificate_details(recipient_name):
    try:
        # Assuming the certificate filename is based on the recipient's name
        certificate_filename = f"certificate_{recipient_name}.jpg"
        certificate_path = os.path.join(CERTIFICATE_FOLDER, certificate_filename)
        details_path = os.path.join(CERTIFICATE_FOLDER, f"{recipient_name}.json")

        if not os.path.exists(certificate_path) or not os.path.exists(details_path):
            return jsonify({"error": "Certificate not found"}), 404

        # Load certificate details from JSON file
        with open(details_path, 'r') as f:
            certificate_details = json.load(f)

        return render_template('certificate.html', **certificate_details)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/certificates/<filename>')
def get_certificate(filename):
    return send_from_directory(CERTIFICATE_FOLDER, filename)

@app.route('/download/<filename>')
def download_certificate(filename):
    return send_file(os.path.join(CERTIFICATE_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

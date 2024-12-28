# Certificate Generator

This Python project allows users to generate certificates based on predefined templates. By providing required information such as name, date, etc., and setting coordinates for fields, users can easily generate professional certificates.

## Features

- Select predefined certificate templates.
- Input required information such as name, date, and other fields.
- Set coordinates for the fields to ensure proper placement on the template.
- Successfully generate and save certificates in image or PDF format.

## Installation

To use this certificate generator on your local machine, follow these steps:

1. Clone the repository:
   git clone https://github.com/Ajx897/certificate_generator.git

   ## Usage

1. **Prepare the Template:**
   - Create or choose a predefined certificate template with placeholders for fields like Name, Date, and others. Make sure the fields are clearly marked where you want the dynamic information (e.g., `<Name>`, `<Date>`).

2. **Set Coordinates:**
   - Use an image map generator tool to map the coordinates of the placeholders (for example, the Name, Date, etc.). You can use this website to map coordinates: [Image Map Generator](https://www.image-map.net/).
   - Once you have mapped the coordinates, note down the values for each field.

3. **Run the Script:**
   - Open the terminal and navigate to the project directory where the `generate_certificate.py` file is located.
   - Run the script:
     python generate_certificate.py
   
4. **Input the Required Information:**
   - The script will prompt you to input the required information (e.g., Name, Date). Enter the details as per the placeholders in your template.

5. **Certificate Generation:**
   - After entering the information, the certificate will be generated and saved in the output directory, typically in PNG or PDF format (depending on your script setup).

6. **Download the Generated Certificate:**
   - The generated certificate will be saved in the output folder (you can specify the output location if needed).

import streamlit as st
import fitz  # PyMuPDF
import json
from io import BytesIO

def extract_text_from_pdf(pdf_file):
    text_data = []
    # Open PDF from a BytesIO object (which is what Streamlit uploader provides)
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as pdf:
        for page_num in range(pdf.page_count):
            page = pdf.load_page(page_num)
            text_data.append(page.get_text("text"))
    return "\n".join(text_data)

def convert_text_to_json(text):
    # Split text into lines
    lines = text.splitlines()

    data_dict = {}
    key = None

    # Iterate over each line and build the key-value pairs
    for i in range(len(lines)):
        line = lines[i].strip()
        
        if line:
            # If this line contains a key (it is followed by another line that is the value)
            if key is None:
                key = line
            else:
                # This line is the value for the previous key
                data_dict[key] = line
                key = None  # Reset key after assigning the value

    return data_dict

# Streamlit app setup
st.title("PDF to JSON Converter")
st.write("Upload a PDF file to extract data and convert it to JSON format.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.write("### Extracted Text")
    st.text(pdf_text)

    # Convert extracted text to JSON format
    json_data = convert_text_to_json(pdf_text)
    st.write("### JSON Data")
    st.json(json_data)

    # Option to download JSON file
    json_file_name = "extracted_data.json"
    with open(json_file_name, "w") as json_file:
        json.dump(json_data, json_file)

    with open(json_file_name, "rb") as json_file:
        st.download_button(label="Download JSON File",
                           data=json_file,
                           file_name=json_file_name,
                           mime="application/json")



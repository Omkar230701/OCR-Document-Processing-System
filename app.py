import streamlit as st
from ocr_engine import extract_text
from extractor import extract_data
from classifier import classify_document
import tempfile

st.title("📄 OCR Document Processing System")

uploaded_file = st.file_uploader("Upload Document", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Document", width=400)

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    # OCR
    text = extract_text(temp_path)
    text_lower = text.lower()

    # ML prediction (baseline)
    ml_type = classify_document(text)

    # STRONG RULE-BASED OVERRIDE (priority > ML)
    # Order matters: invoice first, then receipt
    if ("invoice" in text_lower 
        or "total amount due" in text_lower 
        or "due date" in text_lower):
        doc_type = "invoice"

    elif ("receipt" in text_lower 
          or "payment" in text_lower 
          or "paid by" in text_lower):
        doc_type = "receipt"

    else:
        doc_type = ml_type  # fallback to ML

    # Extraction
    data = extract_data(text)

    # Display
    st.subheader("📌 Document Type:")
    st.write(doc_type)

    st.subheader("📝 Extracted Text:")
    st.text(text)

    st.subheader("📊 Extracted Data:")
    st.json(data)

    # Confidence scoring (balanced)
    score = 0

    if data["Amount"] != "Not Found":
        score += 40

    if data["Date"] != "Not Found":
        score += 25

    if doc_type != "unknown":
        score += 20

    if data["Invoice Number"] != "Not Found":
        score += 10

    if data["Email"] != "Not Found" or data["Phone"] != "Not Found":
        score += 5

    st.write(f"Confidence Score: {score}%")
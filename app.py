import streamlit as st
from PIL import Image

from ocr_engine import extract_text
from classifier import classify_document
from extractor import extract_invoice_data


# Page setup
st.set_page_config(page_title="OCR System", layout="centered")

st.title("📄 OCR Document Processing System")
st.markdown("---")

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Document", use_container_width=True)

    if st.button("Process Document"):

        with st.spinner("Processing..."):

            # OCR
            text = extract_text(image)

            # Classification
            doc_type = classify_document(text)

            # Extraction
            if doc_type == "Invoice":
                data = extract_invoice_data(text)
            else:
                data = {"Message": "Extraction only supported for invoices"}

        st.success("Processing Completed")
        st.markdown("---")

        # Document Type
        st.subheader("📌 Document Type:")
        st.write(doc_type)

        # Extracted Text
        st.subheader("📝 Extracted Text:")
        st.text_area("", text, height=300)

        st.markdown("---")

        # Extracted Data
        st.subheader("📊 Extracted Data:")

        if doc_type == "Invoice":

            col1, col2, col3 = st.columns(3)

            col1.metric("Invoice No", data.get("Invoice Number", ""))
            col2.metric("Date", data.get("Date", ""))
            col3.metric("Amount", data.get("Amount", ""))

            st.write("📧 Email:", data.get("Email", "Not Found"))
            st.write("📞 Phone:", data.get("Phone", "Not Found"))

            # Confidence (FIXED)
            confidence_str = data.get("Confidence Score", "0%").replace("%", "")

            try:
                confidence_value = float(confidence_str)
            except:
                confidence_value = 0

            st.progress(int(confidence_value))
            st.caption(f"Confidence Score: {data.get('Confidence Score', '')}")

            st.markdown("---")

            # Proper JSON
            st.subheader("📦 Raw Output (JSON):")
            st.json(data)

        else:
            st.write(data)
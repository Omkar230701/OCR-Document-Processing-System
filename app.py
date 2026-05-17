import streamlit as st
from ocr_engine import extract_text
from extractor import extract_data
from classifier import classify_document
import tempfile
import base64


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="OCR Dashboard",
    layout="wide"
)


# ---------------- LOAD BACKGROUND IMAGE ----------------
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


img_base64 = get_base64("background.png")


# ---------------- CUSTOM CSS ----------------
st.markdown(
    f"""
    <style>

    /* Background */
    .stApp {{
        background-image:
        linear-gradient(
            rgba(3, 8, 20, 0.82),
            rgba(3, 8, 20, 0.88)
        ),
        url("data:image/png;base64,{img_base64}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Remove Streamlit Header */
    header {{
        background: transparent !important;
    }}

    /* Main Container */
    .main-container {{
        background: rgba(7, 15, 30, 0.72);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 24px;
        padding: 35px;
        backdrop-filter: blur(14px);
        box-shadow: 0 0 40px rgba(0,0,0,0.55);
        margin-top: 20px;
    }}

    /* Title */
    .title {{
        color: white;
        font-size: 52px;
        font-weight: 700;
        margin-bottom: 35px;
    }}

    /* Section Labels */
    .section-label {{
        color: white;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 12px;
    }}

    /* Extracted Text Box */
    .data-box {{
        background: rgba(0, 0, 0, 0.58);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 16px;
        padding: 22px;
        overflow-x: auto;
    }}

    .data-box pre {{
        color: white !important;
        font-size: 16px !important;
        line-height: 1.7;
        white-space: pre-wrap;
    }}

    /* Confidence Score */
    .success {{
        color: #59FF95;
        font-size: 30px;
        font-weight: bold;
    }}

    /* Document Badge */
    .badge {{
        display: inline-block;
        background: rgba(25, 135, 84, 0.25);
        border: 1px solid #59FF95;
        color: #59FF95;
        padding: 8px 18px;
        border-radius: 12px;
        font-size: 18px;
        font-weight: 600;
    }}

    /* File Uploader Box */
    section[data-testid="stFileUploader"] {{
        background: rgba(255,255,255,0.94);
        border-radius: 18px;
        padding: 18px;
        border: none;
    }}

    /* Upload Filename */
    section[data-testid="stFileUploader"] small {{
        color: #666666 !important;
        font-size: 15px !important;
        font-weight: 500;
    }}

    /* Upload Helper Text */
    section[data-testid="stFileUploader"] span {{
        color: #8A8A8A !important;
        font-size: 14px !important;
    }}

    /* ===== UPLOAD BUTTON — Override Streamlit CSS variables ===== */

    /* Override the CSS variables Streamlit uses for secondary buttons */
    :root {{
        --secondary-background-color: #000000;
    }}

    /* Target every possible way Streamlit renders the upload button */
    .stFileUploader button,
    .stFileUploader button:hover,
    .stFileUploader button:focus,
    .stFileUploader button:active,
    div.stFileUploader button,
    div.stFileUploader button:hover,
    section.stFileUploader button,
    section.stFileUploader button:hover,
    [data-testid="stFileUploader"] button,
    [data-testid="stFileUploader"] button:hover,
    [data-testid="stFileUploader"] button:focus,
    [data-testid="stFileUploader"] button:active,
    [data-testid="stFileUploaderDropzone"] button,
    [data-testid="stFileUploaderDropzone"] button:hover {{
        background-color: #000000 !important;
        background: #000000 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        min-height: 48px !important;
        box-shadow: none !important;
    }}

    /* Force white text inside button */
    .stFileUploader button *,
    .stFileUploader button:hover *,
    [data-testid="stFileUploader"] button *,
    [data-testid="stFileUploader"] button:hover * {{
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
    }}

    /* Subtle white glow on hover so user knows it's clickable */
    [data-testid="stFileUploader"] button:hover {{
        box-shadow: 0 0 0 3px rgba(255,255,255,0.3) !important;
    }}

    /* ===== END UPLOAD BUTTON ===== */

    /* JSON Box */
    div[data-testid="stJson"] {{
        background: rgba(255,255,255,0.94) !important;
        border-radius: 16px !important;
        padding: 18px !important;
        border: none !important;
    }}

    /* JSON Text */
    div[data-testid="stJson"] * {{
        color: black !important;
        font-size: 16px !important;
        font-weight: 500 !important;
    }}

    /* Uploaded Image */
    div[data-testid="stImage"] img {{
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.15);
    }}

    /* Generic Text */
    p, label, div {{
        color: white;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------- MAIN CONTAINER ----------------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown(
    '<div class="title">📄 OCR Document Processing System</div>',
    unsafe_allow_html=True
)


# ---------------- LAYOUT ----------------
col1, col2 = st.columns([2, 1])


# ---------------- FILE UPLOAD ----------------
with col1:

    st.markdown(
        '<div class="section-label">Upload Document</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload Invoice / Receipt",
        type=["png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )


# ---------------- IMAGE PREVIEW ----------------
with col2:

    st.markdown(
        '<div class="section-label">Uploaded Document</div>',
        unsafe_allow_html=True
    )

    if uploaded_file:
        st.image(uploaded_file, width=260)


# ---------------- OCR PROCESSING ----------------
if uploaded_file:

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    # OCR extraction
    text = extract_text(temp_path)
    text_lower = text.lower()

    # ML prediction
    ml_type = classify_document(text)

    # Rule-based override
    if (
        "invoice" in text_lower
        or "total amount due" in text_lower
        or "due date" in text_lower
    ):
        doc_type = "invoice"

    elif (
        "receipt" in text_lower
        or "payment" in text_lower
        or "paid by" in text_lower
    ):
        doc_type = "receipt"

    else:
        doc_type = ml_type

    # Extract structured data
    data = extract_data(text)

    # ---------------- CONFIDENCE SCORE ----------------
    score = 0

    if data["Amount"] != "Not Found":
        score += 40

    if data["Date"] != "Not Found":
        score += 25

    if doc_type != "unknown":
        score += 20

    if data["Invoice Number"] != "Not Found":
        score += 10

    if (
        data["Email"] != "Not Found"
        or data["Phone"] != "Not Found"
    ):
        score += 5

    # ---------------- EXTRACTED DATA ----------------
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-label">📊 Extracted Data</div>',
        unsafe_allow_html=True
    )

    st.json(data)

    # ---------------- CONFIDENCE SCORE ----------------
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="section-label">
        Confidence Score:
        <span class="success">{score}%</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- DOCUMENT TYPE ----------------
    st.markdown(
        f"""
        <div class="section-label">
        Document Type:
        <span class="badge">{doc_type}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- EXTRACTED TEXT ----------------
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-label">📝 Extracted Text</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="data-box">
        <pre>{text}</pre>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- END CONTAINER ----------------
st.markdown("</div>", unsafe_allow_html=True)
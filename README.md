# 📄 OCR Document Processing System

## 🚀 Overview

This project is an AI-based OCR (Optical Character Recognition) system that extracts structured data from invoice documents.

The system converts unstructured scanned documents into meaningful structured information using OCR and rule-based processing.

---

## ⚙️ Features

* 📄 Extract Invoice Number, Date, and Total Amount
* 📧 Extract Email and Phone Number
* 🔍 Handles OCR noise and formatting variations
* 📊 Confidence Score calculation
* 🎨 Interactive Streamlit-based UI
* 🧠 Robust extraction using regex + post-processing

---

## 🧠 Tech Stack

* Python
* OpenCV (Image preprocessing)
* Tesseract OCR (Text extraction)
* Streamlit (Frontend UI)
* Regex (Data extraction)

---

## 🏗️ Project Structure

```
ocr-project/
│
├── app.py              # Streamlit frontend
├── extractor.py        # Data extraction logic
├── classifier.py       # Document classification
├── ocr_engine.py       # OCR + preprocessing
├── requirements.txt    # Dependencies
├── README.md           # Project documentation
│
├── screenshots/
│   ├── input.png
│   ├── output.png
```

---

## 📸 Screenshots

### 🔹 Input Document

![Input](screenshots/input.png)

### 🔹 Extracted Output

![Output](screenshots/output.png)

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Omkar230701/OCR-Document-Processing-System.git
cd OCR-Document-Processing-System
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run app.py
```

---

## 📊 Example Output

```json
{
  "Invoice Number": "INV-0001",
  "Date": "01/01/2024",
  "Amount": "55.00",
  "Email": "hello@mac.com",
  "Phone": "0712345678",
  "Confidence Score": "100%"
}
```

---

## 🧠 Methodology

### 1. Image Preprocessing

* Convert image to grayscale
* Apply thresholding for noise reduction

### 2. OCR Processing

* Extract text using Tesseract OCR

### 3. Data Extraction

* Use regex patterns to identify:

  * Invoice Number
  * Date
  * Amount
  * Email
  * Phone

### 4. Post-processing

* Normalize values
* Fix OCR errors (e.g., 55,006 → 55.00)

### 5. Frontend Display

* Show results using Streamlit UI

---

## 🎯 Use Cases

* Invoice Processing Automation
* Accounts Payable Systems
* Document Digitization
* Business Workflow Automation

---

## ⚠️ Limitations

* Accuracy depends on image quality
* OCR may misread special characters
* Not optimized for handwritten text

---

## 🚀 Future Improvements

* Support for PDF documents
* NLP-based intelligent extraction
* Multi-language support
* Cloud deployment

---

## 👨‍💻 Author

**Omkar Varpe**
F.Y. M.Sc Data Science
Vishwakarma University

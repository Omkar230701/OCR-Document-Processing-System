import re

def extract_invoice_data(text):
    data = {}

    # ---------------------------
    # Clean OCR text
    # ---------------------------
    clean_text = text.replace("\n", " ")

    # ---------------------------
    # 🔹 Invoice Number (robust)
    # ---------------------------
    invoice = re.search(
        r'Invoice\s*(No|Number)?[:\s]*([A-Z]+[-\s]?\d+)',
        clean_text,
        re.IGNORECASE
    )

    data["Invoice Number"] = invoice.group(2).strip() if invoice else "Not Found"

    # ---------------------------
    # 🔹 Date (multi-format support)
    # ---------------------------
    date = re.search(
        r'(Issue Date|Invoice Date)[^\d]*(\d{2}[./\s]\d{2}[./\s]\d{4})',
        clean_text,
        re.IGNORECASE
    )

    if date:
        raw = date.group(2)
        digits = re.sub(r'[^\d]', '', raw)  # remove ., /, space
        data["Date"] = f"{digits[:2]}/{digits[2:4]}/{digits[4:]}"
    else:
        data["Date"] = "Not Found"

    # ---------------------------
    # 🔹 Amount (robust + OCR fix)
    # ---------------------------
    amount = re.search(
        r'\bTotal\b[^\d]*(\d+[.,]?\d*)',
        clean_text,
        re.IGNORECASE
    )

    if amount:
        raw_amt = amount.group(1)

        # Replace comma with dot
        cleaned = raw_amt.replace(",", ".")

        # Fix OCR errors like 55.006 → 55.00
        if "." in cleaned:
            parts = cleaned.split(".")
            if len(parts[1]) > 2:
                cleaned = parts[0] + "." + parts[1][:2]

        data["Amount"] = cleaned
    else:
        data["Amount"] = "Not Found"

    # ---------------------------
    # 🔹 Email (strict)
    # ---------------------------
    email = re.search(r'\S+@\S+\.\S+', clean_text)
    data["Email"] = email.group(0) if email else "Not Found"

    # ---------------------------
    # 🔹 Phone (10 digits)
    # ---------------------------
    phone = re.search(r'\b\d{10}\b', clean_text)
    data["Phone"] = phone.group(0) if phone else "Not Found"

    # ---------------------------
    # 🔹 Confidence Score
    # ---------------------------
    confidence = 0

    if data["Invoice Number"] != "Not Found":
        confidence += 0.25
    if data["Date"] != "Not Found":
        confidence += 0.25
    if data["Amount"] != "Not Found":
        confidence += 0.25
    if data["Email"] != "Not Found":
        confidence += 0.125
    if data["Phone"] != "Not Found":
        confidence += 0.125

    data["Confidence Score"] = f"{int(confidence * 100)}%"

    return data
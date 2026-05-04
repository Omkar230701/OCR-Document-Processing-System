def classify_document(text):
    text = text.lower()

    if "invoice" in text:
        return "Invoice"
    elif "report" in text:
        return "Report"
    elif "contract" in text:
        return "Contract"
    else:
        return "Unknown"
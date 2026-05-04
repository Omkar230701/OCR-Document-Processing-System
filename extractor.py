import re

def extract_data(text):
    data = {}

    # Invoice Number
    invoice = re.search(r'(INV[-\s]?\d+)', text, re.IGNORECASE)
    data["Invoice Number"] = invoice.group(1) if invoice else "Not Found"

    # Date
    date = re.search(r'(\d{2}[./-]\d{2}[./-]\d{4})', text)
    data["Date"] = date.group(1) if date else "Not Found"

    # Amount (FIXED LOGIC)
    amounts = re.findall(r'(\d{1,3}(?:,\d{3})+(?:\.\d{2})?|\d+\.\d{2})', text)

    if amounts:
        cleaned = []
        for amt in amounts:
            amt = amt.replace(",", "")  # remove commas
            try:
                cleaned.append(float(amt))
            except:
                pass

        if cleaned:
            max_value = max(cleaned)
            data["Amount"] = f"{max_value:.2f}"
        else:
            data["Amount"] = "Not Found"
    else:
        data["Amount"] = "Not Found"

    # Email
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    data["Email"] = email.group(0) if email else "Not Found"

    # Phone
    phone = re.search(r'(\d{10}|\d{3}[-.\s]\d{3}[-.\s]\d{4})', text)
    data["Phone"] = phone.group(0) if phone else "Not Found"

    return data
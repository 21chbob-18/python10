import pytesseract, re, cv2, numpy as np
from PIL import Image

def preprocess_image(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return thresh


def extract_text(image):
    processed = preprocess_image(image)
    text = pytesseract.image_to_string(processed)
    return text


def extract_line_items(text):
    lines = text.split("\n")

    item_pattern = re.compile(r"(.*?)(\d+[.,]\d{2})$")
    total_pattern = re.compile(r"(total|amount payable|grand total)", re.I)

    items = []
    subtotal = None
    final = None

    for line in lines:
        line = line.strip()
        match = item_pattern.search(line)

        if match:
            desc = match.group(1).strip()
            amt = float(match.group(2).replace(",", ""))
            items.append({"description": desc, "amount": amt})

        if total_pattern.search(line):
            amounts = re.findall(r"\d+[.,]\d{2}", line)
            if amounts:
                final = float(amounts[-1].replace(",", ""))

    computed_total = round(sum(i["amount"] for i in items), 2)

    return {
        "line_items": items,
        "subtotal": subtotal,
        "final_total_computed": computed_total,
        "final_total_extracted": final
    }

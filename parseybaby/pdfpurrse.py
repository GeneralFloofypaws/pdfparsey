import fitz

def gettexthehe(pdfpath):

    docu = fitz.open(pdfpath)

    text = ""

    for page in docu: 

        text += "\n" + page.get_text()

    docu.close()

    return text

def is_all_caps(text):
    letters = [char for char in text if char.isalpha()]
    return bool(letters) and all(char.isupper() for char in letters)

def is_bold(font_name):
   return "bold" in font_name.lower()

def is_italic(font_name):
    font = font_name.lower()
    return "italic" in font or  "oblique" in font

def get_layout(pdf_path):
    doc = fitz.open(pdf_path)
    layout_stuff = []

    for page_no, page in enumerate(doc, start = 1): 
        data = page.get_text("dict")

        for block in data["blocks"]:
            if block["type"] != 0:
                continue

            for line in block["lines"]:
                line_text = ""
                spans_info = []

                for span in line["spans"]:
                    text = span["text"]

                    if not text.strip():
                        continue 

                    line_text += text + " "

                    spans_info.append({
                        "text": text,
                        "font": span["font"],
                        "size": span["size"],
                        "bold": is_bold(span["font"]),
                        "italic": is_italic(span["font"]),
                        "bbox": span["bbox"]
                    })

                if line_text.strip():

                    font_sizes = [span["size"] for span in spans_info]

                    layout_stuff.append({
                        "page": page_no,
                        "text": line_text.strip(),
                        "font_size": max(font_sizes),
                        "all_caps": is_all_caps(line_text),
                        "has_bold": any(span["bold"] for span in spans_info),
                        "bbox": line["bbox"],
                        "x0": line["bbox"][0],
                        "y0": line["bbox"][1],
                        "x1": line["bbox"][2],
                        "y1": line["bbox"][3]
                    })

    doc.close()
    return layout_stuff

def get_tables(pdf_path):
    doc = fitz.open(pdf_path)
    tables = []

    for page_no, page in enumerate(doc, start = 1):
        found_tables = page.find_tables()

        for table in found_tables:
            tables.append({
                "page": page_no,
                "rows": table.extract()
            })

    doc.close()
    return tables
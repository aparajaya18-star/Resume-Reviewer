import pymupdf

# ----Extract text from pdf (Common Use)-----
def load_pdf(uploaded_file):
    text = []
    pages = 0

    # Read the file buffers from Streamlit
    file_bytes = uploaded_file.read()

    # Open the pdf from memory stream
    with pymupdf.open(stream=file_bytes, filetype="pdf") as doc:
        # Iterate through each pdf page
        for page in doc:
            pages += 1
            # Extract text blocks, sorted by natural reading order (helps seperate different paragraphs and headings)
            blocks = page.get_text("blocks", sort=True)
            for block in blocks:
                # Block[4] contains extracted text string
                text.append(block[4])

    full_text = "\n\n".join(text)
    return full_text, pages
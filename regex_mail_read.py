import imaplib
import email
from email.header import decode_header
import os
from PyPDF2 import PdfReader
import re

# ==== YOUR CREDENTIALS ====
EMAIL = "chaitrapaladugula@gmail.com"
PASSWORD = "*******"  # This is an App Password (for Gmail)
IMAP_SERVER = "imap.gmail.com"
DOWNLOAD_FOLDER = "downloads"

# Ensure download folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)
mail.select("inbox")

# Search for emails with subject containing "invoice"
status, data = mail.search(None, '(SUBJECT "invoice")')

if status != "OK" or not data[0]:
    print("No messages found!")
    exit()

# Get the first matching email
email_ids = data[0].split()
latest_email_id = email_ids[0]

# Fetch the email by ID
status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

if status != "OK":
    print("Failed to fetch email!")
    exit()

raw_email = msg_data[0][1]
msg = email.message_from_bytes(raw_email)

# Extract attachments
pdf_path = None
for part in msg.walk():
    content_disposition = str(part.get("Content-Disposition"))
    if part.get_content_maintype() == 'multipart':
        continue
    if "attachment" in content_disposition:
        filename = part.get_filename()
        if filename and filename.endswith(".pdf"):
            filepath = os.path.join(DOWNLOAD_FOLDER, filename)
            with open(filepath, "wb") as f:
                f.write(part.get_payload(decode=True))
            pdf_path = filepath
            break

if not pdf_path:
    print("No PDF attachment found.")
    exit()

print(f"PDF saved to: {pdf_path}")

# Extract text from PDF
def extract_text_from_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

pdf_text = extract_text_from_pdf(pdf_path)

# Extract key-value pairs using regex
def extract_key_value_pairs(text):
    pattern = r"([\w\s]+):\s+([^\n]+)"
    matches = re.findall(pattern, text)
    return {key.strip(): value.strip() for key, value in matches}

key_value_pairs = extract_key_value_pairs(pdf_text)

print("\n🔑 Extracted Key-Value Pairs:")
for key, value in key_value_pairs.items():
    print(f"{key}: {value}")

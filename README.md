# 📧 Invoice Email Parser

This Python project connects to a Gmail account using IMAP, reads the first email with a subject containing the word "invoice", downloads the attached PDF file, extracts text from it, and parses key-value pairs from the PDF contents.

---

## 🚀 Features

- Connects securely to a Gmail inbox via IMAP
- Searches for the first email with subject: **invoice**
- Downloads the **first attached PDF file**
- Extracts text content from the PDF
- Uses regular expressions to identify and extract **key-value pairs**
- Saves the PDF file to a local directory

---

## 🛠️ Requirements

- Python 3.7+
- Gmail IMAP Access Enabled

### 📦 Python Libraries

Install dependencies using:

```bash
pip install PyPDF2 python-dotenv

```markdown
# Trace Sight Forensics

**Trace Sight Forensics** is an automated digital forensics desktop tool designed for investigators to rapidly extract, analyze, and log hidden metadata, EXIF tags, and GPS coordinates from seized image evidence. 

Featuring an intuitive graphical user interface (GUI) and structured audit logging, this engine eliminates manual terminal commands during evidence processing.

---

## Key Features

* **Graphical User Interface (GUI):** Built with Python's `tkinter` to provide a clean, user-friendly workspace for selecting and processing image files.
* **Deep Metadata Extraction:** Automatically parses internal file data to recover camera manufacturer, specific device models, and exact timestamps (`DateTimeOriginal`).
* **Geo-Location & Mapping:** Extracts latitude and longitude coordinates and generates direct map navigation links.
* **Cryptographic Verification:** Computes unique SHA-256 file hashes for every processed image to maintain a strict chain of custody.
* **Automated Evidence Ledger:** Appends all cleaned structural findings, hashes, and coordinates directly into a structured CSV log (`evidence_log.csv`) for bulk case management.
* **Smart Error Handling:** Cleanly flags missing metadata, stripped tags, or disabled location services without crashing the application engine.

---

## Project Structure

```text
Trace-Sight-Forensics/
│
├── app.py                  # Main Tkinter graphical user interface
├── analyzer.py             # Core forensic engine (EXIF parsing, hashing, logging)
├── evidence_log.csv        # Structured audit ledger for processed evidence
├── requirements.txt        # Project dependencies
├── .gitignore              # Git ignore rules for virtual environments
├── test_img/               # Directory for testing standard image files
└── case_img/               # Directory for official seized case evidence

```

---

## Installation & Setup

Follow these steps to set up and run the environment on a Linux/Kali system:

### 1. Clone the Repository

```bash
git clone [https://github.com/Your-Username/Trace-Sight-Forensics.git](https://github.com/Your-Username/Trace-Sight-Forensics.git)
cd Trace-Sight-Forensics

```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

---

## Usage

1. Ensure your virtual environment is active.
2. Launch the graphical user interface:
```bash
python3 app.py

```


3. Click the **"Select Image Evidence"** button in the desktop window.
4. Navigate to your target directory (such as `case_img/`) and select an image file.
5. Review the instant terminal extraction readout, success pop-up confirmation, and updated `evidence_log.csv` spreadsheet ledger.

---

## Technologies Used

* **Python 3.x**
* **Tkinter** (GUI Framework)
* **Pillow (PIL)** (Image Handling)
* **ExifRead** (Metadata Parsing)
* **Git & GitHub** (Version Control)

```

```

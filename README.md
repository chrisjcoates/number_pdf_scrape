# PDF Order Number Comparator

This utility was created to partially automate a repetitive task I was performing manually at work.

## What It Does

The application compares order numbers between two PDF documents:

1. **Scrapes** both PDFs for order numbers.
2. **Identifies** order numbers present in **PDF 1** that are **missing from PDF 2**.
3. **Outputs** the missing order numbers in a `.csv` file for easy review and further processing.

---

## Features

- Extracts text and parses order numbers from PDF documents
- Compares sets of order numbers for discrepancies
- Exports missing entries to a CSV file
- Saves time and reduces human error in repetitive tasks

---

## Requirements

- python3.13
- PySide6
- Pdfplumber

# Bank-Reconciliation-Algorithm
This project temlate features a discrepancy search algorithm designed to identify inconsistencies between internal financial registers and bank declarations. It includes Python scripts optimized for financial data from Banco del Bajío, S.A. (BanBajío) and Banco Bilbao Vizcaya Argentaria (BBVA México, S.A.).

## Technology Stack  
This project leverages a robust stack of Python libraries:  

- **Pandas:** Data manipulation and analysis.  
- **PyPDF2:** PDF parsing and text extraction.  
- **pdfplumber:** Parsing specific keywords and patterns to extract information from PDF files.  
- **Openpyxl:** Used to generate Excel reports summarizing discrepancies.  
- **Tabulate:** Used for formatting structured data into tables for better readability during debugging or console output.  
- **RegEx:** Regular expressions are used extensively in this project to locate financial movements, dates, and references within unstructured text.
  
## Features
The algorithm automates the reconciliation process by:
1. Extracting financial movements from PDFs and Excel files.
2. Comparing data between internal registers and bank declarations.
3. Identifying and documenting inconsistencies for further review.
4. Generating an Excel report summarizing the discrepancies.

## Directory Overview
PDF_Extraction:
Extracts financial movement details (e.g., values, dates, references) line by line from PDF documents.

PDF2Excel:
Converts data from PDF files into Excel files by extracting relevant financial information.

Excel_Extraction:
Extracts financial movement details by accessing specific columns in Excel files containing financial tables.

Main:
Compares financial movements between the internal register and the bank declaration. Identified discrepancies are stored in a data structure, transformed into dataframes, and exported to a new Excel file.

## Discrepancy Categories
Incomes present in the bank declaration but missing from the internal Excel register.
Outcomes present in the bank declaration but missing from the internal Excel register.
Incomes present in the internal Excel register but missing from the bank declaration.
Outcomes present in the internal Excel register but missing from the bank declaration.

## Limitations and Confidentiality
Due to confidentiality agreements, this repository does not include the processed documents or any sensitive data.

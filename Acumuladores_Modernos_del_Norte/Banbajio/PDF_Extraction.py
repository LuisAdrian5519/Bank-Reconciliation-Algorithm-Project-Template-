# This is a function that extracts monetary data from a PDF file containing bank transactions: Date, Amount, Balance, Reference, and Beneficiary.
# The extraction is executed by analyzing the text content of the PDF file and identifying specific symbols related to monetary transactions ($).
# The function returns the extracted data in separate lists for income and outcome transactions, along with the total income and outcome values.

# External libraries
import PyPDF2

def Value_extraction():
   
   # INSERT DATA HERE  :D
   # Replace the following variables with your specific inputs:
   Nombre_del_archivo_PDF = "My_Bank_register.pdf"        # Name of the PDF file to process.
   Páginas_a_leer = 25                                    # Number of pages to read from the PDF file.
   Datos_a_ignorar_Inicio = 6                             # Lines to ignore at the beggining of the document + 1
   Datos_a_ignorar_Final = 5                              # Lines to ignore at the end of the document

   # Variables declaration

   Movimientos = []                 # Monetary movements
   Ingresos = []                    # Income transactions
   Egresos = []                     # Outcome transactions
   
   Fechas = []                      # Transaction dates
   Fechas_Ingresos = []             # Income transaction dates
   Fechas_Egresos = []              # Outcome transaction dates
   
   Balances = []                    # Account balances extracted from the PDF file
   Lines_count =[]                  # Lines of the PDF file containing monetary data
   Balance_values = []              # Extracts and processes specific balance values
   
   Referencias = []                 # References of the transactions
   Referencias_Ingresos = []        # Income transaction references
   Referencias_Egresos = []         # Outcome transaction references
   
   Beneficiarios = []               # Beneficiaries of the transactions 
   Beneficiario_Ingresos = []       # Income transaction beneficiaries
   Beneficiario_Egresos = []        # Outcome transaction beneficiaries

   # Auxiliar variables declaration
   Movimiento = 0
   Fecha = 0
   Balance = 0
   i = 1

   # PDF Preprocessing - Opening and reading of PDF file
   # Open the specified PDF file in read-binary mode and create a PyPDF2 reader object.
   # You can limit the number of pages to read from the PDF file by setting the Páginas_a_leer variable.

   PDF_File = open(Nombre_del_archivo_PDF, 'rb')
   PDF_reader = PyPDF2.PdfReader(PDF_File)

   Num_Pages = len(PDF_reader.pages)            # Total number of pages in the PDF
   Max_Pages = min(Num_Pages, Páginas_a_leer)   # Limit the number of pages to read

   # PDF Processing - Partitioning, Reading, and Logging
   # Loop through the specified pages and extract text line by line.
   
   # Process each page up to the specified maximum
   for Page in range(Max_Pages):
      # Extract text from the page and split it into lines      
      Page_Object = PDF_reader.pages[Page]
      Text = Page_Object.extract_text()
      Lines = Text.split('\n')
   
      # Process each line to extract transactions containing monetary data
      for idx, Line in enumerate(Lines):
         # This loop checks for lines containing a dollar sign ('$'),
         # which indicates a transaction containing monetary data.
         # extracts transaction values, dates, references, and captures related information.

         if '$' in Line:
            split_line = Line.split()
            dollar_index = split_line.index('$')
            # Extract references & Append to references list
            elements_between = split_line[3:dollar_index]
            Reference = ' '.join(elements_between)
            Referencias.append(Reference)

            # Extract transaction amount & Append to movements list
            Movimiento = Line.split('$')[1].strip()
            Movimiento = float(Movimiento.replace(',', '').replace('-', ''))
            Movimientos.append(Movimiento)
            
            # Extract date & Append to dates list
            Fecha = Line.split()[0]
            Fechas.append(Fecha)

            # Extract balance & Append to balances list            
            Balance = Line.split()[-1]
            Balance = float(Balance.replace(',', ''))
            Balances.append(Balance)

            # Store the full line for later use
            Lines_count.append(Line)

            # Check subsequent lines to find beneficiary information          
            for i in range(1, 4):
               # This nested loop looks ahead up to 3 lines to capture
               # beneficiary information for the current transaction.
               if idx + i < len(Lines):
                  next_line = Lines[idx + i]
                        
                  if 'BENEFICIARIO' in next_line or 'ORDENANTE' in next_line:
                     Beneficiarios.append(next_line)
                     break
                         
                  elif '$' in next_line:
                     Beneficiarios.append('N/A')
                     break


   # Post-Processing of Data Structures
   # Truncate data by ignoring the specified number of lines at the beginning and end.
   
   Movimientos = Movimientos[Datos_a_ignorar_Inicio:]
   Movimientos = Movimientos[:-Datos_a_ignorar_Final]

   Fechas = Fechas[Datos_a_ignorar_Inicio:]
   Fechas = Fechas[:-Datos_a_ignorar_Final]
   
   Balances = Balances[(Datos_a_ignorar_Inicio - 1):]
   Balances = Balances[:-Datos_a_ignorar_Final]
   
   Referencias = Referencias[Datos_a_ignorar_Inicio:]
   Referencias = Referencias[:-Datos_a_ignorar_Final]

   Beneficiarios = Beneficiarios[Datos_a_ignorar_Inicio:]
   Beneficiarios = Beneficiarios[:-Datos_a_ignorar_Final]

   Fechas = [int(char) for char in Fechas]  # Convert dates to integers for processing
   
   for i in range(len(Movimientos)):
      # Separate income and outcomes based on balance comparison      
      if Balances[i + 1] < Balances[i]:
         Egresos.append(Movimientos[i])
         Fechas_Egresos.append(Fechas[i])
         Referencias_Egresos.append(Referencias[i])
         Beneficiario_Egresos.append(Beneficiarios[i])

      else: 
         Ingresos.append(Movimientos[i])
         Fechas_Ingresos.append(Fechas[i])
         Referencias_Ingresos.append(Referencias[i])
         Beneficiario_Ingresos.append(Beneficiarios[i])

   # Extract total income and outcome values from the balance line
   Balance_Line = Lines_count[3]
   Balance_values = Balance_Line.split('$')[1:] 
   Balance_values = [value.strip() for value in Balance_values]
   Ingreso_Total = float(Balance_values[1].replace(',', ''))
   Egreso_Total = float(Balance_values[2].replace(',', ''))
         
   return Ingresos, Egresos, Fechas_Ingresos, Fechas_Egresos, Ingreso_Total, Egreso_Total, Referencias_Ingresos, Referencias_Egresos, Beneficiario_Ingresos, Beneficiario_Egresos


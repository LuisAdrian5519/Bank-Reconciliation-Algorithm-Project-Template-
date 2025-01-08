# This script automates the reconciliation of bank and auxiliary financial records by comparing transaction data 
# and generating an Excel report highlighting matches and inconsistencies.

# External libraries
import pandas as pd

# Local Modules for Data Extraction
import PDF_Extraction as PDF
import Excel_Extraction as Excel

# Configuration: Performance Inputs
Nombre_del_archivo_de_salida = 'Result.xlsx'    # Output Excel file name
Margen_de_error = 1                             # Error Margin of One Unit (Mexican Peso)
Margen_de_error_temporal = 3                    # Error Margin of three days

# Functions

def Comparador(Lista_de_valores_Banco, Lista_de_Fechas_Banco, Lista_de_valores_Auxiliar, Lista_de_Fechas_Auxiliar, Valores_en_ambas_listas, Fechas_en_ambas_listas, Valores_en_ninguna_lista, Fechas_en_ninguna_lista, Referencias, Beneficiarios):
    """
    Compares two lists of financial transactions (bank vs auxiliary data) to identify matches and inconsistencies.
    
    Parameters:
    - Lista_de_valores_Banco: List of monetary values from the bank records.
    - Lista_de_Fechas_Banco: List of corresponding transaction dates from the bank records.
    - Lista_de_valores_Auxiliar: List of monetary values from auxiliary records (e.g., Excel).
    - Lista_de_Fechas_Auxiliar: List of corresponding transaction dates from auxiliary records.
    - Valores_en_ambas_listas: List to store matching monetary values.
    - Fechas_en_ambas_listas: List to store matching transaction dates.
    - Valores_en_ninguna_lista: List to store unmatched monetary values.
    - Fechas_en_ninguna_lista: List to store unmatched transaction dates.
    - Referencias: List of transaction references from bank records.
    - Beneficiarios: List of beneficiaries associated with transactions in bank records.
    """
   
    for i, A in enumerate(Lista_de_valores_Banco):
    
        fecha_A = Lista_de_Fechas_Banco[i]
        Found = False

        for j, B in enumerate(Lista_de_valores_Auxiliar):
       
            fecha_B = Lista_de_Fechas_Auxiliar[j]

            if fechas_dentro_del_margen(fecha_A, fecha_B, Margen_de_error_temporal) and valores_dentro_del_margen(A, B, Margen_de_error) and (A not in Valores_en_ambas_listas or Lista_de_Fechas_Banco[i] not in Fechas_en_ambas_listas or Lista_de_valores_Banco.count(A) > 1):

                # Match found
                Valores_en_ambas_listas.append(A)
                Fechas_en_ambas_listas.append(fecha_A)
                Found = True
                print(f"\033[1mConsistente     Banco  |  Auxiliar \033[0m ")
                print(f"Cantidad:     {A}  -  {B}  ")
                print(f"Fecha:      {fecha_A}   -   {fecha_B}")
                print("")

                # Mark the record as matched in auxiliary data
                Lista_de_valores_Auxiliar[j] = 0
                Referencias[i] = "0"
                Beneficiarios[i] = "0"
                break

        if not Found:
            # Record is inconsistent
            Valores_en_ninguna_lista.append(A)
            Fechas_en_ninguna_lista.append(fecha_A)
            print(f"\033[1mInconsistente:\033[0m {A}")
            print(f"Fecha: {Lista_de_Fechas_Banco[i]}")
            print("")
           
    print("")
    print("-------------------------------------------------------------------------------------------------")
    print("")
        
    return Valores_en_ambas_listas, Fechas_en_ambas_listas, Valores_en_ninguna_lista, Fechas_en_ninguna_lista

def fechas_dentro_del_margen(fecha1, fecha2, margen):
    """
    Checks if two dates are within the specified margin of error.
    """
    return abs(fecha1 - fecha2) <= margen or abs(fecha1 - fecha2) == 0 

def valores_dentro_del_margen(valor1, valor2, margen):
    """
    Checks if two monetary values are within the specified margin of error.
    """
    return abs(valor1 - valor2) <= margen

def Dataframe_Construction(Fechas_en_ninguna_lista, valores_en_ninguna_lista, Referencias, Beneficiarios):
    """
    Creates a DataFrame for inconsistent records.
    """
    Inconsistencias_Dataframe = {
    'Fechas': Fechas_en_ninguna_lista,
    'Importe': valores_en_ninguna_lista,
    'Referencias': Referencias, 
    'Beneficiario / Ordenante': Beneficiarios}
    
    Inconsistencias_Dataframe = pd.DataFrame(Inconsistencias_Dataframe)
    
    return Inconsistencias_Dataframe

def Excel_Construction(Table_title, Tabla_Inconsistencias):
    """
    Constructs an Excel-compatible DataFrame with a general header and inconsistency data.
    """  
    General_header = pd.DataFrame([[Table_title, "", "", ""]],
    columns = ['Fechas', 'Importe', 'Referencias', 'Beneficiario / Ordenante'])
    
    Tabla_Inconsistencias_Excel = pd.concat([General_header, Tabla_Inconsistencias], ignore_index = True)
    
    return Tabla_Inconsistencias_Excel

# Data Set-up
"""
1. PDF data extraction
2. Excel data extraction
"""

Lista_de_valores_MNA_BBVA_Ingresos, Lista_de_valores_MNA_BBVA_Egresos, Lista_de_valores_MNA_BBVA_Fechas_Ingresos, Lista_de_valores_MNA_BBVA_Fechas_Egresos, Ingreso_Total, Egreso_Total, Referencias_MNA_BBVA_Ingresos, Referencias_MNA_BBVA_Egresos, Beneficiarios_MNA_BBVA_Ingresos, Beneficiarios_MNA_BBVA_Egresos = PDF.Value_extraction()
Lista_de_valores_Auxiliar_Ingresos, Lista_de_valores_Auxiliar_Egresos, Lista_de_valores_Auxiliar_Fechas_Ingresos, Lista_de_valores_Auxiliar_Fechas_Egresos, Referencias_Auxiliar_Ingresos, Referencias_Auxiliar_Egresos, Beneficiarios_Auxiliar_Ingresos, Beneficiarios_Auxiliar_Egresos = Excel.Value_extraction()

print("")
print("            Conciliación Bancaria")
print("")

# Comparison between total declarated and individual recorded financial movements
print("")
print("Antes de comenzar...")
print("")

Suma_Ingresos_MNA_BBVA = sum(Lista_de_valores_MNA_BBVA_Ingresos)
Suma_Egresos_MNA_BBVA = sum(Lista_de_valores_MNA_BBVA_Egresos)

print(f"\033[1m                    Banco  |  Base de datos Capturada \033[0m")
print("")
print(f"Ingresos:     {Ingreso_Total}  -  {Suma_Ingresos_MNA_BBVA}")
print("")
print(f"Diferencia:              {Ingreso_Total - Suma_Ingresos_MNA_BBVA}")
print("---------------------------------------------------------")
print("")
print(f"Egresos:     {Egreso_Total}  -  {Suma_Egresos_MNA_BBVA}")
print("")
print(f"Diferencia:              {Egreso_Total - Suma_Egresos_MNA_BBVA}")
print("---------------------------------------------------------")
print("")

# Variables declaration

# BBVA Income
Ingresos_en_ambas_listas_MNA_BBVA = []          # Matching income values found in both Bank and Auxiliary records
Fechas_en_ambas_listas_Ingresos_MNA_BBVA = []   # Matching income dates for the values above
Valores_en_ninguna_lista_MNA_BBVA_Ingresos = [] # Income values found only in Bank records
Fechas_en_ninguna_lista_Ingresos_MNA_BBVA = []  # Dates corresponding to income found only in Bank records

# Excel Income
Ingresos_en_ambas_listas_auxiliar = []          # Matching income values found in both Auxiliary and Bank records
Fechas_en_ambas_listas_Ingresos_auxiliar = []   # Matching income dates for the values above
Valores_en_ninguna_lista_auxiliar_Ingresos = [] # Income values found only in Auxiliary records
Fechas_en_ninguna_lista_Ingresos_auxiliar = []  # Dates corresponding to income found only in Auxiliary records

# BBVA Outcome
Egresos_en_ambas_listas_MNA_BBVA = []           # Matching outcome values found in both Bank and Auxiliary records
Fechas_en_ambas_listas_Egresos_MNA_BBVA = []    # Matching outcome dates for the values above
Valores_en_ninguna_lista_MNA_BBVA_Egresos = []  # Outcome values found only in Bank records
Fechas_en_ninguna_lista_Egresos_MNA_BBVA = []   # Dates corresponding to outcome found only in Bank records

# Excel Outcome
Egresos_en_ambas_listas_auxiliar = []           # Matching outcome values found in both Auxiliary and Bank records
Fechas_en_ambas_listas_Egresos_auxiliar = []    # Matching outcome dates for the values above
Valores_en_ninguna_lista_auxiliar_Egresos = []  # Outcome values found only in Auxiliary records
Fechas_en_ninguna_lista_Egresos_auxiliar = []   # Dates corresponding to outcome found only in Auxiliary records

# Auxiliary variables
Lista_de_valores_Auxiliar_Ingresos_Copia = Lista_de_valores_Auxiliar_Ingresos.copy()
Lista_de_valores_Auxiliar_Egresos_Copia = Lista_de_valores_Auxiliar_Egresos.copy()

# Work Cycle 1: Income Recorded in the Bank but not in Excel
Comparador(Lista_de_valores_MNA_BBVA_Ingresos, Lista_de_valores_MNA_BBVA_Fechas_Ingresos, Lista_de_valores_Auxiliar_Ingresos_Copia, Lista_de_valores_Auxiliar_Fechas_Ingresos, Ingresos_en_ambas_listas_MNA_BBVA, Fechas_en_ambas_listas_Ingresos_MNA_BBVA, Valores_en_ninguna_lista_MNA_BBVA_Ingresos, Fechas_en_ninguna_lista_Ingresos_MNA_BBVA, Referencias_MNA_BBVA_Ingresos, Beneficiarios_MNA_BBVA_Ingresos)

# Remove matched records from reference and beneficiary lists
Referencias_MNA_BBVA_Ingresos = [x for x in Referencias_MNA_BBVA_Ingresos if x != "0"]
Beneficiarios_MNA_BBVA_Ingresos = [x for x in Beneficiarios_MNA_BBVA_Ingresos if x != "0"]

# Generate DataFrame for inconsistencies and prepare Excel-compatible structure
Tabla_Inconsistencias_Ingresos_MNA_BBVA = Dataframe_Construction(Fechas_en_ninguna_lista_Ingresos_MNA_BBVA, Valores_en_ninguna_lista_MNA_BBVA_Ingresos, Referencias_MNA_BBVA_Ingresos, Beneficiarios_MNA_BBVA_Ingresos)
Tabla_Inconsistencias_Ingresos_MNA_BBVA = Excel_Construction("Ingresos registrados en Banco y no en Auxiliar", Tabla_Inconsistencias_Ingresos_MNA_BBVA)


# Work Cycle 2: Outcome Recorded in the Bank but not in Excel
Comparador(Lista_de_valores_MNA_BBVA_Egresos, Lista_de_valores_MNA_BBVA_Fechas_Egresos, Lista_de_valores_Auxiliar_Egresos_Copia, Lista_de_valores_Auxiliar_Fechas_Egresos, Egresos_en_ambas_listas_MNA_BBVA, Fechas_en_ambas_listas_Egresos_MNA_BBVA, Valores_en_ninguna_lista_MNA_BBVA_Egresos, Fechas_en_ninguna_lista_Egresos_MNA_BBVA, Referencias_MNA_BBVA_Egresos, Beneficiarios_MNA_BBVA_Egresos)
# Remove matched records from reference and beneficiary lists
Referencias_MNA_BBVA_Egresos = [x for x in Referencias_MNA_BBVA_Egresos if x != "0"]
Beneficiarios_MNA_BBVA_Egresos = [x for x in Beneficiarios_MNA_BBVA_Egresos if x != "0"]

# Generate DataFrame for inconsistencies and prepare Excel-compatible structure
Tabla_Inconsistencias_Egresos_MNA_BBVA = Dataframe_Construction(Fechas_en_ninguna_lista_Egresos_MNA_BBVA, Valores_en_ninguna_lista_MNA_BBVA_Egresos, Referencias_MNA_BBVA_Egresos, Beneficiarios_MNA_BBVA_Egresos)
Tabla_Inconsistencias_Egresos_MNA_BBVA = Excel_Construction("Egresos registrados en Banco y no en Auxiliar", Tabla_Inconsistencias_Egresos_MNA_BBVA)


# Work Cycle 3: Income Recorded in Excel but not in the Bank
Comparador(Lista_de_valores_Auxiliar_Ingresos, Lista_de_valores_Auxiliar_Fechas_Ingresos, Lista_de_valores_MNA_BBVA_Ingresos, Lista_de_valores_MNA_BBVA_Fechas_Ingresos, Ingresos_en_ambas_listas_auxiliar, Fechas_en_ambas_listas_Ingresos_auxiliar, Valores_en_ninguna_lista_auxiliar_Ingresos, Fechas_en_ninguna_lista_Ingresos_auxiliar, Referencias_Auxiliar_Ingresos, Beneficiarios_Auxiliar_Ingresos)
# Remove matched records from reference and beneficiary lists
Referencias_Auxiliar_Ingresos = [x for x in Referencias_Auxiliar_Ingresos if x != "0"]
Beneficiarios_Auxiliar_Ingresos = [x for x in Beneficiarios_Auxiliar_Ingresos if x != "0"]

# Generate DataFrame for inconsistencies and prepare Excel-compatible structure
Tabla_Inconsistencias_Ingresos_Auxiliar = Dataframe_Construction(Fechas_en_ninguna_lista_Ingresos_auxiliar, Valores_en_ninguna_lista_auxiliar_Ingresos, Referencias_Auxiliar_Ingresos, Beneficiarios_Auxiliar_Ingresos)
Tabla_Inconsistencias_Ingresos_Auxiliar = Excel_Construction("Ingresos registrados en Auxiliar y no en Banco", Tabla_Inconsistencias_Ingresos_Auxiliar)


# Work Cycle 3: Outcome Recorded in Excel but not in the Bank
Comparador(Lista_de_valores_Auxiliar_Egresos, Lista_de_valores_Auxiliar_Fechas_Egresos, Lista_de_valores_MNA_BBVA_Egresos, Lista_de_valores_MNA_BBVA_Fechas_Egresos, Egresos_en_ambas_listas_auxiliar, Fechas_en_ambas_listas_Egresos_auxiliar, Valores_en_ninguna_lista_auxiliar_Egresos, Fechas_en_ninguna_lista_Egresos_auxiliar, Referencias_Auxiliar_Egresos, Beneficiarios_Auxiliar_Egresos)
# Remove matched records from reference and beneficiary lists
Referencias_Auxiliar_Egresos = [x for x in Referencias_Auxiliar_Egresos if x != "0"]
Beneficiarios_Auxiliar_Egresos = [x for x in Beneficiarios_Auxiliar_Egresos if x != "0"]

# Generate DataFrame for inconsistencies and prepare Excel-compatible structure
Tabla_Inconsistencias_Egresos_Auxiliar = Dataframe_Construction(Fechas_en_ninguna_lista_Egresos_auxiliar, Valores_en_ninguna_lista_auxiliar_Egresos, Referencias_Auxiliar_Egresos, Beneficiarios_Auxiliar_Egresos)
Tabla_Inconsistencias_Egresos_Auxiliar = Excel_Construction("Egresos registrados en Auxiliar y no en Banco", Tabla_Inconsistencias_Egresos_Auxiliar)

# Excel file export
# Create a consolidated Excel file with inconsistencies organized in separate sheets
with pd.ExcelWriter(Nombre_del_archivo_de_salida) as writer:
    Tabla_Inconsistencias_Ingresos_MNA_BBVA.to_excel(writer, sheet_name = "Ingresos Banco", index = False, header = True)
    Tabla_Inconsistencias_Egresos_MNA_BBVA.to_excel(writer, sheet_name = "Egresos Banco", index = False, header = True)
    Tabla_Inconsistencias_Ingresos_Auxiliar.to_excel(writer, sheet_name = "Ingresos Auxiliar", index = False, header = True)
    Tabla_Inconsistencias_Egresos_Auxiliar.to_excel(writer, sheet_name = "Egresos Auxiliar", index = False, header = True)

print("")
print("Archivo Excel exportado con éxito") # Success message for Excel export
print("")
print("")

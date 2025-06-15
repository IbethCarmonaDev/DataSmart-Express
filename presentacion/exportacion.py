import pandas as pd
import os
from datetime import datetime

# Para PDF (puedes ampliar con fpdf, reportlab, etc.)
from fpdf import FPDF

# --- EXPORTAR A EXCEL ---
def exportar_excel(df_estado, df_kpis, año, mes):
    nombre_archivo = f"Reporte_Financiero_{año}_{mes:02}.xlsx"
    ruta_salida = os.path.join("salidas", nombre_archivo)
    os.makedirs("salidas", exist_ok=True)

    with pd.ExcelWriter(ruta_salida, engine="openpyxl") as writer:
        df_estado.to_excel(writer, sheet_name="Estado", index=False)
        df_kpis.to_excel(writer, sheet_name="KPIs", index=False)

    return ruta_salida

# --- EXPORTAR A PDF ---
def exportar_pdf(df_estado, df_kpis, año, mes):
    nombre_archivo = f"Reporte_Financiero_{año}_{mes:02}.pdf"
    ruta_salida = os.path.join("salidas", nombre_archivo)
    os.makedirs("salidas", exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Reporte Financiero - {año} / {mes}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="KPIs:", ln=True)
    for _, row in df_kpis.iterrows():
        pdf.cell(200, 8, txt=f"{row['GRUPO']}: Mensual={row['MENSUAL']} | Anual={row['ANUAL']}", ln=True)

    pdf.output(ruta_salida)
    return ruta_salida

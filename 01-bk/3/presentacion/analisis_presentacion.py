import pandas as pd

def generar_html_estado_resultados(df, df_kpis_tarjeta):
    tipo_kpis = {row["GRUPO"]: str(row.get("TIPO_DATO", "MONEDA")).upper() for _, row in df_kpis_tarjeta.iterrows()}

    def formatear(valor, grupo):
        tipo = tipo_kpis.get(grupo, "MONEDA")
        if pd.isnull(valor): return ""
        if tipo == "PORCENTAJE": return f"{valor:.2f}%"
        elif tipo == "DECIMAL": return f"{valor:.2f}"
        else: return f"$ {valor:,.0f}"

    df = df.copy()
    if "AÑO" in df.columns: df.drop(columns=["AÑO"], inplace=True)
    if "MES" in df.columns: df.drop(columns=["MES"], inplace=True)

    html = """
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        th {
            background-color: #f2f2f2;
            text-align: center;
        }
        td:nth-child(1), td:nth-child(2) {
            text-align: left;
        }
        td:nth-child(3), td:nth-child(4) {
            text-align: right;
        }
    </style>
    <table>
        <thead>
            <tr>
                <th>Grupo</th>
                <th>Cuenta</th>
                <th>Mensual</th>
                <th>Anual</th>
            </tr>
        </thead>
        <tbody>
    """
    for _, row in df.iterrows():
        html += "<tr>"
        html += f"<td>{row.get('GRUPO', '')}</td>"
        html += f"<td>{row.get('CUENTA', '')}</td>"
        html += f"<td>{formatear(row.get('MENSUAL', ''), row.get('GRUPO', ''))}</td>"
        html += f"<td>{formatear(row.get('ANUAL', ''), row.get('GRUPO', ''))}</td>"
        html += "</tr>"
    html += "</tbody></table>"
    return html

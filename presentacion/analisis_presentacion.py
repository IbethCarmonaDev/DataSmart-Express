import pandas as pd
import numpy as np
import re

def formato_moneda(valor):
    if pd.isna(valor) or valor == 0:
        return "0"
    return f"$ {valor:,.0f}"



def generar_html_estado_resultados(df: pd.DataFrame, df_kpis: pd.DataFrame) -> str:
    df_formateado = df.copy()
    df_formateado = df_formateado.drop(columns=[col for col in ["AÑO", "MES"] if col in df_formateado.columns])
    columnas_valores = [col for col in df_formateado.columns if col not in ["GRUPO", "CUENTA"]]

    # Crear diccionario para mapear cada KPI a su tipo de dato
    tipos_kpis = {}
    if isinstance(df_kpis, pd.DataFrame) and not df_kpis.empty:
        if "MOSTRAR_EN_PG" in df_kpis.columns:
            df_kpis_filtrado = df_kpis[df_kpis['MOSTRAR_EN_PG'] == 1]
        else:
            df_kpis_filtrado = df_kpis

        tipos_kpis = {
            str(row["KPI"]).strip().lower(): str(row.get("TIPO_DATO", "MONEDA")).upper()
            for _, row in df_kpis_filtrado.iterrows()
        }

    def formatear(valor, grupo):
        tipo = tipos_kpis.get(str(grupo).strip().lower(), "MONEDA")
        ##print("DEBUG ➤", grupo, tipo, valor)

        try:
            valor = float(str(valor).replace("$", "").replace(",", "").replace("%", "").strip())
        except:
            return valor

        if valor is None or str(valor).lower() in ["nan", "none", ""]:
            return ""

        if tipo == "PORCENTAJE":
            valor_ajustado = valor / 100 if valor > 100 else valor
            return f"{valor_ajustado:.2f}%"
        elif tipo == "DECIMAL":
            return f"{valor:.2f}"
        else:
            return f"$ {valor:,.0f}"

    for idx, row in df_formateado.iterrows():
        grupo = str(row.get("GRUPO", ""))
        for col in columnas_valores:
            valor = row[col]
            df_formateado.at[idx, col] = formatear(valor, grupo)

    df_formateado.columns = [col.capitalize() for col in df_formateado.columns]

    if "Grupo" in df_formateado.columns:
        df_formateado["Grupo"] = df_formateado["Grupo"].astype(str).str.capitalize()
    if "Cuenta" in df_formateado.columns:
        df_formateado["Cuenta"] = df_formateado["Cuenta"].astype(str).str.capitalize()

    html = '''
    <style>
        .scroll-table-container {
            overflow-x: auto;
            max-width: 100%;
            border: 1px solid #ddd;
            font-family: Arial, sans-serif;
            font-size: 12px;
        }
        table.custom-table {
            border-collapse: collapse;
            width: max-content;
            min-width: 100%;
        }
        table.custom-table th, table.custom-table td {
            padding: 4px 8px;
            border: 1px solid #ccc;
            text-align: right;
            white-space: nowrap;
        }
        table.custom-table th {
            position: sticky;
            top: 0;
            background-color: #003366;
            color: white;
            z-index: 1;
            text-align: center;
            font-weight: bold;
        }
        table.custom-table td:first-child,
        table.custom-table td:nth-child(2),
        table.custom-table th:first-child,
        table.custom-table th:nth-child(2) {
            position: sticky;
            left: 0;
            background-color: #fff;
            z-index: 2;
            text-align: left;
            font-weight: bold;
        }
        table.custom-table tr.total-row td {
            background-color: #e6f0ff;
            font-weight: bold;
        }
        table.custom-table tr.kpi-row td {
            background-color: #e1f5e1;
            font-weight: bold;
        }
    </style>
    <div class="scroll-table-container">
    '''

    def clasificar_fila(grupo):
        grupo_lower = str(grupo).strip().lower()
        if grupo_lower.startswith("total "):
            return "total-row"
        if grupo_lower in tipos_kpis:
            return "kpi-row"
        return ""

    html += "<table class='custom-table'>"
    html += "<thead><tr>" + "".join(f"<th>{col}</th>" for col in df_formateado.columns) + "</tr></thead><tbody>"

    for _, row in df_formateado.iterrows():
        clase = clasificar_fila(row["Grupo"])
        html += f"<tr class='{clase}'>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"

    html += "</tbody></table></div>"

    #if isinstance(df_kpis, pd.DataFrame) and "GRUPO" in df_kpis.columns and "MOSTRAR_EN_PG" in df_kpis.columns:
    if isinstance(df_kpis, pd.DataFrame) and "GRUPO" in df_kpis.columns and "MOSTRAR_EN_PG" in df_kpis.columns:
        kpis_excel = set(df_kpis[df_kpis["MOSTRAR_EN_PG"] == 1]["GRUPO"].str.strip().str.upper())
        grupos_df = set(df["GRUPO"].str.strip().str.upper()) if "GRUPO" in df.columns else set()
        no_detectados = kpis_excel - grupos_df
        if no_detectados:
            print("⚠️ KPIs con MOSTRAR_EN_PG=1 que no aparecen en el DataFrame:")
            for kpi in no_detectados:
                print("   ➤", kpi)

    return html


def generar_html_estado_resultados_anual(df: pd.DataFrame, kpi_destacados: list = []) -> str:
    df_formateado = df.copy()
    columnas_valores = [col for col in df.columns if col not in ["GRUPO", "CUENTA", "TIPO_DATO"]]
    columnas_ordenadas = [col for col in columnas_valores if col.upper() != "ACUMULADO"]

    # Convertir columnas de valores a object para permitir texto
    for col in columnas_valores:
        df_formateado[col] = df_formateado[col].astype("object")

    variaciones = {}

    for idx, row in df.iterrows():
        grupo = str(row.get("GRUPO", "")).upper()
        if grupo in [k.upper() for k in kpi_destacados]:
            variaciones[idx] = {}
            for i in range(1, len(columnas_ordenadas)):
                actual = row[columnas_ordenadas[i]]
                anterior = row[columnas_ordenadas[i - 1]]
                if isinstance(actual, (int, float)) and isinstance(anterior, (int, float)):
                    if actual > anterior:
                        variaciones[idx][columnas_ordenadas[i]] = "⬆️"
                    elif actual < anterior:
                        variaciones[idx][columnas_ordenadas[i]] = "🔻"
            if "ACUMULADO" in columnas_valores:
                acumulado_actual = row.get("ACUMULADO", None)
                acumulado_previo = sum(
                    [row.get(col, 0) for col in columnas_ordenadas if isinstance(row.get(col, 0), (int, float))]
                )
                if isinstance(acumulado_actual, (int, float)) and isinstance(acumulado_previo, (int, float)):
                    if acumulado_actual > acumulado_previo:
                        variaciones[idx]["ACUMULADO"] = "⬆️"
                    elif acumulado_actual < acumulado_previo:
                        variaciones[idx]["ACUMULADO"] = "🔻"

    def formatear(valor, tipo, icono=""):
        if pd.isna(valor) or valor in [float("inf"), float("-inf")]:
            return ""
        if tipo == "PORCENTAJE":
            return f"{icono} {valor:.2f}%"
        elif tipo == "DECIMAL":
            return f"{icono} {valor:.2f}"
        else:
            return f"{icono} $ {valor:,.0f}"

    for idx, row in df.iterrows():
        tipo = str(row.get("TIPO_DATO", "MONEDA")).upper()
        for col in columnas_valores:
            valor = row[col]
            icono = variaciones.get(idx, {}).get(col, "")
            df_formateado.at[idx, col] = formatear(valor, tipo, icono)

    if "TIPO_DATO" in df_formateado.columns:
        df_formateado = df_formateado.drop(columns=["TIPO_DATO"])

    nuevas_columnas = []
    for col in df_formateado.columns:
        if col.lower() in ["grupo", "cuenta"]:
            nuevas_columnas.append(col.capitalize())
        elif col.lower() == "acumulado":
            nuevas_columnas.append("📊 Acumulado")
        elif col.lower() in ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                             "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]:
            nuevas_columnas.append(f"📅 {col.capitalize()}")
        else:
            nuevas_columnas.append(col.capitalize())

    df_formateado.columns = nuevas_columnas

    html = '''
    <style>
        .scroll-table-container {
            overflow-x: auto;
            max-width: 100%;
            border: 1px solid #ddd;
            font-family: Arial, sans-serif;
            font-size: 12px;
        }
        table.custom-table {
            border-collapse: collapse;
            width: max-content;
            min-width: 100%;
        }
        table.custom-table th, table.custom-table td {
            padding: 4px 8px;
            border: 1px solid #ccc;
            text-align: right;
            white-space: nowrap;
        }
        table.custom-table th {
            position: sticky;
            top: 0;
            background-color: #003366;
            color: white;
            z-index: 3;
            text-align: center;
            font-weight: bold;
        }
        table.custom-table td:first-child,
        table.custom-table td:nth-child(2) {
            position: sticky;
            left: 0;
            background-color: #fff;
            z-index: 2;
            text-align: left;
            font-weight: bold;
        }
        table.custom-table th:first-child,
        table.custom-table th:nth-child(2) {
            position: sticky;
            left: 0;
            background-color: #003366;
            color: white;
            z-index: 4;
        }
        table.custom-table tr.total-row td {
            background-color: #e6f0ff;
            font-weight: bold;
        }
        table.custom-table tr.kpi-row td {
            background-color: #e1f5e1;
            font-weight: bold;
        }
    </style>
    <div class="scroll-table-container">
    '''

    def clasificar_fila(grupo):
        if str(grupo).upper() in [k.upper() for k in kpi_destacados]:
            return "kpi-row"
        elif str(grupo).lower().startswith("total "):
            return "total-row"
        return ""

    html += "<table class='custom-table'>"
    html += "<thead><tr>" + "".join(f"<th>{col}</th>" for col in df_formateado.columns) + "</tr></thead><tbody>"

    for _, row in df_formateado.iterrows():
        clase = clasificar_fila(row["Grupo"])
        html += f"<tr class='{clase}'>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"

    html += "</tbody></table></div>"
    return html


def generar_html_estado_resumido(df_estado, df_kpis_filtrados=None):
    import pandas as pd

    df_resumen = df_estado[df_estado["TIPO"] == "CUENTA"].copy()

    # Agrupar por GRUPO y calcular totales
    df_grupos = df_resumen.groupby("GRUPO")[["MENSUAL", "ANUAL"]].sum().reset_index()

    html = """
    <style>
        .resumen-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        .resumen-table th, .resumen-table td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: right;
        }
        .resumen-table th {
            background-color: #f4f4f4;
            color: #333;
        }
        .resumen-table td:first-child {
            text-align: left;
            font-weight: 600;
        }
    </style>
    <table class='resumen-table'>
        <tr>
            <th>Grupo</th>
            <th>Mes actual</th>
            <th>Acumulado anual</th>
        </tr>
    """

    for _, row in df_grupos.iterrows():
        grupo = row["GRUPO"]
        mensual = f"$ {row['MENSUAL']:,.0f}"
        anual = f"$ {row['ANUAL']:,.0f}"
        html += f"""
        <tr>
            <td>{grupo}</td>
            <td>{mensual}</td>
            <td>{anual}</td>
        </tr>
        """

    html += "</table>"
    return html

# Funcion creada para generar analisis mas avanzados
# Creada por: Ibeth Carmona - IA
# Fecha de Creación: Junio 7-2025
# All rights reserved

import pandas as pd


def generar_conclusiones_avanzadas(df_kpis, df_estado, archivo_parametros, año, mes):
    frases = []

    # Cargar hoja TARJETAS para saber qué KPIs mostrar
    df_tarjetas = pd.read_excel(archivo_parametros, sheet_name="TARJETAS")
    df_tarjetas.columns = df_tarjetas.columns.str.strip().str.upper()

    # Determinar mes anterior y año anterior si aplica
    if mes == 1:
        mes_anterior = 12
        año_anterior = año - 1
    else:
        mes_anterior = mes - 1
        año_anterior = año

    # Construir historial mensual a partir de df_estado
    df_estado_filtrado = df_estado[["GRUPO", "AÑO", "MES", "MENSUAL"]].copy()
    df_estado_filtrado.columns = ["KPI", "AÑO", "MES", "VALOR"]
    df_estado_filtrado["KPI"] = df_estado_filtrado["KPI"].str.upper()

    tabla = []

    for _, fila in df_tarjetas.iterrows():
        nombre_kpi = str(fila["KPI"]).upper().strip()
        tipo_dato = str(fila.get("TIPO_DATO", "MONEDA")).upper()

        fila_actual = df_kpis[df_kpis["GRUPO"].str.upper() == nombre_kpi]
        valor_actual = fila_actual["MENSUAL"].values[0] if not fila_actual.empty else None

        fila_anterior = df_estado_filtrado[
            (df_estado_filtrado["KPI"] == nombre_kpi) &
            (df_estado_filtrado["AÑO"] == año_anterior) &
            (df_estado_filtrado["MES"] == mes_anterior)
        ]
        valor_anterior = fila_anterior["VALOR"].values[0] if not fila_anterior.empty else None

        if valor_actual is not None and valor_anterior is not None:
            variacion_abs = valor_actual - valor_anterior
            variacion_pct = (variacion_abs / valor_anterior * 100) if valor_anterior != 0 else 0
            tabla.append({
                "KPI": nombre_kpi,
                "Mes Actual": valor_actual,
                "Mes Anterior": valor_anterior,
                "Variacion": variacion_abs,
                "Variacion %": variacion_pct,
                "TIPO": tipo_dato
            })

    if not tabla:
        return pd.DataFrame(), "No se encontraron KPIs definidos para análisis avanzado."

    df_comparativo = pd.DataFrame(tabla)
    for _, row in df_comparativo.iterrows():
        kpi = row["KPI"]
        delta = row["Variacion"]
        pct = row["Variacion %"]
        tipo = row["TIPO"]
        if pct == 0:
            frases.append(f"🔹 El indicador '{kpi}' no tuvo variación respecto al mes anterior.")
        elif pct > 0:
            frases.append(f"📈 El KPI '{kpi}' aumentó un {pct:.2f}% respecto al mes anterior.")
        else:
            frases.append(f"📉 El KPI '{kpi}' disminuyó un {abs(pct):.2f}% respecto al mes anterior.")

    return df_comparativo, "\n\n".join(frases)

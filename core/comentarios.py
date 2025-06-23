import pandas as pd
import numpy as np
import openai
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
#openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()  # usa automáticamente tu OPENAI_API_KEY del entorno

def generar_comentario_logico(df, kpi_nombre, modo):
    try:
        if modo.upper() == "ANUAL":
            columnas_mes = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
                            "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
            fila = df[df["GRUPO"].str.upper() == kpi_nombre.upper()]
            if fila.empty:
                return None
            valores = fila[columnas_mes].values.flatten()
            valores = valores[valores != 0]
            if len(valores) < 2:
                return None
            variacion = (valores[-1] - valores[-2]) / valores[-2] if valores[-2] != 0 else 0
            if variacion > 0:
                return f"El valor de {kpi_nombre} aumentó un {variacion:.1%} respecto al mes anterior."
            elif variacion < 0:
                return f"El valor de {kpi_nombre} disminuyó un {abs(variacion):.1%} respecto al mes anterior."
            else:
                return f"No hubo variación significativa en {kpi_nombre} respecto al mes anterior."
        else:
            return None
    except Exception:
        return None

def generar_comentario_logico_anual(df, kpi_nombre, mes_actual=None, anio_actual=None):
    orden_meses = [
        "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
        "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
    ]

    frases = []
    df = df.copy()
    df.columns = [col.upper() for col in df.columns]

    if "AÑO" not in df.columns and anio_actual is not None:
        df["AÑO"] = anio_actual

    fila_kpi = df[df["GRUPO"].str.upper() == kpi_nombre.upper()]
    if fila_kpi.empty:
        return []

    valores = fila_kpi[orden_meses].iloc[0].apply(pd.to_numeric, errors='coerce')
    mes_max = valores.idxmax()
    valor_max = valores.max()
    frases.append(f"🔹 El valor más alto de **{kpi_nombre.title()}** se registró en **{mes_max.title()}** con **${valor_max:,.0f}**.")

    if mes_actual and anio_actual:
        idx = orden_meses.index(mes_actual.upper())
        if idx == 0:
            mes_anterior = "DICIEMBRE"
            anio_anterior = anio_actual - 1
        else:
            mes_anterior = orden_meses[idx - 1]
            anio_anterior = anio_actual

        fila_actual = df[(df["GRUPO"].str.upper() == kpi_nombre.upper()) & (df["AÑO"] == anio_actual)]
        fila_anterior = df[(df["GRUPO"].str.upper() == kpi_nombre.upper()) & (df["AÑO"] == anio_anterior)]

        if not fila_actual.empty and not fila_anterior.empty:
            try:
                valor_act = float(fila_actual[mes_actual.upper()].values[0])
                valor_ant = float(fila_anterior[mes_anterior.upper()].values[0]) if mes_anterior.upper() in fila_anterior else 0

                if pd.notnull(valor_act) and pd.notnull(valor_ant) and valor_ant != 0:
                    variacion = (valor_act - valor_ant) / abs(valor_ant)
                    direccion = "subió" if variacion > 0 else "bajó"
                    frases.append(
                        #f"🔹 Durante el mes de **{mes_actual.title()}**, el **{kpi_nombre.title()}** fue de **${valor_act:,.0f}** y {direccion} un **{abs(variacion * 100):.1f}** respecto a **{mes_anterior.title()}** (**${valor_ant:,.0f}**)."
                        f"🔹 Durante el mes de **{mes_actual.title()}**, el **{kpi_nombre.title()}** fue de **${valor_act:,.0f}** y {direccion} un {abs(variacion * 100):.1f} % respecto a **{mes_anterior.title()}** que fue de {valor_ant:,.0f} "
                    )
            except Exception as e:
                frases.append("⚠️ Error al generar el comentario: " + str(e))

    return frases

def OLDgenerar_comentario_gpt(df, kpi_nombre, modo, ubicacion="", modelo="gpt-3.5-turbo", log_path="logs/consumo_gpt.csv"):
#def generar_comentario_gpt(df, kpi_nombre, modo, ubicacion="", modelo="gpt-4", log_path="logs/consumo_gpt.csv"):
    try:

        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        df.columns = [col.upper() for col in df.columns]

        if modo.upper() == "ANUAL":
            columnas_mes = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
                            "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
            fila = df[df["GRUPO"].str.upper() == kpi_nombre.upper()]
            if fila.empty:
                return None

            # serie = fila[columnas_mes].values.flatten().tolist()
            columnas_filtradas = [mes for mes in columnas_mes if df[mes].sum() != 0]
            serie = fila[columnas_filtradas].values.flatten().tolist()

            serie_format = [
                f"{mes.title()}: ${float(fila[mes].iloc[0]):,.0f}"
                for mes in columnas_filtradas
                if pd.notnull(fila[mes].iloc[0])
            ]

            # prompt = (
            #     f"Actúa como un analista financiero con experiencia. Con base en la siguiente serie mensual de datos "
            #     f"del KPI '{kpi_nombre}':\n\n{serie}\n\n"
            #     f"Redacta un análisis ejecutivo claro y profesional para gerencia. "
            #     f"Incluye si hay crecimiento, caídas, estacionalidades, meses críticos o mejoras. "
            #     f"Usa un lenguaje técnico pero fácil de entender, y enfócate en puntos relevantes para la toma de decisiones. "
            #     f"El análisis debe ser breve pero más enriquecido que una sola frase."
            # )

            prompt = (
                f"Actúa como un analista financiero con experiencia. Con base en la siguiente serie mensual de datos "
                f"del KPI '{kpi_nombre}':\\n\\n{serie_format}\\n\\n"
                f"Redacta un análisis ejecutivo claro y profesional para gerencia. "
                f"Incluye si hay crecimiento, caídas, estacionalidades, meses críticos o mejoras. "
                f"Usa nombres de los meses, el símbolo '$' para los valores, y evita expresiones como 'primer mes'. "
                f"El análisis debe ser breve pero enriquecido y útil para la toma de decisiones."
            )

            response = client.chat.completions.create(
                model=modelo,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=300
            )
            comentario = response.choices[0].message.content.strip()

            tokens = response.usage.total_tokens
            costo = tokens / 1000 * (0.0015 if modelo == "gpt-3.5-turbo" else 0.03)

            log_df = pd.DataFrame([{
                "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "kpi": kpi_nombre,
                "modo": modo,
                "tokens": tokens,
                "costo_estimado_usd": round(costo, 6),
                "ubicacion": ubicacion,
                "modelo": modelo
            }])

            if os.path.exists(log_path):
                log_df.to_csv(log_path, mode='a', header=False, index=False)
            else:
                log_df.to_csv(log_path, index=False)

            return comentario
        else:
            return None

    except Exception as e:
        return f"🚨 Error GPT: {str(e)}"

def generar_comentario_gpt(df, kpi_nombre, modo, ubicacion="", modelo="gpt-3.5-turbo", log_path="logs/consumo_gpt.csv"):
#def generar_comentario_gpt(df, kpi_nombre, modo, ubicacion="", modelo="gpt-4", log_path="logs/consumo_gpt.csv"):
    try:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        df.columns = [col.upper() for col in df.columns]

        if modo.upper() == "ANUAL":
            columnas_mes = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
                            "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
            fila = df[df["GRUPO"].str.upper() == kpi_nombre.upper()]
            if fila.empty:
                return None

            columnas_filtradas = [mes for mes in columnas_mes if df[mes].sum() != 0]

            # serie_format = [
            #     f"{mes.title()}: ${float(fila[mes].iloc[0]):,.0f}"
            #     for mes in columnas_filtradas
            #     if pd.notnull(fila[mes].iloc[0])
            # ]

            # serie_format = [
            #     f"{mes.title()}: {float(fila[mes].iloc[0])}"
            #     for mes in columnas_filtradas
            #     if pd.notnull(fila[mes].iloc[0])
            # ]

            serie_format = [
                f"{mes.title()}: {float(fila[mes].iloc[0]):.0f}"
                for mes in columnas_filtradas
                if pd.notnull(fila[mes].iloc[0])
            ]

            print("serie_format")
            print(serie_format)

            # prompt = (
            #     f"Actúa como un analista financiero con experiencia. Con base en la siguiente serie mensual de datos "
            #     f"del KPI '{kpi_nombre}':\n\n{serie_format}\n\n"
            #     f"Redacta un análisis ejecutivo claro y profesional para gerencia. "
            #     f"Usa los nombres de los meses y muestra los valores con símbolo de pesos ($). "
            #     f"Evita escribir 'primer mes', 'segundo mes', etc. "
            #     f"Identifica patrones importantes como aumentos, caídas, repuntes o estacionalidad. "
            #     f"Redacta de manera precisa y clara, en lenguaje técnico pero comprensible para la alta dirección."
            # )

            # prompt = (
            #     f"Actúa como un analista financiero con experiencia. Con base en la siguiente serie mensual de datos "
            #     f"del KPI '{kpi_nombre}':\n\n{serie_format}\n\n"
            #     f"Redacta un análisis ejecutivo claro y profesional para gerencia. "
            #     f"Usa los nombres de los meses, y los valores deben mostrarse con el símbolo de pesos ($) en formato normal, "
            #     f"por ejemplo: $1,234,567. No uses comas para separar miles si estás dentro de una lista ni pegues texto. "
            #     f"Evita frases como 'primer mes'. Utiliza un lenguaje fluido, técnico, claro y bien espaciado. "
            #     f"El texto debe estar en párrafos legibles y naturales, evitando saltos de línea innecesarios y sin formato tipo lista JSON."
            # )


            # prompt = (
            #     f"Actúa como un analista financiero con experiencia. Con base en la siguiente serie mensual de datos "
            #     f"del KPI '{kpi_nombre}':\n\n{serie_format}\n\n"
            #     f"Redacta un análisis ejecutivo claro y profesional para gerencia. "
            #     f"Usa los nombres de los meses, y los valores deben mostrarse con el símbolo de pesos ($) en formato normal, "
            #     f"por ejemplo: $1,234,567. No uses comas para separar miles si estás dentro de una lista ni pegues texto. "
            #     f"Evita frases como 'primer mes'. Utiliza un lenguaje fluido, técnico, claro y bien espaciado. "
            #     f"El texto debe estar en párrafos legibles y naturales, evitando saltos de línea innecesarios y sin formato tipo lista JSON."
            # )

            prompt = (
                f"Actúa como un analista financiero. Con base en la siguiente serie mensual de valores del KPI '{kpi_nombre}':\n\n"
                f"{serie_format}\n\n"
                f"Redacta un breve análisis ejecutivo en máximo 10 frases claras máximo 2 párrafos. Menciona si hubo crecimiento, caídas o estabilidad, "
                f"usando nombres de los meses y valores en millones redondeado y sin decimales si es necesario. Puedes usar una frase "
                f"con comparativos porcentuales mas relevantes que encuentres. Evita repetir información o extenderte demasiado. "
                f"El texto debe ser profesional, directo y enfocado en transmitir una conclusión rápida para gerencia."
            )

            response = client.chat.completions.create(
                model=modelo,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=300
            )
            comentario = response.choices[0].message.content.strip()

            tokens = response.usage.total_tokens
            costo = tokens / 1000 * (0.0015 if modelo == "gpt-3.5-turbo" else 0.03)

            log_df = pd.DataFrame([{
                "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "kpi": kpi_nombre,
                "modo": modo,
                "tokens": tokens,
                "costo_estimado_usd": round(costo, 6),
                "ubicacion": ubicacion,
                "modelo": modelo
            }])

            if os.path.exists(log_path):
                log_df.to_csv(log_path, mode='a', header=False, index=False)
            else:
                log_df.to_csv(log_path, index=False)

            return comentario
        else:
            return None

    except Exception as e:
        return f"🚨 Error GPT: {str(e)}"

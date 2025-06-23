import pandas as pd
import numpy as np
from scipy import stats
from openai import OpenAI
import os

_client = None

def _get_client():
    global _client
    if _client is None:
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("❌ No se encontró OPENAI_API_KEY en el entorno")
        _client = OpenAI(api_key=key)
    return _client


def analizar_mes_anual(df_kpis, df_mensual, df_anual, plan, config):
    env = os.getenv("APP_ENV")
    print("🔧 variables de entorno:", {"APP_ENV": env, "OPENAI_API_KEY": bool(os.getenv("OPENAI_API_KEY"))})

    frases = generar_conclusiones(df_kpis)

    # Comparativo vs mes anterior
    if config.get("Comparativo mes anterior"):
        try:
            idx = list(df_anual.columns).index("MENSUAL")
            mes_ant = df_anual.columns[idx - 1]
            ventas_hoy = float(df_anual.loc[df_anual["GRUPO"].str.upper()=="VENTAS", "MENSUAL"])
            ventas_ant = float(df_anual.loc[df_anual["GRUPO"].str.upper()=="VENTAS", mes_ant])
            pct = (ventas_hoy / ventas_ant - 1) * 100
            frases.append(f"↔️ Ventas {pct:+.1f}% vs mes anterior ({mes_ant}).")
        except Exception:
            pass

    # Conclusión anual
    if config.get("Conclusiones anuales"):
        try:
            total_ano = float(df_anual.loc[df_anual["GRUPO"].str.upper()=="VENTAS", "Acumulado"])
            frases.append(f"📅 Ventas acumuladas en el año: ${total_ano:,.0f}.")
        except Exception:
            pass

    # Alertas por desviación vs anual
    if config.get("Detectar alertas (> umbral %)"):
        umbral = config.get("Umbral alertas %", 10)
        for label in ["Ventas", "Total costo mercancia vendida", "Total gastos operacionales"]:
            fila = df_kpis[df_kpis["GRUPO"].str.upper()==label.upper()]
            if not fila.empty:
                hoy = float(fila["MENSUAL"]); ant = float(fila["ANUAL"])
                pctc = (hoy/ant - 1) * 100 if ant else 0
                if abs(pctc) > umbral:
                    frases.append(f"⚠️ Cambio en *{label}* de {pctc:+.1f}% vs anual (> {umbral}%).")

    # Tendencia últimos 6 meses
    if config.get("Tendencias (3–6 meses)"):
        try:
            df_ventas = df_anual[df_anual["GRUPO"].str.upper()=="VENTAS"]
            ult6 = df_ventas.iloc[0, -6:].values.astype(float)
            slope = np.polyfit(range(len(ult6)), ult6, 1)[0]
            trend = "alzando 📈" if slope > 0 else "bajando 📉"
            frases.append(f"📈 Tendencia ventas últimos 6 meses: {trend}.")
        except Exception:
            pass

    # Anomalías por z-score
    if config.get("Detección de anomalías estadísticas"):
        vals = df_mensual["VALOR"].fillna(0).astype(float)
        zs = stats.zscore(vals)
        out = df_mensual["CUENTA"][np.abs(zs) > 2].tolist()
        if out:
            frases.append(f"🔍 Valores atípicos en cuentas: {', '.join(out)}.")


    if env == "MOCK":
        print("⚠️ [MOCK] Modo desarrollo activo. No se usará GPT.")
        frases.insert(0, "[MOCK] Resumen simulado activado.")
        return frases

    if config.get("Resumen narrativo con GPT"):
        prompt = "Resume el siguiente análisis financiero:\n" + "\n".join(frases)
        try:
            client = _get_client()
            resp = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un analista financiero."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            resumen = resp.choices[0].message.content.strip()
            return [resumen]
        except Exception as e:
            frases.append("⚠️ Resumen GPT no disponible. Ejecutando análisis básico.")
            print("🚨 Error GPT:", e)
            return frases

    return frases

def generar_conclusiones(df_kpis):
    frases = []
    def valor(grupo, tipo="MENSUAL"):
        fila = df_kpis[df_kpis["GRUPO"].str.upper() == grupo.upper()]
        return float(fila.iloc[0][tipo]) if not fila.empty else None

    # (tu lógica original)
    ventas = valor("TOTAL VENTAS")
    margen_bruto_pct = valor("MARGEN BRUTO %")
    utilidad_operacional = valor("RESULTADO OPERACIONAL")
    margen_valor = valor("MARGEN BRUTO")
    costo_ventas = valor("TOTAL COSTO MERCANCIA VENDIDA")
    gastos_operacionales = valor("TOTAL GASTOS OPERACIONALES")

    if ventas is not None:
        frases.append(f"📊 Las ventas del mes fueron de ${ventas:,.0f}.")
    if margen_bruto_pct is not None:
        if margen_bruto_pct < 20:
            frases.append(f"⚠️ Margen bruto de *{margen_bruto_pct:.2f}%*, es bajo.")
        elif margen_bruto_pct < 40:
            frases.append(f"🔎 Margen bruto de *{margen_bruto_pct:.2f}%*, dentro de rango.")
        else:
            frases.append(f"✅ Excelente margen bruto de *{margen_bruto_pct:.2f}%*.")
    if utilidad_operacional is not None:
        if utilidad_operacional > 0:
            frases.append(f"📈 Resultado operacional positivo de ${utilidad_operacional:,.0f}.")
        elif utilidad_operacional == 0:
            frases.append("🔍 Resultado operacional neutro.")
        else:
            frases.append(f"🚨 Pérdida operacional de ${abs(utilidad_operacional):,.0f}.")
    if margen_valor is not None:
        frases.append(f"🧮 Margen bruto total: ${margen_valor:,.0f}.")
    if costo_ventas is not None:
        frases.append(f"📦 Costo mercancía vendida: ${costo_ventas:,.0f}.")
    if gastos_operacionales is not None:
        frases.append(f"🧾 Gastos operacionales: ${gastos_operacionales:,.0f}.")

    if not frases:
        return ["No se generaron conclusiones automáticas por falta de datos."]
    return frases

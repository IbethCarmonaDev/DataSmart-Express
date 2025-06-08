# Funcion creada para generar conclusiones en Lenguaje Natural con base en los KPI's
# Creada por: Ibeth Carmona - IA
# Fecha de Creación: Junio 7-2025
# All rights reserved

def generar_conclusiones(df_kpis):
    frases = []

    def valor(grupo, tipo="MENSUAL"):
        fila = df_kpis[df_kpis["GRUPO"].str.upper() == grupo.upper()]
        if not fila.empty:
            return fila.iloc[0][tipo]
        return None

    ventas = valor("TOTAL VENTAS")
    margen_bruto = valor("MARGEN BRUTO %")
    utilidad_operacional = valor("RESULTADO OPERACIONAL")
    margen_valor = valor("MARGEN BRUTO")
    costo_ventas = valor("TOTAL COSTO MERCANCIA VENDIDA")
    gastos_operacionales = valor("TOTAL GASTOS OPERACIONALES")

    if ventas is not None:
        frases.append(f"📊 Las ventas del mes fueron de ${ventas:,.0f}.")

    if margen_bruto is not None:
        if margen_bruto < 20:
            frases.append(f"⚠️ El margen bruto fue de solo {margen_bruto:.2f}%, lo cual es bajo.")
        elif margen_bruto < 40:
            frases.append(f"🔎 El margen bruto fue de {margen_bruto:.2f}%, dentro de un rango aceptable.")
        else:
            frases.append(f"✅ Excelente margen bruto de {margen_bruto:.2f}%.")

    if utilidad_operacional is not None:
        if utilidad_operacional > 0:
            frases.append(f"📈 El resultado operacional fue positivo por ${utilidad_operacional:,.0f}.")
        elif utilidad_operacional == 0:
            frases.append("🔍 El resultado operacional fue neutro.")
        else:
            frases.append(f"🚨 Hubo una pérdida operacional de ${abs(utilidad_operacional):,.0f}.")

    if margen_valor is not None:
        frases.append(f"🧮 El margen bruto total fue de ${margen_valor:,.0f}.")

    if costo_ventas is not None:
        frases.append(f"📦 El costo de la mercancía vendida fue de ${costo_ventas:,.0f}.")

    if gastos_operacionales is not None:
        frases.append(f"🧾 Los gastos operacionales fueron de ${gastos_operacionales:,.0f}.")

    if not frases:
        return "No se pudo generar el análisis automático porque no se encontraron KPIs clave."

    return "\n\n".join(frases)  # <- cada frase en un párrafo separado

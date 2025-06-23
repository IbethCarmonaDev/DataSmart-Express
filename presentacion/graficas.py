import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st
from io import BytesIO
from core.comentarios import generar_comentario_logico_anual

def grafico_generico(df, kpi_nombre, tipo_grafico, modo="ANUAL", tipo_dato="MONEDA", columna_texto_extra=None):
    df = df.copy()
    df.columns = [col.upper() for col in df.columns]

    orden_meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
                   "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]

    if modo.upper() == "MENSUAL":
        if not all(col in df.columns for col in ["CUENTA", "MES", "VALOR"]):
            raise ValueError("El DataFrame mensual debe tener columnas 'CUENTA', 'MES' y 'VALOR'")
        df["CUENTA"] = df["CUENTA"].str.upper()
        df["MES"] = df["MES"].str.upper()
        df_filtrado = df[df["CUENTA"] == kpi_nombre.upper()]
        if df_filtrado.empty:
            raise ValueError(f"No se encontraron datos mensuales para el KPI: {kpi_nombre}")
        df_sum = df_filtrado.groupby("MES")["VALOR"].sum().reset_index()

    elif modo.upper() == "ANUAL":
        if "GRUPO" not in df.columns:
            raise ValueError("El DataFrame anual debe tener la columna 'GRUPO'")
        df["GRUPO"] = df["GRUPO"].str.upper()
        columnas_mes = [col for col in orden_meses if col in df.columns]
        df_largo = df.melt(id_vars=["GRUPO"], value_vars=columnas_mes,
                           var_name="MES", value_name="VALOR")
        df_filtrado = df_largo[df_largo["GRUPO"] == kpi_nombre.upper()]
        if df_filtrado.empty:
            raise ValueError(f"No se encontraron datos anuales para el KPI: {kpi_nombre}")
        df_sum = df_filtrado.groupby("MES")["VALOR"].sum().reset_index()

        if columna_texto_extra:
            columna_texto_extra = str(columna_texto_extra).upper()
            if columna_texto_extra in df_largo["GRUPO"].unique():
                df_extra = df_largo[df_largo["GRUPO"] == columna_texto_extra]
                df_extra = df_extra.groupby("MES")["VALOR"].sum().reset_index()
                df_extra.rename(columns={"VALOR": "VALOR_EXTRA"}, inplace=True)
                df_sum = pd.merge(df_sum, df_extra, on="MES", how="left")
            else:
                df_sum["VALOR_EXTRA"] = None
        else:
            df_sum["VALOR_EXTRA"] = None

    else:
        raise ValueError("Modo inválido. Usa 'MENSUAL' o 'ANUAL'.")

    df_sum["MES"] = pd.Categorical(df_sum["MES"], categories=orden_meses, ordered=True)
    df_sum = df_sum.sort_values("MES")

    if tipo_dato.upper() == "PORCENTAJE":
        df_sum["VALOR"] = df_sum["VALOR"] / 100

    df_sum = df_sum[df_sum["VALOR"] != 0]

    def formatear_texto(row):
        color_negativo = 'red'
        valor_base = row["VALOR"]
        if tipo_dato.upper() == "MONEDA":
            texto = f"<b style='color:{color_negativo}'>{valor_base:,.0f}</b>" if valor_base < 0 else f"<b>${valor_base:,.0f}</b>"
        elif tipo_dato.upper() == "PORCENTAJE":
            texto = f"<b style='color:{color_negativo}'>{valor_base:.2%}</b>" if valor_base < 0 else f"<b>{valor_base:.2%}</b>"
        else:
            texto = f"<b style='color:{color_negativo}'>{valor_base:,.2f}</b>" if valor_base < 0 else f"<b>{valor_base:,.2f}</b>"

        if row.get("VALOR_EXTRA") is not None and np.isfinite(row["VALOR_EXTRA"]):
            texto_extra = f"<br><span style='font-size:11px'>{row['VALOR_EXTRA']:.1f}%</span>"
            return f"{texto}{texto_extra}"
        return texto


    df_sum["TEXTO_COMBINADO"] = df_sum.apply(formatear_texto, axis=1)

    if tipo_grafico.upper() == "BARRA":
        fig = px.bar(df_sum, x="MES", y="VALOR", title=kpi_nombre, text="TEXTO_COMBINADO")
        fig.update_traces(textposition="outside", texttemplate=df_sum["TEXTO_COMBINADO"])
    elif tipo_grafico.upper() == "LINEAL":
        fig = px.line(df_sum, x="MES", y="VALOR", title=kpi_nombre, text="TEXTO_COMBINADO")
        fig.update_traces(textposition="top center", texttemplate=df_sum["TEXTO_COMBINADO"])
    else:
        fig = px.bar(df_sum, x="MES", y="VALOR", title=kpi_nombre, text="TEXTO_COMBINADO")
        fig.update_traces(textposition="outside", texttemplate=df_sum["TEXTO_COMBINADO"])

    fig.update_yaxes(range=[df_sum["VALOR"].min() * 1.15 if df_sum["VALOR"].min() < 0 else 0, df_sum["VALOR"].max() * 1.15])
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode="show")
    return fig

def grafico_participacion_mensual(df, kpi_nombre, tipo_grafico, tipo_dato="MONEDA", columna_texto_extra=None, top_n=10):
    import plotly.express as px
    import numpy as np
    import pandas as pd

    df = df.copy()
    df.columns = [col.upper() for col in df.columns]

    if "GRUPO" not in df.columns or "CUENTA" not in df.columns or "VALOR" not in df.columns:
        raise ValueError("El DataFrame mensual debe tener columnas 'GRUPO', 'CUENTA' y 'VALOR'")

    # Filtrar y agrupar por KPI
    df_filtrado = df[df["GRUPO"].str.upper() == kpi_nombre.upper()]
    if df_filtrado.empty:
        raise ValueError(f"No se encontraron datos mensuales para el KPI: {kpi_nombre}")

    df_sum = df_filtrado.groupby("CUENTA")["VALOR"].sum().reset_index()
    df_sum = df_sum.sort_values(by="VALOR", ascending=False).head(top_n)

    # Invertir orden visual para que la barra más grande quede arriba
    cuentas_ordenadas = df_sum["CUENTA"].tolist()[::-1]
    df_sum["CUENTA"] = pd.Categorical(df_sum["CUENTA"], categories=cuentas_ordenadas, ordered=True)

    # Texto enriquecido
    def formatear(valor):
        if tipo_dato.upper() == "PORCENTAJE":
            return f"{valor:.2%}"
        elif tipo_dato.upper() == "DECIMAL":
            return f"{valor:,.2f}"
        else:
            return f"$ {valor:,.0f}"

    df_sum["TEXTO"] = df_sum["CUENTA"].astype(str) + "<br>" + df_sum["VALOR"].apply(formatear)

    # Gráfico tipo TORTA
    if tipo_grafico.upper() == "TORTA":
        fig = px.pie(
            df_sum,
            values="VALOR",
            names="CUENTA",
            title=kpi_nombre,
            hover_data=["TEXTO"],
            color_discrete_sequence=["#0d47a1", "#1976d2", "#2196f3", "#64b5f6", "#bbdefb"]
        )
        fig.update_traces(
            textinfo="label+percent+text",
            textposition="outside",
            textfont = dict(color="black")
        )

    # Gráfico tipo BARRA
    else:
        fig = px.bar(
            df_sum,
            x="VALOR",
            y="CUENTA",
            orientation="h",
            text="TEXTO",
            title=kpi_nombre,
            color="CUENTA",
            color_discrete_sequence=["#0d47a1", "#1976d2", "#2196f3", "#64b5f6", "#bbdefb"]
        )
        fig.update_traces(textposition="outside", textfont=dict(color="black"))

    # Configuración visual común
    fig.update_layout(
        yaxis_title=None,
        xaxis_title=None,
        coloraxis_showscale=False,
        uniformtext_minsize=8,
        uniformtext_mode="show"
    )

    return fig

def exportar_grafico_plotly(fig, formato="png"):
    img_bytes = fig.to_image(format=formato, width=800, height=600, scale=2)
    return img_bytes



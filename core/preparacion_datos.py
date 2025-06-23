import numpy as np
import pandas as pd
import streamlit as st

def preparar_df_mensual(df_datos, df_clasificacion, año, mes, centro):
    df_temp = df_datos.copy()
    df_temp["AÑO"] = df_temp["AÑO"].astype(int)
    df_temp["MES"] = df_temp["MES"].astype(int)

    df_mensual = df_temp[
        (df_temp["AÑO"] == año) &
        (df_temp["MES"] == mes)
    ].copy()

    if centro != "TODOS":
        df_mensual = df_mensual[df_mensual["CENTRO_COSTOS"] == centro]

    df_mensual["PREFIJO"] = df_mensual["COD_CUENTA"].astype(str).str[:2]

    df_datos["PREFIJO"] = df_datos["COD_CUENTA"].astype(str).str[:2]
    df_clasificacion["PREFIJO"] = df_clasificacion["PREFIJO"].astype(str).str.zfill(2)

    df_mensual = pd.merge(
        df_mensual,
        df_clasificacion[["PREFIJO", "GRUPO", "NATURALEZA_CONTABLE"]],
        on="PREFIJO",
        how="left"
    )

    df_mensual.columns = [col.upper() for col in df_mensual.columns]

    df_mensual["VALOR"] = np.where(
        df_mensual["NATURALEZA_CONTABLE"].str.upper() == "DEBITO",
        df_mensual["DEBITO"] - df_mensual["CREDITO"],
        df_mensual["CREDITO"] - df_mensual["DEBITO"]
    )

    return df_mensual

def validar_archivo_usuario(df_datos, df_clasificacion):
    """
    Valida la estructura y tipos del archivo:
      • DATOS_FINANCIEROS: AÑO, MES, COD_CUENTA, CUENTA, CODCC, CENTRO_COSTOS, DEBITO, CREDITO
      • CLASIFICACION_CUENTAS: PREFIJO, GRUPO, NATURALEZA_CONTABLE
    Muestra mensajes en Streamlit y retorna True si pasa las validaciones.
    """
    ok = True

    # 1. Estructura de DATOS_FINANCIEROS
    esperadas = {"AÑO", "MES", "COD_CUENTA", "CUENTA", "CODCC", "CENTRO_COSTOS", "DEBITO", "CREDITO"}
    cols = set(df_datos.columns.str.upper())
    faltan = esperadas - cols
    if faltan:
        st.error(f"❌ Faltan columnas en DATOS_FINANCIEROS: {', '.join(faltan)}")
        ok = False

    # 2. Validar tipos básicos
    if "AÑO" in cols and not pd.api.types.is_integer_dtype(df_datos["AÑO"]):
        st.error("❌ La columna 'AÑO' debe ser de tipo entero.")
        ok = False
    if "MES" in cols and not pd.api.types.is_integer_dtype(df_datos["MES"]):
        st.error("❌ La columna 'MES' debe ser de tipo entero.")
        ok = False
    for col in ["DEBITO", "CREDITO"]:
        if col in cols and not pd.api.types.is_numeric_dtype(df_datos[col]):
            st.error(f"❌ La columna '{col}' debe ser numérica.")
            ok = False

    # 3. Rango de MES válido
    if "MES" in cols:
        invalid_mes = df_datos.loc[~df_datos["MES"].between(1,12), "MES"]
        if not invalid_mes.empty:
            st.error(f"❌ {len(invalid_mes)} filas con 'MES' fuera de 1–12.")
            ok = False

    # 4. Filas con valores críticos faltantes
    clave = ["AÑO", "MES", "DEBITO", "CREDITO"]
    if all(c in cols for c in clave):
        nulos = df_datos[df_datos[clave].isnull().any(axis=1)]
        if not nulos.empty:
            st.warning(f"⚠️ {len(nulos)} filas con valores nulos en columnas críticas serán eliminadas.")
            df_datos.dropna(subset=clave, inplace=True)

    # 5. Validar CLASIFICACION_CUENTAS si está presente
    if df_clasificacion is not None:
        cols2 = set(df_clasificacion.columns.str.upper())
        esperadas2 = {"PREFIJO", "GRUPO", "NATURALEZA_CONTABLE"}
        faltan2 = esperadas2 - cols2
        if faltan2:
            st.error(f"❌ En CLASIFICACION_CUENTAS faltan columnas: {', '.join(faltan2)}")
            ok = False

    return ok


# Funcion creada para generar estado de resultados
# Creada por: Ibeth Carmona - IA
# Fecha de Creación: Junio 7-2025
# All rights reserved

import pandas as pd
import numpy as np
import streamlit as st

def git init(df_datos, df_clasificacion, archivo_parametros, centro_costos=None):
    df = df_datos.copy()

    # Asegurar que COD_CUENTA es string limpio
    df["COD_CUENTA"] = df["COD_CUENTA"].astype(str).str.strip()
    df["PREFIJO"] = df["COD_CUENTA"].str[:2]

    df_clasificacion["PREFIJO"] = df_clasificacion["PREFIJO"].astype(str).str.strip()

    # Hacer merge por PREFIJO
    df = df.merge(df_clasificacion, on="PREFIJO", how="left")

    # Calcular el valor contable
    df["VALOR"] = np.where(
        df["NATURALEZA_CONTABLE"].str.upper() == "DEBITO",
        df["DEBITO"] - df["CREDITO"],
        df["CREDITO"] - df["DEBITO"]
    )

    columnas_validas = ["AÑO", "MES", "GRUPO", "COD_CUENTA", "CUENTA", "CENTRO_COSTOS", "VALOR"]
    if "SUBTOTAL_EN" in df.columns:
        columnas_validas.insert(3, "SUBTOTAL_EN")

    df = df[columnas_validas]

    # Agrupación por cuenta
    df_cuenta = df.groupby(["AÑO", "MES", "GRUPO", "COD_CUENTA", "CUENTA", "CENTRO_COSTOS"], as_index=False)["VALOR"].sum()
    df_cuenta["TIPO"] = "CUENTA"

    # Agregar totales por grupo si existe SUBTOTAL_EN
    if "SUBTOTAL_EN" in columnas_validas:
        df_totales = df.groupby(["AÑO", "MES", "SUBTOTAL_EN", "CENTRO_COSTOS"], as_index=False)["VALOR"].sum()
        df_totales = df_totales.rename(columns={"SUBTOTAL_EN": "GRUPO"})
        df_totales["CUENTA"] = ""
        df_totales["COD_CUENTA"] = ""
        df_totales["TIPO"] = "TOTAL_GRUPO"
        df_resultado = pd.concat([df_cuenta, df_totales], ignore_index=True)
    else:
        df_resultado = df_cuenta.copy()

    df_resultado["MENSUAL"] = df_resultado["VALOR"]
    df_resultado["ANUAL"] = df_resultado.groupby(["GRUPO", "CUENTA", "CENTRO_COSTOS"])["MENSUAL"].transform("sum")
    df_resultado = df_resultado[["AÑO", "MES", "GRUPO", "COD_CUENTA", "CUENTA", "CENTRO_COSTOS", "TIPO", "MENSUAL", "ANUAL"]]

    return df_resultado

def generar_estado_resultados_detallado(df_datos, df_clasificacion, df_tarjetas, año, mes, df_kpis, centro_costos=None):
    df_datos.columns = df_datos.columns.str.strip().str.upper()

    # df_clasificacion es recibido directamente desde app.py
    # df_kpis = pd.read_excel(archivo_parametros, sheet_name="KPIS_FINANCIEROS")
    if 'MOSTRAR_EN_PG' in df_kpis.columns:
        df_kpis = df_kpis[df_kpis['MOSTRAR_EN_PG'] == 1]
        ##df_tarjetas = pd.read_excel(archivo_parametros, sheet_name="TARJETAS")

    df_clasificacion.columns = df_clasificacion.columns.str.strip().str.upper()
    df_kpis.columns = df_kpis.columns.str.strip().str.upper()
    ##df_tarjetas.columns = df_tarjetas.columns.str.strip().str.upper()

    df_datos = df_datos[df_datos["AÑO"] == año].copy()
    df_datos["PREFIJO"] = df_datos["COD_CUENTA"].astype(str).str[:2]
    df_clasificacion["PREFIJO"] = df_clasificacion["PREFIJO"].astype(str)
    df_datos = df_datos.merge(df_clasificacion, on="PREFIJO", how="left")

    df_datos["VALOR"] = df_datos.apply(
        lambda row: row["DEBITO"] - row["CREDITO"] if str(row["NATURALEZA_CONTABLE"]).upper() == "DEBITO" else row["CREDITO"] - row["DEBITO"],
        axis=1
    )

    if centro_costos and centro_costos != "TODOS":
        df_datos = df_datos[df_datos["CENTRO_COSTOS"] == centro_costos]

    df_mensual = df_datos[df_datos["MES"] == mes].groupby(["GRUPO", "COD_CUENTA", "CUENTA"])["VALOR"].sum()
    df_anual = df_datos[df_datos["MES"] <= mes].groupby(["GRUPO", "COD_CUENTA", "CUENTA"])["VALOR"].sum()
    df_cuentas = pd.DataFrame({"MENSUAL": df_mensual, "ANUAL": df_anual}).fillna(0).reset_index()

    clasif = df_clasificacion.drop_duplicates(subset=["GRUPO"])[["GRUPO"]]
    df_cuentas = df_cuentas.merge(clasif, on="GRUPO", how="left")

    orden = df_clasificacion.drop_duplicates(subset=["GRUPO"]).reset_index(drop=True)
    orden["ORDEN"] = orden.index
    df_cuentas = df_cuentas.merge(orden[["GRUPO", "ORDEN"]], on="GRUPO", how="left")

    df_cuentas = df_cuentas.sort_values(by=["ORDEN", "COD_CUENTA"])

    def normalizar(texto):
        return str(str(texto).strip().upper())

    estructura = []
    totales_por_grupo = {}
    #kpis_para_tarjeta = []
    kpis_dict = {}

    grupo_actual = None
    valores_grupo = []
    ultimo_kpi = None

    for i, fila in df_cuentas.iterrows():
        grupo = fila["GRUPO"]
        cuenta = fila["CUENTA"]
        mensual = fila["MENSUAL"]
        anual = fila["ANUAL"]

        if grupo != grupo_actual and grupo_actual is not None:
            total_mensual_grupo = sum(x["MENSUAL"] for x in valores_grupo)
            total_anual_grupo = sum(x["ANUAL"] for x in valores_grupo)

            estructura.append({"GRUPO": grupo_actual, "CUENTA": "", "MENSUAL": None, "ANUAL": None})
            estructura.extend(valores_grupo)
            total_key = f"TOTAL {grupo_actual.upper()}"
            totales_por_grupo[normalizar(total_key)] = {"MENSUAL": total_mensual_grupo, "ANUAL": total_anual_grupo}
            estructura.append({"GRUPO": total_key, "CUENTA": "", "MENSUAL": total_mensual_grupo, "ANUAL": total_anual_grupo})

            contexto_mensual = {normalizar(k).replace(" ", "_"): v["MENSUAL"] for k, v in totales_por_grupo.items()}
            contexto_anual = {normalizar(k).replace(" ", "_"): v["ANUAL"] for k, v in totales_por_grupo.items()}

            kpis_grupo = df_kpis[df_kpis["UBICAR_LUEGO_DE"].apply(normalizar) == normalizar(total_key)]
            for _, kpi in kpis_grupo.iterrows():
                nombre_kpi = kpi["KPI"].upper()
                formula = str(str(kpi["FORMULA"]).strip().upper()).replace(" ", "_")
                tipo_dato = kpi.get("TIPO_DATO", "MONEDA").strip().upper()
                try:
                    mensual_kpi = eval(formula, {}, contexto_mensual)
                    anual_kpi = eval(formula, {}, contexto_anual)
                except Exception as e:
                    mensual_kpi = 0
                    anual_kpi = 0
                kpi_row = {"GRUPO": nombre_kpi, "CUENTA": "", "MENSUAL": mensual_kpi, "ANUAL": anual_kpi}
                ultimo_kpi = kpi_row
                estructura.append(kpi_row)
                kpis_dict[nombre_kpi] = kpi_row

            valores_grupo = []

        grupo_actual = grupo
        valores_grupo.append({"GRUPO": "", "CUENTA": cuenta, "MENSUAL": mensual, "ANUAL": anual})

    if grupo_actual:
        total_mensual_grupo = sum(x["MENSUAL"] for x in valores_grupo)
        total_anual_grupo = sum(x["ANUAL"] for x in valores_grupo)

        estructura.append({"GRUPO": grupo_actual, "CUENTA": "", "MENSUAL": None, "ANUAL": None})
        estructura.extend(valores_grupo)
        total_key = f"TOTAL {grupo_actual.upper()}"
        totales_por_grupo[normalizar(total_key)] = {"MENSUAL": total_mensual_grupo, "ANUAL": total_anual_grupo}
        estructura.append({"GRUPO": total_key, "CUENTA": "", "MENSUAL": total_mensual_grupo, "ANUAL": total_anual_grupo})

        contexto_mensual = {normalizar(k).replace(" ", "_"): v["MENSUAL"] for k, v in totales_por_grupo.items()}
        contexto_anual = {normalizar(k).replace(" ", "_"): v["ANUAL"] for k, v in totales_por_grupo.items()}

        kpis_grupo = df_kpis[df_kpis["UBICAR_LUEGO_DE"].apply(normalizar) == normalizar(total_key)]
        for _, kpi in kpis_grupo.iterrows():
            nombre_kpi = kpi["KPI"].upper()
            formula = str(str(kpi["FORMULA"]).strip().upper()).replace(" ", "_")
            tipo_dato = kpi.get("TIPO_DATO", "MONEDA").strip().upper()
            try:
                mensual_kpi = eval(formula, {}, contexto_mensual)
                anual_kpi = eval(formula, {}, contexto_anual)
            except Exception as e:
                mensual_kpi = 0
                anual_kpi = 0
            kpi_row = {"GRUPO": nombre_kpi, "CUENTA": "", "MENSUAL": mensual_kpi, "ANUAL": anual_kpi}
            ultimo_kpi = kpi_row
            estructura.append(kpi_row)
            kpis_dict[nombre_kpi] = kpi_row

    df_estructura = pd.DataFrame(estructura)

    kpis_para_tarjeta = []
    df_tarjetas.columns = df_tarjetas.columns.str.strip().str.upper()

    for _, fila in df_tarjetas.sort_values(by="ORDEN").iterrows():
        nombre = str(fila["KPI"]).upper()
        tipo_dato = str(fila.get("TIPO_DATO", "MONEDA")).upper()
        fuente = str(fila.get("FUENTE", "KPI")).upper()
        if fuente == "GRUPO":
            key = normalizar(nombre)
            if key in totales_por_grupo:
                mensual = totales_por_grupo[key]["MENSUAL"]
                anual = totales_por_grupo[key]["ANUAL"]
                kpis_para_tarjeta.append({"GRUPO": nombre, "MENSUAL": mensual, "ANUAL": anual, "TIPO_DATO": tipo_dato})
        elif fuente == "KPI" and nombre in kpis_dict:
            row = kpis_dict[nombre]
            kpis_para_tarjeta.append({"GRUPO": nombre, "MENSUAL": row["MENSUAL"], "ANUAL": row["ANUAL"], "TIPO_DATO": tipo_dato})

    df_kpis_tarjeta = pd.DataFrame(kpis_para_tarjeta)

    return df_estructura, df_kpis_tarjeta

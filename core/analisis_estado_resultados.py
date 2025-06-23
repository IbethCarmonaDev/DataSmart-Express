# Funcion creada para generar estado de resultados
# Creada por: Ibeth Carmona - IA
# Fecha de Creación: Junio 7-2025
# All rights reserved

import pandas as pd
import numpy as np
import streamlit as st
import hashlib
from core.analisis_estado_resultados_anual import generar_estado_resultados_anual

_cache_estados = {}

def _hash_df(df):
    return hashlib.md5(pd.util.hash_pandas_object(df, index=True).values).hexdigest()

def cargar_cache(df_datos, df_clasificacion, ruta_parametros):
    key = _hash_df(df_datos)
    if key not in _cache_estados:
        _cache_estados[key] = generar_estado_resultados_todos_los_meses(
            df_datos, df_clasificacion, ruta_parametros
        )
    return _cache_estados[key]

def obtener_estado_por_mes(df_todos, año, mes, centro_costos=None):
    df = df_todos[df_todos["AÑO"] == año]
    if centro_costos and centro_costos.upper() != "TODOS":
        df = df[df["CENTRO_COSTOS"] == centro_costos]
    df_mes = df[df["MES"] == mes]
    df_mes_ant = df[df["MES"] == mes - 1] if mes > 1 else None
    return df_mes, df_mes_ant

def obtener_estado_anual(df_todos, df_clasificacion, df_kpis_param, año, centro_costos=None):
    df = df_todos[df_todos["AÑO"] == año]
    if centro_costos and centro_costos.upper() != "TODOS":
        df = df[df["CENTRO_COSTOS"] == centro_costos]
    return generar_estado_resultados_anual(
        df, df_clasificacion, df_kpis_param, año, centro_costos
    )

def generar_estado_resultados_todos_los_meses(df_datos, df_clasificacion, archivo_parametros, centro_costos=None):
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
    df_resultado = df_resultado[["AÑO", "MES", "GRUPO", "COD_CUENTA", "CUENTA", "CENTRO_COSTOS", "TIPO", "MENSUAL", "ANUAL", "VALOR"]]

    return df_resultado

def OLDgenerar_estado_resultados_detallado(df_datos, df_clasificacion, df_tarjetas, año, mes, df_kpis, centro_costos=None):
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


def old2generar_estado_resultados_detallado(df_mes, df_clasificacion, df_tarjetas, año, mes, df_kpis, centro_costos=None):
    df_kpis = df_kpis[df_kpis.get('MOSTRAR_EN_PG', 1) == 1].copy()
    df_clasificacion = df_clasificacion.copy()
    df_tarjetas = df_tarjetas.copy()

    # Agrupamos el mes y acumulado
    df_cuentas = df_mes.groupby(
        ["GRUPO", "COD_CUENTA", "CUENTA"], as_index=False
    )["VALOR"].sum().rename(columns={"VALOR": "MENSUAL"})
    df_cuentas["ANUAL"] = df_mes.groupby(
        ["GRUPO", "COD_CUENTA", "CUENTA"]
    )["VALOR"].cumsum()  # ya es acumulado hasta este mes

    # Unimos datos para mantener columnas
    clasif = df_clasificacion.drop_duplicates(subset=["GRUPO"])[["GRUPO"]]
    df_cuentas = df_cuentas.merge(clasif, on="GRUPO", how="left")

    # Asignar orden visual
    orden = df_clasificacion.drop_duplicates(subset=["GRUPO"]).reset_index(drop=True)
    orden["ORDEN"] = orden.index
    df_cuentas = df_cuentas.merge(orden[["GRUPO", "ORDEN"]], on="GRUPO", how="left")
    df_cuentas = df_cuentas.sort_values(by=["ORDEN", "COD_CUENTA"])

    # Lógica para construir estructuras y KPIs (idéntica a tu función original)
    def normalizar(texto): return str(texto).strip().upper()

    estructura, totales_por_grupo, kpis_dict = [], {}, {}
    grupo_actual, valores_grupo = None, []
    ultimo_kpi = None

    for _, fila in df_cuentas.iterrows():
        grupo, cuenta = fila["GRUPO"], fila["CUENTA"]
        mensual, anual = fila["MENSUAL"], fila["ANUAL"]

        if grupo != grupo_actual and grupo_actual is not None:
            total_mensual = sum(x["MENSUAL"] for x in valores_grupo)
            total_anual = sum(x["ANUAL"] for x in valores_grupo)
            estructura.append({"GRUPO": grupo_actual, "CUENTA": "", "MENSUAL": None, "ANUAL": None})
            estructura.extend(valores_grupo)
            total_key = f"TOTAL {grupo_actual.upper()}"
            totales_por_grupo[normalizar(total_key)] = {"MENSUAL": total_mensual, "ANUAL": total_anual}
            estructura.append({"GRUPO": total_key, "CUENTA": "", "MENSUAL": total_mensual, "ANUAL": total_anual})

            contexto_m = {normalizar(k).replace(" ", "_"): v["MENSUAL"] for k, v in totales_por_grupo.items()}
            contexto_a = {normalizar(k).replace(" ", "_"): v["ANUAL"] for k, v in totales_por_grupo.items()}

            kpis_group = df_kpis[df_kpis["UBICAR_LUEGO_DE"].str.upper() == total_key]
            for _, kpi in kpis_group.iterrows():
                nombre_kpi = kpi["KPI"].upper()
                formula = kpi["FORMULA"].strip().upper().replace(" ", "_")
                try:
                    val_m = eval(formula, {}, contexto_m)
                    val_a = eval(formula, {}, contexto_a)
                except:
                    val_m = val_a = 0
                kpi_row = {"GRUPO": nombre_kpi, "CUENTA": "", "MENSUAL": val_m, "ANUAL": val_a}
                estructura.append(kpi_row)
                kpis_dict[nombre_kpi] = kpi_row

            valores_grupo = []

        grupo_actual = grupo
        valores_grupo.append({"GRUPO": "", "CUENTA": cuenta, "MENSUAL": mensual, "ANUAL": anual})

    # Proceso final de grupo pendiente
    if valores_grupo:
        total_m = sum(x["MENSUAL"] for x in valores_grupo)
        total_a = sum(x["ANUAL"] for x in valores_grupo)
        estructura.append({"GRUPO": grupo_actual, "CUENTA": "", "MENSUAL": None, "ANUAL": None})
        estructura.extend(valores_grupo)
        total_key = f"TOTAL {grupo_actual.upper()}"
        totales_por_grupo[normalizar(total_key)] = {"MENSUAL": total_m, "ANUAL": total_a}
        estructura.append({"GRUPO": total_key, "CUENTA": "", "MENSUAL": total_m, "ANUAL": total_a})

        contexto_m = {normalizar(k).replace(" ", "_"): v["MENSUAL"] for k, v in totales_por_grupo.items()}
        contexto_a = {normalizar(k).replace(" ", "_"): v["ANUAL"] for k, v in totales_por_grupo.items()}

        kpis_group = df_kpis[df_kpis["UBICAR_LUEGO_DE"].str.upper() == total_key]
        for _, kpi in kpis_group.iterrows():
            nombre_kpi = kpi["KPI"].upper()
            formula = kpi["FORMULA"].strip().upper().replace(" ", "_")
            try:
                val_m = eval(formula, {}, contexto_m)
                val_a = eval(formula, {}, contexto_a)
            except:
                val_m = val_a = 0
            kpi_row = {"GRUPO": nombre_kpi, "CUENTA": "", "MENSUAL": val_m, "ANUAL": val_a}
            estructura.append(kpi_row)
            kpis_dict[nombre_kpi] = kpi_row

    df_estructura = pd.DataFrame(estructura)

    # Lógica para tarjetas KPI (idéntica a tu función original)
    kpis_para_tarjeta = []
    df_tarjetas.columns = df_tarjetas.columns.str.strip().str.upper()

    for _, fila in df_tarjetas.sort_values("ORDEN").iterrows():
        nombre = fila["KPI"].upper()
        tipo_dato = fila.get("TIPO_DATO", "MONEDA").upper()
        fuente = fila.get("FUENTE", "KPI").upper()
        key = nombre if fuente == "KPI" else normalizar(nombre)
        if fuente == "GRUPO" and key in totales_por_grupo:
            m = totales_por_grupo[key]["MENSUAL"]
            a = totales_por_grupo[key]["ANUAL"]
            kpis_para_tarjeta.append({"GRUPO": nombre, "MENSUAL": m, "ANUAL": a, "TIPO_DATO": tipo_dato})
        elif fuente == "KPI" and nombre in kpis_dict:
            row = kpis_dict[nombre]
            kpis_para_tarjeta.append({"GRUPO": nombre, "MENSUAL": row["MENSUAL"], "ANUAL": row["ANUAL"], "TIPO_DATO": tipo_dato})

    df_kpis_tarjeta = pd.DataFrame(kpis_para_tarjeta)

    return df_estructura, df_kpis_tarjeta

def OLD3generar_estado_resultados_detallado(df_mes_all, df_clasificacion, df_tarjetas,
                                        año, mes, df_kpis, centro_costos=None):

    df_kpis = df_kpis[df_kpis.get('MOSTRAR_EN_PG', 1) == 1].copy()
    df_clasificacion = df_clasificacion.copy()
    df_tarjetas = df_tarjetas.copy()

    # Filtrado del mes actual
    df_mes = df_mes_all[df_mes_all["MES"] == mes]

    # Acumulado desde enero hasta el mes actual
    estado_anual = df_mes_all[(df_mes_all["MES"] <= mes)]
    if centro_costos and centro_costos.upper() != "TODOS":
        estado_anual = estado_anual[estado_anual["CENTRO_COSTOS"] == centro_costos]

    # Generar df_cuentas con valores Mensual y Anual
    df_cuentas = pd.DataFrame({
        "MENSUAL": df_mes.groupby(["GRUPO","COD_CUENTA","CUENTA"])["VALOR"].sum(),
        "ANUAL": estado_anual.groupby(["GRUPO","COD_CUENTA","CUENTA"])["VALOR"].sum()
    }).fillna(0).reset_index()

    # Agregar columnas para orden y clasificación
    clasif = df_clasificacion.drop_duplicates(subset=["GRUPO"])[["GRUPO"]]
    df_cuentas = df_cuentas.merge(clasif, on="GRUPO", how="left")
    orden = df_clasificacion.drop_duplicates(subset=["GRUPO"]).reset_index(drop=True)
    orden["ORDEN"] = orden.index
    df_cuentas = df_cuentas.merge(orden[["GRUPO","ORDEN"]], on="GRUPO", how="left")
    df_cuentas = df_cuentas.sort_values(by=["ORDEN","COD_CUENTA"])

    def normalizar(texto): return str(texto).strip().upper()

    estructura, totales_por_grupo, kpis_dict = [], {}, {}
    grupo_actual, valores_grupo = None, []

    # Construcción de filas por grupo + KPI
    for _, fila in df_cuentas.iterrows():
        grupo, cuenta = fila["GRUPO"], fila["CUENTA"]
        mensual, anual = fila["MENSUAL"], fila["ANUAL"]

        if grupo != grupo_actual and grupo_actual is not None:
            total_m = sum(x["MENSUAL"] for x in valores_grupo)
            total_a = sum(x["ANUAL"] for x in valores_grupo)
            estructura.append({"GRUPO":grupo_actual,"CUENTA":"","MENSUAL":None,"ANUAL":None})
            estructura.extend(valores_grupo)
            total_key = f"TOTAL {grupo_actual.upper()}"
            totales_por_grupo[normalizar(total_key)] = {"MENSUAL":total_m,"ANUAL":total_a}
            estructura.append({"GRUPO":total_key,"CUENTA":"","MENSUAL":total_m,"ANUAL":total_a})

            ctx_m = {normalizar(k).replace(" ","_"):v["MENSUAL"] for k,v in totales_por_grupo.items()}
            ctx_a = {normalizar(k).replace(" ","_"):v["ANUAL"] for k,v in totales_por_grupo.items()}

            for _, kpi in df_kpis[df_kpis["UBICAR_LUEGO_DE"].str.upper()==total_key].iterrows():
                nombre = kpi["KPI"].upper()
                formula = kpi["FORMULA"].strip().upper().replace(" ","_")
                try:
                    val_m = eval(formula,{},ctx_m)
                    val_a = eval(formula,{},ctx_a)
                except: val_m=val_a=0
                kpi_row={"GRUPO":nombre,"CUENTA":"","MENSUAL":val_m,"ANUAL":val_a}
                estructura.append(kpi_row); kpis_dict[nombre]=kpi_row

            valores_grupo = []

        grupo_actual = grupo
        valores_grupo.append({"GRUPO":"","CUENTA":cuenta,"MENSUAL":mensual,"ANUAL":anual})

    # Último grupo
    if valores_grupo:
        total_m = sum(x["MENSUAL"] for x in valores_grupo)
        total_a = sum(x["ANUAL"] for x in valores_grupo)
        estructura.append({"GRUPO":grupo_actual,"CUENTA":"","MENSUAL":None,"ANUAL":None})
        estructura.extend(valores_grupo)
        total_key = f"TOTAL {grupo_actual.upper()}"
        totales_por_grupo[normalizar(total_key)] = {"MENSUAL":total_m,"ANUAL":total_a}
        estructura.append({"GRUPO":total_key,"CUENTA":"","MENSUAL":total_m,"ANUAL":total_a})

        ctx_m = {normalizar(k).replace(" ","_"):v["MENSUAL"] for k,v in totales_por_grupo.items()}
        ctx_a = {normalizar(k).replace(" ","_"):v["ANUAL"] for k,v in totales_por_grupo.items()}
        for _, kpi in df_kpis[df_kpis["UBICAR_LUEGO_DE"].str.upper()==total_key].iterrows():
            nombre = kpi["KPI"].upper()
            formula = kpi["FORMULA"].strip().upper().replace(" ","_")
            try:
                val_m = eval(formula,{},ctx_m)
                val_a = eval(formula,{},ctx_a)
            except: val_m=val_a=0
            kpi_row={"GRUPO":nombre,"CUENTA":"","MENSUAL":val_m,"ANUAL":val_a}
            estructura.append(kpi_row); kpis_dict[nombre]=kpi_row

    df_estructura = pd.DataFrame(estructura)

    # Tarjetas KPI al final (igual que antes)
    kpis_para_tarjeta = []
    df_tarjetas.columns = df_tarjetas.columns.str.strip().str.upper()
    for _, fila in df_tarjetas.sort_values("ORDEN").iterrows():
        nombre = fila["KPI"].upper()
        tipo = fila.get("TIPO_DATO","MONEDA").upper()
        fuente = fila.get("FUENTE","KPI").upper()
        key = nombre if fuente=="KPI" else normalizar(nombre)
        if fuente=="GRUPO" and key in totales_por_grupo:
            m = totales_por_grupo[key]["MENSUAL"]
            a = totales_por_grupo[key]["ANUAL"]
            kpis_para_tarjeta.append({"GRUPO":nombre,"MENSUAL":m,"ANUAL":a,"TIPO_DATO":tipo})
        elif fuente=="KPI" and nombre in kpis_dict:
            r = kpis_dict[nombre]
            kpis_para_tarjeta.append({"GRUPO":nombre,"MENSUAL":r["MENSUAL"],"ANUAL":r["ANUAL"],"TIPO_DATO":tipo})

    df_kpis_tarjeta = pd.DataFrame(kpis_para_tarjeta)
    return df_estructura, df_kpis_tarjeta


def old4generar_estado_resultados_detallado(df_mes_all, df_clasificacion, df_tarjetas,
                                        año, mes, df_kpis, centro_costos=None):

    df_kpis = df_kpis[df_kpis.get('MOSTRAR_EN_PG', 1) == 1].copy()
    df_clasificacion = df_clasificacion.copy()
    df_tarjetas = df_tarjetas.copy()

    # 1️⃣ Filtrado del año completo y centros
    df_anio = df_mes_all[df_mes_all["AÑO"] == año]
    if centro_costos and centro_costos.upper() != "TODOS":
        df_anio = df_anio[df_anio["CENTRO_COSTOS"] == centro_costos]

    # 2️⃣ Separar datos del mes y del acumulado anual
    df_mes = df_anio[df_anio["MES"] == mes]
    estado_anual = df_anio[df_anio["MES"] <= mes]

    # 3️⃣ Construcción de df_cuentas con MENSUAL y ANUAL
    df_cuentas = pd.DataFrame({
        "MENSUAL": df_mes.groupby(["GRUPO", "COD_CUENTA", "CUENTA"])["VALOR"].sum(),
        "ANUAL": estado_anual.groupby(["GRUPO", "COD_CUENTA", "CUENTA"])["VALOR"].sum()
    }).fillna(0).reset_index()

    # 4️⃣ Estructura visual y orden
    clasif = df_clasificacion.drop_duplicates(subset=["GRUPO"])[["GRUPO"]]
    df_cuentas = df_cuentas.merge(clasif, on="GRUPO", how="left")
    orden = df_clasificacion.drop_duplicates(subset=["GRUPO"]).reset_index(drop=True)
    orden["ORDEN"] = orden.index
    df_cuentas = df_cuentas.merge(orden[["GRUPO", "ORDEN"]], on="GRUPO", how="left")
    df_cuentas = df_cuentas.sort_values(by=["ORDEN", "COD_CUENTA"])

    def normalizar(texto): return str(texto).strip().upper()

    estructura, totales_por_grupo, kpis_dict = [], {}, {}
    grupo_actual, valores_grupo = None, []

    # 5️⃣ Construcción de filas por grupo y cálculos KPI internos
    for _, fila in df_cuentas.iterrows():
        grupo, cuenta = fila["GRUPO"], fila["CUENTA"]
        mensual, anual = fila["MENSUAL"], fila["ANUAL"]

        if grupo != grupo_actual and grupo_actual is not None:
            total_m = sum(x["MENSUAL"] for x in valores_grupo)
            total_a = sum(x["ANUAL"] for x in valores_grupo)
            estructura.append({"GRUPO": grupo_actual, "CUENTA": "", "MENSUAL": None, "ANUAL": None})
            estructura.extend(valores_grupo)
            total_key = f"TOTAL {grupo_actual.upper()}"
            totales_por_grupo[normalizar(total_key)] = {"MENSUAL": total_m, "ANUAL": total_a}
            estructura.append({"GRUPO": total_key, "CUENTA": "", "MENSUAL": total_m, "ANUAL": total_a})

            ctx_m = {normalizar(k).replace(" ", "_"): v["MENSUAL"] for k, v in totales_por_grupo.items()}
            ctx_a = {normalizar(k).replace(" ", "_"): v["ANUAL"] for k, v in totales_por_grupo.items()}

            for _, kpi in df_kpis[df_kpis["UBICAR_LUEGO_DE"].str.upper() == total_key].iterrows():
                nombre = kpi["KPI"].upper()
                formula = kpi["FORMULA"].strip().upper().replace(" ", "_")
                try:
                    val_m = eval(formula, {}, ctx_m)
                    val_a = eval(formula, {}, ctx_a)
                except:
                    val_m = val_a = 0
                kpi_row = {"GRUPO": nombre, "CUENTA": "", "MENSUAL": val_m, "ANUAL": val_a}
                estructura.append(kpi_row)
                kpis_dict[nombre] = kpi_row

            valores_grupo = []

        grupo_actual = grupo
        valores_grupo.append({"GRUPO": "", "CUENTA": cuenta, "MENSUAL": mensual, "ANUAL": anual})

    # 6️⃣ Procesar último grupo pendiente
    if valores_grupo:
        total_m = sum(x["MENSUAL"] for x in valores_grupo)
        total_a = sum(x["ANUAL"] for x in valores_grupo)
        estructura.append({"GRUPO": grupo_actual, "CUENTA": "", "MENSUAL": None, "ANUAL": None})
        estructura.extend(valores_grupo)
        total_key = f"TOTAL {grupo_actual.upper()}"
        totales_por_grupo[normalizar(total_key)] = {"MENSUAL": total_m, "ANUAL": total_a}
        estructura.append({"GRUPO": total_key, "CUENTA": "", "MENSUAL": total_m, "ANUAL": total_a})

        ctx_m = {normalizar(k).replace(" ", "_"): v["MENSUAL"] for k, v in totales_por_grupo.items()}
        ctx_a = {normalizar(k).replace(" ", "_"): v["ANUAL"] for k, v in totales_por_grupo.items()}
        for _, kpi in df_kpis[df_kpis["UBICAR_LUEGO_DE"].str.upper() == total_key].iterrows():
            nombre = kpi["KPI"].upper()
            formula = kpi["FORMULA"].strip().upper().replace(" ", "_")
            try:
                val_m = eval(formula, {}, ctx_m)
                val_a = eval(formula, {}, ctx_a)
            except:
                val_m = val_a = 0
            kpi_row = {"GRUPO": nombre, "CUENTA": "", "MENSUAL": val_m, "ANUAL": val_a}
            estructura.append(kpi_row)
            kpis_dict[nombre] = kpi_row

    df_estructura = pd.DataFrame(estructura)

    # 7️⃣ Generación de tarjetas KPI
    kpis_para_tarjeta = []
    df_tarjetas.columns = df_tarjetas.columns.str.strip().str.upper()
    for _, fila in df_tarjetas.sort_values("ORDEN").iterrows():
        nombre = fila["KPI"].upper()
        tipo = fila.get("TIPO_DATO", "MONEDA").upper()
        fuente = fila.get("FUENTE", "KPI").upper()
        key = nombre if fuente == "KPI" else normalizar(nombre)
        if fuente == "GRUPO" and key in totales_por_grupo:
            m = totales_por_grupo[key]["MENSUAL"]
            a = totales_por_grupo[key]["ANUAL"]
            kpis_para_tarjeta.append({"GRUPO": nombre, "MENSUAL": m, "ANUAL": a, "TIPO_DATO": tipo})
        elif fuente == "KPI" and nombre in kpis_dict:
            row = kpis_dict[nombre]
            kpis_para_tarjeta.append({"GRUPO": nombre, "MENSUAL": row["MENSUAL"], "ANUAL": row["ANUAL"], "TIPO_DATO": tipo})

    df_kpis_tarjeta = pd.DataFrame(kpis_para_tarjeta)
    return df_estructura, df_kpis_tarjeta


def generar_estado_resultados_detallado(df_mes_all, df_clasificacion, df_tarjetas,
                                        año, mes, df_kpis, centro_costos=None):
    df_kpis = df_kpis[df_kpis.get('MOSTRAR_EN_PG', 1) == 1].copy()
    df_clasificacion = df_clasificacion.copy()
    df_tarjetas = df_tarjetas.copy()

    # Filtrar año actual y centro de costos (si aplica)
    df_anio = df_mes_all[df_mes_all["AÑO"] == año]
    if centro_costos and centro_costos.upper() != "TODOS":
        df_anio = df_anio[df_anio["CENTRO_COSTOS"] == centro_costos]

    # Datos del mes actual y del acumulado enero → mes seleccionado
    df_mes = df_anio[df_anio["MES"] == mes]
    estado_anual = df_anio[df_anio["MES"] <= mes]

    # Construcción de df_cuentas
    df_cuentas = pd.DataFrame({
        "MENSUAL": df_mes.groupby(["GRUPO", "COD_CUENTA", "CUENTA"])["VALOR"].sum(),
        "ANUAL": estado_anual.groupby(["GRUPO", "COD_CUENTA", "CUENTA"])["VALOR"].sum()
    }).fillna(0).reset_index()


    # Agregar orden y estructura
    df_clasificacion = df_clasificacion.drop_duplicates(subset=["GRUPO"])
    df_cuentas = df_cuentas.merge(df_clasificacion[["GRUPO"]], on="GRUPO", how="left")
    df_clasificacion["ORDEN"] = df_clasificacion.reset_index().index
    df_cuentas = df_cuentas.merge(df_clasificacion[["GRUPO", "ORDEN"]], on="GRUPO", how="left")
    df_cuentas = df_cuentas.sort_values(by=["ORDEN", "COD_CUENTA"])

    def normalizar(txt): return str(txt).strip().upper()

    estructura, totales_por_grupo, kpis_dict = [], {}, {}
    grupo_actual, valores_grupo = None, []

    for _, fila in df_cuentas.iterrows():
        grupo, cuenta = fila["GRUPO"], fila["CUENTA"]
        mensual, anual = fila["MENSUAL"], fila["ANUAL"]

        if grupo != grupo_actual and grupo_actual is not None:
            total_m = sum(x["MENSUAL"] for x in valores_grupo)
            total_a = sum(x["ANUAL"] for x in valores_grupo)
            estructura.append({"GRUPO": grupo_actual, "CUENTA": "", "MENSUAL": None, "ANUAL": None})
            estructura.extend(valores_grupo)
            total_key = f"TOTAL {grupo_actual.upper()}"
            totales_por_grupo[normalizar(total_key)] = {"MENSUAL": total_m, "ANUAL": total_a}
            estructura.append({"GRUPO": total_key, "CUENTA": "", "MENSUAL": total_m, "ANUAL": total_a})

            ctx_m = {normalizar(k).replace(" ", "_"): v["MENSUAL"] for k, v in totales_por_grupo.items()}
            ctx_a = {normalizar(k).replace(" ", "_"): v["ANUAL"] for k, v in totales_por_grupo.items()}

            for _, kpi in df_kpis[df_kpis["UBICAR_LUEGO_DE"].str.upper() == total_key].iterrows():
                nombre = kpi["KPI"].upper()
                formula = kpi["FORMULA"].strip().upper().replace(" ", "_")
                try:
                    val_m = eval(formula, {}, ctx_m)
                    val_a = eval(formula, {}, ctx_a)
                except:
                    val_m = val_a = 0
                kpi_row = {"GRUPO": nombre, "CUENTA": "", "MENSUAL": val_m, "ANUAL": val_a}
                estructura.append(kpi_row)
                kpis_dict[nombre] = kpi_row

            valores_grupo = []

        grupo_actual = grupo
        valores_grupo.append({"GRUPO": "", "CUENTA": cuenta, "MENSUAL": mensual, "ANUAL": anual})

    if valores_grupo:
        total_m = sum(x["MENSUAL"] for x in valores_grupo)
        total_a = sum(x["ANUAL"] for x in valores_grupo)
        estructura.append({"GRUPO": grupo_actual, "CUENTA": "", "MENSUAL": None, "ANUAL": None})
        estructura.extend(valores_grupo)
        total_key = f"TOTAL {grupo_actual.upper()}"
        totales_por_grupo[normalizar(total_key)] = {"MENSUAL": total_m, "ANUAL": total_a}
        estructura.append({"GRUPO": total_key, "CUENTA": "", "MENSUAL": total_m, "ANUAL": total_a})

        ctx_m = {normalizar(k).replace(" ", "_"): v["MENSUAL"] for k, v in totales_por_grupo.items()}
        ctx_a = {normalizar(k).replace(" ", "_"): v["ANUAL"] for k, v in totales_por_grupo.items()}
        for _, kpi in df_kpis[df_kpis["UBICAR_LUEGO_DE"].str.upper() == total_key].iterrows():
            nombre = kpi["KPI"].upper()
            formula = kpi["FORMULA"].strip().upper().replace(" ", "_")
            try:
                val_m = eval(formula, {}, ctx_m)
                val_a = eval(formula, {}, ctx_a)
            except:
                val_m = val_a = 0
            kpi_row = {"GRUPO": nombre, "CUENTA": "", "MENSUAL": val_m, "ANUAL": val_a}
            estructura.append(kpi_row)
            kpis_dict[nombre] = kpi_row

    df_estructura = pd.DataFrame(estructura)

    # KPIs para tarjetas
    df_tarjetas.columns = df_tarjetas.columns.str.strip().str.upper()
    tarjetas = []
    for _, fila in df_tarjetas.sort_values("ORDEN").iterrows():
        nombre = fila["KPI"].upper()
        tipo = fila.get("TIPO_DATO", "MONEDA").upper()
        fuente = fila.get("FUENTE", "KPI").upper()
        key = nombre if fuente == "KPI" else normalizar(nombre)
        if fuente == "GRUPO" and key in totales_por_grupo:
            m = totales_por_grupo[key]["MENSUAL"]
            a = totales_por_grupo[key]["ANUAL"]
            tarjetas.append({"GRUPO": nombre, "MENSUAL": m, "ANUAL": a, "TIPO_DATO": tipo})
        elif fuente == "KPI" and nombre in kpis_dict:
            r = kpis_dict[nombre]
            tarjetas.append({"GRUPO": nombre, "MENSUAL": r["MENSUAL"], "ANUAL": r["ANUAL"], "TIPO_DATO": tipo})

    df_kpis_tarjeta = pd.DataFrame(tarjetas)
    return df_estructura, df_kpis_tarjeta

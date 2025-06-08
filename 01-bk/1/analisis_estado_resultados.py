# Funcion creada para generar estado de resultados
# Creada por: Ibeth Carmona - IA
# Fecha de Creación: Junio 7-2025
# All rights reserved

import pandas as pd


def generar_estado_resultados_detallado(df_datos, archivo_parametros, año, mes, centro_costos=None):
    df_datos.columns = df_datos.columns.str.strip().str.upper()

    df_clasificacion = pd.read_excel(archivo_parametros, sheet_name="CLASIFICACION_CUENTAS", dtype={"PREFIJO": str})
    df_kpis = pd.read_excel(archivo_parametros, sheet_name="KPIS_FINANCIEROS")
    df_tarjetas = pd.read_excel(archivo_parametros, sheet_name="TARJETAS")
    df_clasificacion.columns = df_clasificacion.columns.str.strip().str.upper()
    df_kpis.columns = df_kpis.columns.str.strip().str.upper()
    df_tarjetas.columns = df_tarjetas.columns.str.strip().str.upper()

    df_datos = df_datos[df_datos["AÑO"] == año].copy()
    df_datos["PREFIJO"] = df_datos["COD_CUENTA"].astype(str).str[:2]
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

    clasif = df_clasificacion.drop_duplicates(subset=["GRUPO"])[["GRUPO", "SUBTOTAL_EN", "NATURALEZA_FINANCIERA"]]
    df_cuentas = df_cuentas.merge(clasif, on="GRUPO", how="left")

    orden = df_clasificacion.drop_duplicates(subset=["GRUPO"]).reset_index(drop=True)
    orden["ORDEN"] = orden.index
    df_cuentas = df_cuentas.merge(orden[["GRUPO", "ORDEN"]], on="GRUPO", how="left")

    df_cuentas = df_cuentas.sort_values(by=["ORDEN", "COD_CUENTA"])

    def normalizar(texto):
        return str(str(texto).strip().upper())

    estructura = []
    totales_por_grupo = {}
    kpis_para_tarjeta = []
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

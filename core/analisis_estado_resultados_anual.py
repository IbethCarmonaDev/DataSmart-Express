import pandas as pd

def generar_estado_resultados_anual(df_estado_todos, df_clasificacion, df_kpis_param, anio, centro_costos=None):
    df = df_estado_todos.copy()
    df = df[df["AÑO"] == anio]

    if centro_costos and centro_costos != "TODOS":
        df = df[df["CENTRO_COSTOS"] == centro_costos]

    columnas_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    map_meses = dict(zip(range(1, 13), columnas_meses))

    df_cuentas = df[df["TIPO"] == "CUENTA"].copy()
    df_cuentas["MES_NOMBRE"] = df_cuentas["MES"].map(map_meses)

    df_grouped = df_cuentas.groupby(["GRUPO", "COD_CUENTA", "CUENTA", "MES_NOMBRE"])["MENSUAL"].sum().reset_index()
    df_pivot = df_grouped.pivot_table(
        index=["GRUPO", "COD_CUENTA", "CUENTA"],
        columns="MES_NOMBRE",
        values="MENSUAL",
        fill_value=0
    ).reset_index()

    for mes in columnas_meses:
        if mes not in df_pivot.columns:
            df_pivot[mes] = 0

    df_clasificacion.columns = df_clasificacion.columns.str.strip().str.upper()
    orden_grupos = df_clasificacion["GRUPO"].dropna().unique().tolist()

    df_pivot["ORDEN"] = df_pivot["GRUPO"].apply(lambda x: orden_grupos.index(x) if x in orden_grupos else 999)
    df_pivot = df_pivot.sort_values(by=["ORDEN", "GRUPO", "COD_CUENTA"]).drop(columns=["ORDEN", "COD_CUENTA"])

    df_kpis_param.columns = df_kpis_param.columns.str.strip().str.upper()
    df_kpis_param = df_kpis_param[df_kpis_param.get("MOSTRAR_EN_PG", 0) == 1]

    def normalizar(texto):
        return str(texto).strip().upper().replace(" ", "_")

    def estilo_oracion(texto):
        return str(texto).capitalize()

    resultado = []
    total_por_grupo = {mes: {} for mes in columnas_meses}
    total_anual = {}

    for grupo in orden_grupos:
        df_grupo = df_pivot[df_pivot["GRUPO"] == grupo]
        if df_grupo.empty:
            continue

        resultado.append({"GRUPO": estilo_oracion(grupo), "CUENTA": "", **{mes: None for mes in columnas_meses}, "ACUMULADO": None})

        for _, fila in df_grupo.iterrows():
            fila_dict = fila.to_dict()
            fila_dict["GRUPO"] = ""
            fila_dict["CUENTA"] = estilo_oracion(fila_dict["CUENTA"])
            fila_dict["ACUMULADO"] = sum(fila_dict[mes] for mes in columnas_meses)
            resultado.append(fila_dict)

        total = df_grupo[columnas_meses].sum()
        total_key = f"TOTAL {grupo.upper()}"
        for mes in columnas_meses:
            total_por_grupo[mes][normalizar(total_key)] = total[mes]
        total_anual[normalizar(total_key)] = total.sum()

        total_dict = {"GRUPO": estilo_oracion(total_key.lower()), "CUENTA": "", **total.to_dict()}
        total_dict["ACUMULADO"] = total.sum()
        resultado.append(total_dict)

        kpis_grupo = df_kpis_param[df_kpis_param["UBICAR_LUEGO_DE"].apply(normalizar) == normalizar(total_key)]

        for _, kpi in kpis_grupo.iterrows():
            nombre_kpi = kpi["KPI"].capitalize()
            formula = normalizar(kpi["FORMULA"])
            tipo_dato = kpi.get("TIPO_DATO", "MONEDA").upper()
            fila_kpi = {"GRUPO": nombre_kpi, "CUENTA": "", "TIPO_DATO": tipo_dato}

            acumulado = 0
            for mes in columnas_meses:
                try:
                    valor = eval(formula, {}, total_por_grupo[mes])
                except:
                    valor = 0
                fila_kpi[mes] = valor
                acumulado += valor

            try:
                fila_kpi["ACUMULADO"] = eval(formula, {}, total_anual)
            except:
                fila_kpi["ACUMULADO"] = 0

            resultado.append(fila_kpi)

    df_final = pd.DataFrame(resultado)
    return df_final



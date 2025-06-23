import pandas as pd

def obtener_funcionalidades(plan, archivo_parametros):
    df_planes = pd.read_excel(archivo_parametros, sheet_name="PLANES", index_col=0)
    df_planes.index = df_planes.index.str.strip()  # Limpiar espacios
    if plan in df_planes.columns:
        return df_planes[plan].to_dict()
    else:
        return {}

def filtrar_kpis_por_plan(df_kpis, plan, archivo_parametros):
    df_kpis.columns = df_kpis.columns.str.strip().str.upper()

    if plan.upper() not in df_kpis.columns:
        return df_kpis  # Si no hay restricción, se devuelven todos

    kpis_autorizados = df_kpis[df_kpis[plan.upper()] == 1]["KPI"].str.upper().tolist()
    return df_kpis[df_kpis["KPI"].str.upper().isin(kpis_autorizados)]

def obtener_graficas_por_plan(plan, df_graficas):
    if plan not in df_graficas.columns:
        return pd.DataFrame()  # Retorna un DataFrame vacío si no existe la columna del plan
    df_graficas_activas = df_graficas[df_graficas[plan] == 1]
    df_graficas_activas = df_graficas_activas.sort_values("ORDEN")
    return df_graficas_activas
import os
import pandas as pd
from datetime import datetime

def registrar_log(nombre_evento, duracion):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    ruta_log = os.path.join(log_dir, "tiempos_procesamiento.csv")
    tiempo_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_log = pd.DataFrame([[tiempo_actual, nombre_evento, duracion]], columns=["FECHA", "EVENTO", "TIEMPO_SEG"])
    if os.path.exists(ruta_log):
        df_log.to_csv(ruta_log, mode="a", header=False, index=False)
    else:
        df_log.to_csv(ruta_log, index=False)



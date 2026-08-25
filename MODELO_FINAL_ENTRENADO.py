import pandas as pd
import numpy as np
from xgboost import XGBRegressor
import joblib

# 1. Carga y Limpieza Completa
df = pd.read_excel('dataset_modelo_final.xlsx')
df['fecha'] = pd.to_datetime(df['fecha'])

# Filtrado de la ruptura estructural COVID-19
df_clean = df[~((df['fecha'] >= '2020-03-01') & (df['fecha'] <= '2021-06-30'))].copy()
df_clean = df_clean.dropna(subset=['VIAJEROS_lag1', 'VIAJEROS_lag12']).reset_index(drop=True)

# Transformación Delta
df_clean['DELTA_12'] = df_clean['VIAJEROS'] - df_clean['VIAJEROS_lag12']
df_clean['RATIO_LAG1'] = df_clean['VIAJEROS_lag1'] / (df_clean['VIAJEROS_lag12'] + 1e-5)

features = ['np_010', 'nt_30', 'n_des', 'mes', 'dias_libres_totales', 'semana_santa', 'RATIO_LAG1']
regiones = ['Asturias', 'Galicia', 'País Vasco', 'Madrid']

df_resultados_global = pd.DataFrame()

# 2. Reentrenamiento con el 100% de los datos y Exportación
for reg in regiones:
    df_reg = df_clean[df_clean[reg] == 1].sort_values('fecha').reset_index(drop=True)
    
    # Matriz completa (Train + Test unificados)
    X_full = df_reg[features]
    y_full_delta = df_reg['DELTA_12']
    
    # Ajuste del modelo final
    model_final = XGBRegressor(
        n_estimators=150,
        learning_rate=0.04,
        max_depth=3,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )
    model_final.fit(X_full, y_full_delta)
    
    # Guardar el modelo entrenado en disco
    nombre_archivo = f'modelo_XGB_{reg.replace(" ", "_")}.pkl'
    joblib.dump(model_final, nombre_archivo)
    
    # Generar ajuste histórico completo
    pred_delta_full = model_final.predict(X_full)
    df_reg['PREDICCION_FINAL'] = df_reg['VIAJEROS_lag12'] + pred_delta_full
    df_reg['ERROR_ABSOLUTO'] = np.abs(df_reg['VIAJEROS'] - df_reg['PREDICCION_FINAL'])
    
    df_resultados_global = pd.concat([df_resultados_global, df_reg], ignore_index=True)

# 3. Exportar resultados ajustados a Excel
columnas_exportar = ['fecha', 'Asturias', 'Galicia', 'País Vasco', 'Madrid', 
                     'VIAJEROS', 'PREDICCION_FINAL', 'ERROR_ABSOLUTO']
df_resultados_global[columnas_exportar].to_excel('predicciones_modelos_finales.xlsx', index=False)

print("¡Modelos finales entrenados con el 100% de los datos!")
print("Archivos .pkl guardados por región y dataset consolidado 'predicciones_modelos_finales.xlsx' generado.")
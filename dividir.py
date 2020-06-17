# -*- coding: utf-8 -*-
u"""
Stripct usado para dividir las preguntas aumentadas en 5 archivos.

* consulta_afip.csv: (identificación unívoca consulta AFIP (IUCA), Texto Consulta AFIP)
* consulta_usuario.csv: (IUCA , Texto Consulta Usuario)
* respuesta_afip.csv: (IUCA , Texto Respuesta AFIP)
* respuesta_bill.csv: (IUCA , Texto Respuesta Bill)
* preg_cat.csv: (IUCA , Categoría)
"""
from __future__ import print_function
from os import makedirs
from sys import argv
import pandas as pd

DATASET_FILE = argv[1] if len(argv) > 1 else 'dataset-afip-aumentado.csv'
PATH = "dataset_dividido/"
makedirs(PATH, exist_ok=True)

df = pd.read_csv('dataset-afip-completo.csv', sep=';')
df.insert(0, "IUCA", range(len(df)), True)

print("Creando archivo 'consulta_afip.csv'")
df_con_afip = pd.DataFrame({"IUCA": df["IUCA"],
                            "Texto Consulta AFIP": df["Pregunta ABC AFIP"]})
df_con_afip.to_csv(PATH + "consulta_afip.csv", index=False)

print("Creando archivo 'respuesta_afip.csv'")
df_con_afip = pd.DataFrame({"IUCA": df["IUCA"],
                            "Texto Respuesta AFIP": df["Respuesta AFIP"]})
df_con_afip.to_csv(PATH + "respuesta_afip.csv", index=False)

print("Creando archivo 'respuesta_bill.csv'")
df_con_afip = pd.DataFrame({"IUCA": df["IUCA"],
                            "Texto Respuesta Bill": df["Respuesta Bill"]})
df_con_afip.to_csv(PATH + "respuesta_bill.csv", index=False)

print("Creando archivo 'preg_cat.csv'")
df_con_afip = pd.DataFrame(df[["IUCA", "Categoría"]])
df_con_afip.to_csv(PATH + "preg_cat.csv", index=False)

print("Creando archivo 'consulta_usuario.csv'")
to_id = dict([(str(p), id)
              for p, id in df[["Pregunta ABC AFIP", "IUCA"]].values.tolist()])
df_aumentado = pd.read_csv(DATASET_FILE, sep=';').dropna()
df_con_usuario = pd.DataFrame({
    "IUCA": [to_id[p]
             if p in to_id else
             to_id[' ' + p] if ' ' + p in to_id else
             to_id[p + '\n'] if p + '\n' in to_id else
             to_id[p.rstrip('?')] if p.rstrip('?') in to_id else
             to_id[p.rstrip('\n')]
             for p in df_aumentado["Pregunta ABC AFIP"].values.tolist()],
    "Texto Consulta Usuario": df_aumentado["Preguntas Similares"]
})
df_con_usuario.to_csv(PATH + "consulta_usuario.csv", index=False)

# print(len(pd.read_csv(PATH + 'consulta_afip.csv')))
# print(len(pd.read_csv(PATH + 'respuesta_afip.csv')))
# print(len(pd.read_csv(PATH + 'respuesta_bill.csv')))
# print(len(pd.read_csv(PATH + 'preg_cat.csv')))
# print(len(pd.read_csv(PATH + 'consulta_usuario.csv')))

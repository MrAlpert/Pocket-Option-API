"""
Autor: AdminhuDev
"""
import pandas as pd

# Lê os arquivos CSV
df_1 = pd.read_csv('dados_completos_AUDNZD_otc.csv')
df_2 = pd.read_csv('dados_completos_AUDNZD_otc_2.csv')

# Concatena os dataframes
df_full = pd.concat([df_1, df_2], axis=0)
print(df_full.shape)
# Salva o resultado
df_full.to_csv('dados_full_AUDNZD_otc.csv', index=False)

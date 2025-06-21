import pandas as pd
import matplotlib.pyplot as plt

# Lê o CSV
df = pd.read_csv('dados.csv')

# Converte tempo de ms para segundos
df['Tempo_s'] = df['Tempo_ms'] / 1000

# Cria figura com dois gráficos
plt.figure(figsize=(12, 6))

# Gráfico de Movimento
plt.subplot(2, 1, 1)
plt.plot(df['Tempo_s'], df['Movimento'], drawstyle='steps-post', color='red')
plt.xlabel('Tempo (s)')
plt.ylabel('Movimento (0 = não, 1 = sim)')
plt.title('Detecção de Movimento')
plt.grid(True)

# Gráfico de LDR
plt.subplot(2, 1, 2)
plt.plot(df['Tempo_s'], df['LDR'], color='blue')
plt.xlabel('Tempo (s)')
plt.ylabel('Valor LDR')
plt.title('Intensidade de Luz (Sensor LDR)')
plt.grid(True)

plt.tight_layout()
plt.show()

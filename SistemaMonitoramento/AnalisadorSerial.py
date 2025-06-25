import serial
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# Configurações
porta = 'COM5'
baudrate = 9600
arquivo_saida = 'dados.csv'

# Buffer dos gráficos
buffer_size = 100
tempos = deque(maxlen=buffer_size)
movimentos = deque(maxlen=buffer_size)
ldr_vals = deque(maxlen=buffer_size)

# Inicializa conexão serial
ser = serial.Serial(porta, baudrate, timeout=1)
print(f"Lendo dados da porta {porta}...")

# Arquivo CSV
csv_file = open(arquivo_saida, mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Tempo_ms', 'Movimento', 'LDR'])

# Inicializa gráficos
fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle("Leitura em Tempo Real")
line1, = ax1.plot([], [], 'r-', label='Movimento')
line2, = ax2.plot([], [], 'b-', label='LDR')

ax1.set_ylabel("Movimento")
ax2.set_ylabel("LDR")
ax2.set_xlabel("Tempo (ms)")
ax1.set_ylim(-0.1, 1.1)  # Para movimento (0 ou 1)
ax1.legend()
ax2.legend()

# Atualização dos gráficos
def update(frame):
    linha = ser.readline().decode(errors='ignore').strip()
    if linha:
        print(linha)
        try:
            partes = linha.replace("Tempo(ms):", "").replace("Movimento:", "").replace("LDR:", "").split('|')
            if len(partes) == 3:
                tempo = int(partes[0].strip())
                movimento = int(partes[1].strip())
                ldr = int(partes[2].strip())

                # Adiciona ao CSV
                csv_writer.writerow([tempo, movimento, ldr])

                # Atualiza buffers
                tempos.append(tempo)
                movimentos.append(movimento)
                ldr_vals.append(ldr)

                # Atualiza dados dos gráficos
                line1.set_data(tempos, movimentos)
                line2.set_data(tempos, ldr_vals)

                ax1.set_xlim(max(0, tempo - 10000), tempo)
                ax2.set_xlim(max(0, tempo - 10000), tempo)
                ax2.set_ylim(min(ldr_vals, default=0) - 10, max(ldr_vals, default=100) + 10)
        except:
            print("Erro ao processar linha.")

    return line1, line2

# Inicia animação
ani = animation.FuncAnimation(fig, update, interval=100)

try:
    plt.tight_layout()
    plt.show()
except KeyboardInterrupt:
    print("Interrompido.")
finally:
    ser.close()
    csv_file.close()

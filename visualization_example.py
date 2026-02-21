import matplotlib.pyplot as plt

# Recuperamos los tiempos de la parte de matrices (Valores simulados ya que las variables no estan definidas en el snippet)
# Asumiendo valores de ejemplo basados en la descripción del gráfico
tiempo_simple = 5.0
tiempo_bloques_sec = 4.5
tiempo_bloques_par = 1.2

tiempos_matrices = [tiempo_simple, tiempo_bloques_sec, tiempo_bloques_par]
etiquetas_matrices = ['Simple', 'Bloques\nSecuencial', 'Bloques\nParalelo (MP)']
colores_matrices = ['#333333', '#666666', '#999999'] # Escala de grises Carlemany

# Output de cProfile
labels_finanzas = ['Esperando Red (I/O)', 'Procesamiento CPU']
sizes_finanzas = [95, 5] # 1.6s descarga vs ms proceso)
colores_finanzas = ['#F3A618', '#001C47'] # Colores divergentes Carlemany

# Figura
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Matrices (eficacia del Multiprocessing)
bars = ax1.bar(etiquetas_matrices, tiempos_matrices, color=colores_matrices, edgecolor='grey')
ax1.set_ylabel('Tiempo (segundos)')
ax1.set_title('Conclusión 1: Eficacia de la Paralelización (CPU-Bound)', fontsize=12, fontweight='bold')
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# Añadir el valor encima de las barras
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.4f}s',
             ha='center', va='bottom')

# segundo gráfico justificación I/O Bound
# explode debe ser una tupla de longitud igual a sizes_finanzas
# sizes_finanzas tiene 2 elementos, el código del usuario tenía una tupla de 2 elementos tambien.
explode = (0.1, 0) 

ax2.pie(sizes_finanzas, labels=labels_finanzas, autopct='%1.1f%%',
        startangle=90, colors=colores_finanzas, explode=explode, shadow=True)
ax2.set_title('Cuello de Botella en Finanzas (I/O-Bound)', fontsize=12, fontweight='bold')

# Ajuste final
plt.suptitle('Visualización de conclusiones', fontsize=16)
plt.tight_layout()
plt.show()

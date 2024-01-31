import json
import matplotlib.pyplot as plt
import random

# Cargar el archivo JSON
with open('../registros.json') as file:
    data = json.load(file)

# Crear listas para almacenar los promedios y las ventas de cada producto
promedios_good = []
promedios_bad = []
ventas = []
product_names = []

# Obtener la cantidad total de productos
total_productos = len(data['products'])

# Generar colores aleatorios para cada producto (formato hexadecimal RGB)
colores = [f'#{random.randint(0, 0xFFFFFF):06x}' for _ in range(total_productos)]

# Color rojo para las opiniones malas
color_bad = 'red'

# Iterar sobre los productos
for product in data['products']:
    product_names.append(product['Title'])

    # Obtener las ventas y el número de opiniones buenas y malas
    ventas.append(int(product['Sale']['Amount']))

    opiniones_good = 0
    opiniones_bad = 0

    if isinstance(product['RatingOpinion'], list):
        for rating in product['RatingOpinion']:
            if rating['Rating'] == 'Good':
                opiniones_good += int(rating['Amount'])
            elif rating['Rating'] == 'Bad':
                opiniones_bad += int(rating['Amount'])
    else:
        if product['RatingOpinion']['Rating'] == 'Good':
            opiniones_good = int(product['RatingOpinion']['Amount'])
        elif product['RatingOpinion']['Rating'] == 'Bad':
            opiniones_bad = int(product['RatingOpinion']['Amount'])

    # Calcular los promedios y agregarlos a las listas
    promedio_good = opiniones_good / ventas[-1]
    promedios_good.append(promedio_good)

    promedio_bad = opiniones_bad / ventas[-1]
    promedios_bad.append(promedio_bad)

# Crear el gráfico de barras con colores aleatorios para cada producto y rojo para opiniones malas
plt.figure(figsize=(10, 6))
plt.bar(range(len(promedios_good)), promedios_good, color=colores, alpha=0.7)
plt.bar(range(len(promedios_bad)), promedios_bad, color=color_bad, alpha=0.7)

# Configurar el título y las etiquetas de los ejes
plt.title('Promedio de opiniones buenas y malas por ventas')
plt.ylabel('Promedio')

# Crear la guía de colores
plt.figure(figsize=(4, 2))
plt.bar([0], [0], color=color_bad, label='Malas')
for i, color in enumerate(colores):
    plt.bar([0], [0], color=color, label=product_names[i])
plt.legend(loc='center')

# Mostrar el gráfico y la guía de colores
plt.show()



import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
import json
import numpy as np
from matplotlib.cm import tab20
import textwrap

# Cargar el JSON desde un archivo
with open("../offers.json", "r") as file:
    json_data = json.load(file)

# Obtener la lista de productos del JSON
products = json_data["products"]

# Crear una lista para almacenar los datos de los productos
data = []

# Iterar sobre los productos y extraer los datos relevantes
for product in products:
    title = product["Title"]
    days = product["Sale"]["Days"]
    amount = product["Sale"]["Amount"]

    # Obtener el valor numérico de "Amount" eliminando caracteres no deseados
    if amount.startswith("+"):
        amount = amount[1:]
    amount = amount.replace("mil", "000").replace(",", "")

    # Convertir a entero si es posible, de lo contrario asignar NaN
    try:
        amount = int(amount)
    except ValueError:
        amount = np.nan

    data.append({"Title": title, "Days": days, "Amount": amount})

# Convertir los datos en un DataFrame
data = pd.DataFrame(data)

# Reemplazar los valores cero por NaN en la columna "Amount"
data["Amount"] = data["Amount"].replace(0, np.nan)

# Eliminar los datos no numéricos de la columna "Amount"
data = data[data["Amount"].notnull()]

# Verificar si el DataFrame está vacío
if data.empty:
    print("No hay datos disponibles para graficar.")
    exit()

# Ordenar los datos por ventas en orden ascendente
data = data.sort_values(by="Amount", ascending=True)

# Obtener el top 20 de productos
top_20_data = data.tail(20)

# Ordenar el top 20 de menor a mayor
top_20_data = top_20_data.sort_values(by="Amount")

# Generar colores aleatorios para cada producto
categories = top_20_data["Title"].apply(lambda x: str(hash(x)))
colors = tab20.colors[:len(categories)]

# Limitar el nombre de los productos en la paleta de colores
wrapped_labels = [textwrap.wrap(label, width=10)[0] for label in top_20_data["Title"]]

# Crear una figura con un subplot
fig, ax = plt.subplots(figsize=(10, 6))

# Configurar el gráfico de barras
bars = ax.bar(top_20_data.index, top_20_data["Amount"], color=colors, width=0.8)

# Configurar los ejes y etiquetas
ax.set_xlabel("Productos")
ax.set_ylabel("Ventas")
ax.set_title("Top 20 Productos por Ventas")
ax.tick_params(axis="x", labelrotation=45, labelsize=8)

# Mostrar la guía de colores fuera de la gráfica
legend_elements = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors]
plt.legend(legend_elements, wrapped_labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)

# Obtener el producto con la mejor cantidad y el producto con la menor cantidad
best_product = top_20_data.loc[top_20_data["Amount"].idxmax(), "Title"]
worst_product = top_20_data.loc[top_20_data["Amount"].idxmin(), "Title"]

# Agregar leyendas para el mejor y peor producto en la parte superior e inferior de la gráfica
ax.text(-0.1, 1.1, f"Mejor Producto: {best_product}", color="black", fontsize=10, ha="left", va="center", transform=ax.transAxes)
ax.text(-0.1, -0.15, f"Peor Producto: {worst_product}", color="black", fontsize=10, ha="left", va="center", transform=ax.transAxes)

# Ajustar el espacio entre subplots y margen
plt.tight_layout()

# Mostrar el gráfico
plt.show()



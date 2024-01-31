import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
from mpl_toolkits.mplot3d import Axes3D

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
    price = product.get("DiscountPrice", product["OriginalPrice"])
    data.append({"Title": title, "Price": price})

# Convertir los datos en un DataFrame y ordenar por precio descendente
data = pd.DataFrame(data).sort_values("Price", ascending=False)

# Obtener los datos del top 20, el producto más caro y el producto más barato
top_20 = data.head(20)
producto_mas_caro = data.iloc[0]
producto_mas_barato = data.iloc[-1]

# Generar colores aleatorios para cada producto
colors = []
for _ in range(len(data)):
    colors.append(random.choice(list(mcolors.CSS4_COLORS.values())))

# Crear la figura y el subplot 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Configurar los datos para la gráfica 3D
x = range(len(data))
y = data["Price"]
z = range(1, len(data)+1)

# Generar los puntos 3D con los colores aleatorios
ax.scatter(x, y, z, c=colors, s=50)

# Configurar título y etiquetas del eje Z
ax.set_xlabel('Productos')
ax.set_ylabel('Precio')
ax.set_zlabel('Cantidad de productos')
ax.set_title('Precios de los productos')

# Configurar la guía de colores
custom_legend = []
legend_labels = []

# Mostrar el top 20 en la guía de colores
for i, row in top_20.iterrows():
    custom_legend.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[i], markersize=10))
    legend_labels.append(row["Title"][:10])

# Agregar el producto más caro y el más barato a la guía de colores
custom_legend.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10))
legend_labels.append(f"Producto más caro: {producto_mas_caro['Title'][:10]} - {producto_mas_caro['Price']}")

custom_legend.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10))
legend_labels.append(f"Producto más barato: {producto_mas_barato['Title'][:10]} - {producto_mas_barato['Price']}")

# Mostrar la guía de colores al lado de la gráfica
plt.legend(custom_legend, legend_labels, loc='center left', bbox_to_anchor=(1.05, 0.5))

# Mostrar la figura
plt.show()



import json
import pandas as pd
import matplotlib.pyplot as plt
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
    title = product["Title"][:15]  # Mostrar solo los primeros 15 caracteres del título
    price = product.get("DiscountPrice", product["OriginalPrice"])
    rating = float(product["Rating"]["Rating"])
    rating_amount_str = product["Rating"]["Amount"].replace("+", "")
    
    # Omitir los casos en los que Rating es 0 o Amount está vacío
    if rating != 0 and rating_amount_str:
        # Eliminar palabras no numéricas de Amount
        rating_amount_str = ''.join(filter(str.isdigit, rating_amount_str))
        
        # Verificar si rating_amount_str es un número válido
        if rating_amount_str.isdigit():
            rating_amount = int(rating_amount_str)
        else:
            rating_amount = 0
        
        data.append({"Title": title, "Price": price, "Rating": rating, "RatingAmount": rating_amount})

# Convertir los datos en un DataFrame
data = pd.DataFrame(data)

# Ordenar los productos por precio y cantidad de ratings
data = data.sort_values(by=["Price", "RatingAmount"])

# Obtener los top 20 productos
top_20 = data.head(20)

# Generar una lista de colores únicos para cada producto en los top 20
colors = random.choices(list(range(len(top_20))), k=len(top_20))

# Crear una figura y subplots
fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(121, projection='3d')  # Subplot para la gráfica tridimensional
ax2 = fig.add_subplot(122)  # Subplot para la guía de colores

# Configurar la gráfica de dispersión tridimensional
scatter = ax1.scatter(data["RatingAmount"], data["Price"], data["Rating"], c=data.index, cmap='rainbow', s=50, alpha=0.8)

# Configurar los ejes de la gráfica tridimensional
ax1.set_xlabel("Cantidad de Ratings")
ax1.set_ylabel("Precio")
ax1.set_zlabel("Rating")
ax1.set_title("Dispersión Tridimensional de Productos")

# Mostrar los puntos correspondientes a los top 20 productos
top_20_colors = [data.index.get_loc(i) for i in top_20.index]
ax1.scatter(top_20["RatingAmount"], top_20["Price"], top_20["Rating"], c=top_20_colors, cmap='rainbow', s=100, alpha=1.0)

# Configurar la guía de colores
ax2.scatter([1] * len(top_20_colors), list(range(len(top_20_colors))), c=top_20_colors, cmap='rainbow', s=100, alpha=1.0)
ax2.set_xticks([])
ax2.set_yticks(list(range(len(top_20_colors))))
ax2.set_yticklabels([f"{product.Title}  " for product in top_20.itertuples()], ha='left', va='center', fontsize=8)
ax2.set_title("Guía de Colores")

# Mostrar la leyenda con el producto de mayor y menor rating
max_product = data.loc[data["Rating"].idxmax()]
min_product = data.loc[data["Rating"].idxmin()]
plt.suptitle(f"Producto con mayor rating: {max_product['Title']} ({max_product['Rating']} estrellas)\n"
             f"Producto con menor rating: {min_product['Title']} ({min_product['Rating']} estrellas)")

# Ajustar el diseño y mostrar la figura
plt.tight_layout(rect=[0, 1, 1.2, 1])  # Ajustar el rectángulo para evitar superposición con la guía de colores
plt.show()

#from django.test import TestCase
from apps.productos.models import Producto

from .models import Producto

# Create your tests here.
import random


productos = [
    {"nombre": "iPhone 14 Pro Max", "descripcion": "Smartphone de última generación", "precio": 1200, "categoria": 8, "stock": 0},
    {"nombre": "Televisor Samsung QLED 75 pulgadas", "descripcion": "Pantalla de alta resolución para una experiencia inmersiva", "precio": 2500, "categoria": 4, "stock": 0},
    {"nombre": "Batidora de vaso Oster", "descripcion": "Potente batidora para preparar todo tipo de bebidas", "precio": 200, "categoria": 4, "stock": 0},
    {"nombre": "Rimel de pestañas Maybelline", "descripcion": "Rimel alargador y voluminizador", "precio": 30, "categoria": 2, "stock": 0},
    {"nombre": "Lego Star Wars", "descripcion": "Set de construcción con personajes icónicos", "precio": 100, "categoria": 9, "stock": 0},
    {"nombre": "Nintendo Switch OLED", "descripcion": "Consola de videojuegos portátil y de sobremesa", "precio": 350, "categoria": 8, "stock": 0},
    {"nombre": "Cafetera Nespresso", "descripcion": "Máquina de café espresso en cápsulas", "precio": 350, "categoria": 4, "stock": 0},
    {"nombre": "Sérum facial The Ordinary", "descripcion": "Tratamiento facial hidratante y rejuvenecedor", "precio": 25, "categoria": 2, "stock": 0},
    {"nombre": "Robot aspirador Roomba", "descripcion": "Aspirador automático para una limpieza eficiente", "precio": 500, "categoria": 4, "stock": 0},
    {"nombre": "Bicicleta de montaña Specialized", "descripcion": "Bicicleta de alta gama para todo terreno", "precio": 1500, "categoria": 3, "stock": 0},
    {"nombre": "Guitarra eléctrica Fender", "descripcion": "Guitarra eléctrica clásica para principiantes y profesionales", "precio": 800, "categoria": 3, "stock": 0},
    {"nombre": "Consola PlayStation 5", "descripcion": "La última generación de consolas de videojuegos", "precio": 500, "categoria": 8, "stock": 0},
    {"nombre": "Perfume Chanel N°5", "descripcion": "Clásico perfume femenino", "precio": 150, "categoria": 2, "stock": 0},
    {"nombre": "Muñeca Barbie", "descripcion": "Muñeca clásica para niñas", "precio": 30, "categoria": 9, "stock": 0},
    {"nombre": "Zapatilla deportiva Nike Air Force 1", "descripcion": "Zapatillas icónicas y cómodas", "precio": 120, "categoria": 7, "stock": 0},
    {"nombre": "Auriculares inalámbricos AirPods Pro", "descripcion": "Auriculares con cancelación de ruido activa", "precio": 250, "categoria": 8, "stock": 0},
    {"nombre": "Freidora de aire Philips", "descripcion": "Cocina saludable con aire caliente", "precio": 150, "categoria": 4, "stock": 0},
    {"nombre": "Tablet Samsung Galaxy Tab S8", "descripcion": "Tablet de alta resolución para entretenimiento y productividad", "precio": 800, "categoria": 8, "stock": 0},
    {"nombre": "Juego de mesa Monopoly", "descripcion": "Clásico juego de mesa para toda la familia", "precio": 50, "categoria": 9, "stock": 0},
    {"nombre": "Libro de cocina de Jamie Oliver", "descripcion": "Recetas deliciosas y fáciles de seguir", "precio": 30, "categoria": 1, "stock": 0}
]


for i in range(1, 6000):
    producto_ale = random.choice(productos)
    p = Producto(
        nombre=producto_ale['nombre'],
        descripcion=producto_ale['descripcion'],
        precio=producto_ale['precio'],
        categoria_id=producto_ale['categoria'],
        cantidad_en_stock=producto_ale['stock']
    )
    p.save()




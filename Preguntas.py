import csv
import os

def cargar_preguntas_desde_csv():
    """Carga las preguntas desde el archivo CSV con estadísticas"""
    lista_preguntas = []
    
    try:
        with open('preguntas.csv', 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                pregunta = {
                    "pregunta": fila["pregunta"],
                    "respuesta_1": fila["respuesta_1"],
                    "respuesta_2": fila["respuesta_2"],
                    "respuesta_3": fila["respuesta_3"],
                    "respuesta_4": fila["respuesta_4"],
                    "respuesta_correcta": int(fila["respuesta_correcta"]),
                    "porcentaje_aciertos": float(fila["porcentaje_aciertos"]),
                    "cantidad_fallos": int(fila["cantidad_fallos"]),
                    "cantidad_aciertos": int(fila["cantidad_aciertos"]),
                    "cantidad_veces_preguntada": int(fila["cantidad_veces_preguntada"])
                }
                lista_preguntas.append(pregunta)
    except FileNotFoundError:
        # Si no existe el CSV, usar la lista original
        lista_preguntas = [
            {"pregunta":"¿En qué ciudad nació Lionel Messi?", "respuesta_1":"Rosario","respuesta_2":"Buenos Aires","respuesta_3":"Córdoba","respuesta_4":"La Plata","respuesta_correcta":1, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Cuál es la capital de Argentina?", "respuesta_1": "Buenos Aires", "respuesta_2": "Córdoba", "respuesta_3": "Rosario", "respuesta_4": "Mendoza", "respuesta_correcta": 1, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿En qué año ganó Argentina su primer mundial de fútbol?", "respuesta_1": "1978", "respuesta_2": "1986", "respuesta_3": "2002", "respuesta_4": "1994", "respuesta_correcta": 1, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Quién es conocido como el 'Padre de la Patria' en Argentina?", "respuesta_1": "Juan Manuel de Rosas", "respuesta_2": "José de San Martín", "respuesta_3": "Manuel Belgrano", "respuesta_4": "Bartolomé Mitre", "respuesta_correcta": 2, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Cuál es el pico más alto de Argentina?", "respuesta_1": "Cerro Aconcagua", "respuesta_2": "Cerro Tronador", "respuesta_3": "Cerro Fitz Roy", "respuesta_4": "Cerro Champaquí", "respuesta_correcta": 1, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Qué río separa a Argentina de Uruguay?", "respuesta_1": "Río Paraná", "respuesta_2": "Río Colorado", "respuesta_3": "Río de la Plata", "respuesta_4": "Río Uruguay", "respuesta_correcta": 3, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Quién compuso la canción 'Gracias a la Vida'?", "respuesta_1": "Mercedes Sosa", "respuesta_2": "Charly García", "respuesta_3": "Violeta Parra", "respuesta_4": "Fito Páez", "respuesta_correcta": 3, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿En qué año fue elegido presidente Néstor Kirchner?", "respuesta_1": "2000", "respuesta_2": "2003", "respuesta_3": "2007", "respuesta_4": "2011", "respuesta_correcta": 2, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿En qué provincia se encuentra la ciudad de Ushuaia?", "respuesta_1": "Santa Cruz", "respuesta_2": "Chubut", "respuesta_3": "Tierra del Fuego", "respuesta_4": "Neuquén", "respuesta_correcta": 3, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Qué moneda se utiliza en Argentina?", "respuesta_1": "Dólar", "respuesta_2": "Peso", "respuesta_3": "Real", "respuesta_4": "Euro", "respuesta_correcta": 2, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Qué famoso cantante argentino popularizó el tango?", "respuesta_1": "Astor Piazzolla", "respuesta_2": "Carlos Gardel", "respuesta_3": "Sandro", "respuesta_4": "Luis Alberto Spinetta", "respuesta_correcta": 2, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Cuál es la danza tradicional de Argentina?", "respuesta_1": "Salsa", "respuesta_2": "Cumbia", "respuesta_3": "Tango", "respuesta_4": "Cueca", "respuesta_correcta": 3, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Cuál es el nombre del famoso glaciar en la Patagonia?", "respuesta_1": "Perito Moreno", "respuesta_2": "Martial", "respuesta_3": "Upsala", "respuesta_4": "Spegazzini", "respuesta_correcta": 1, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Quién es el autor de 'Martín Fierro'?", "respuesta_1": "Jorge Luis Borges", "respuesta_2": "José Hernández", "respuesta_3": "Julio Cortázar", "respuesta_4": "Ricardo Güiraldes", "respuesta_correcta": 2, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Cuál es la montaña más alta de América del Sur?", "respuesta_1": "Cerro Bonete", "respuesta_2": "Monte Pissis", "respuesta_3": "Aconcagua", "respuesta_4": "Cerro Mercedario", "respuesta_correcta": 3, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Qué bebida es famosa en Argentina?", "respuesta_1": "Tequila", "respuesta_2": "Mate", "respuesta_3": "Pisco", "respuesta_4": "Café", "respuesta_correcta": 2, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Cuál es el nombre del teatro más famoso de Buenos Aires?", "respuesta_1": "Teatro Colón", "respuesta_2": "Teatro Gran Rex", "respuesta_3": "Teatro Nacional", "respuesta_4": "Teatro Cervantes", "respuesta_correcta": 1, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Cuál es la Avenida más ancha del mundo ubicada en Buenos Aires?", "respuesta_1": "Avenida de Mayo", "respuesta_2": "Avenida Corrientes", "respuesta_3": "Avenida 9 de Julio", "respuesta_4": "Avenida Libertador", "respuesta_correcta": 3, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Qué prócer argentino creó la bandera?", "respuesta_1": "Domingo Sarmiento", "respuesta_2": "José de San Martín", "respuesta_3": "Manuel Belgrano", "respuesta_4": "Juan Lavalle", "respuesta_correcta": 3, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Qué actriz argentina fue esposa de Juan Domingo Perón?", "respuesta_1": "Tita Merello", "respuesta_2": "Eva Perón", "respuesta_3": "Libertad Lamarque", "respuesta_4": "Mirtha Legrand", "respuesta_correcta": 2, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿En qué año fue la Guerra de las Malvinas?", "respuesta_1": "1980", "respuesta_2": "1982", "respuesta_3": "1984", "respuesta_4": "1976", "respuesta_correcta": 2, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Cuál es el nombre del equipo de fútbol conocido como 'La Academia'?", "respuesta_1": "Boca Juniors", "respuesta_2": "Racing Club", "respuesta_3": "River Plate", "respuesta_4": "San Lorenzo", "respuesta_correcta": 2, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿En qué provincia se encuentra la ciudad de Mendoza?", "respuesta_1": "Santa Fe", "respuesta_2": "San Juan", "respuesta_3": "Mendoza", "respuesta_4": "La Rioja", "respuesta_correcta": 3, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Cuál es el ave nacional de Argentina?", "respuesta_1": "Cóndor", "respuesta_2": "Ñandú", "respuesta_3": "Hornero", "respuesta_4": "Carancho", "respuesta_correcta": 3, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Qué escritora argentina ganó el Premio Cervantes en 2018?", "respuesta_1": "Silvina Ocampo", "respuesta_2": "María Elena Walsh", "respuesta_3": "María Teresa Andruetto", "respuesta_4": "Samanta Schweblin", "respuesta_correcta": 3, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0},
            {"pregunta": "¿Qué ciudad argentina es conocida por sus cataratas?", "respuesta_1": "Misiones", "respuesta_2": "Puerto Iguazú", "respuesta_3": "Cataratas de Córdoba", "respuesta_4": "Bariloche", "respuesta_correcta": 2, "porcentaje_aciertos":0, "cantidad_fallos":0, "cantidad_aciertos":0, "cantidad_veces_preguntada":0}
        ]
    
    return lista_preguntas

def guardar_preguntas_a_csv(lista_preguntas):
    """Guarda las preguntas con estadísticas al archivo CSV"""
    try:
        with open('preguntas.csv', 'w', newline='', encoding='utf-8') as archivo:
            campos = ['pregunta', 'respuesta_1', 'respuesta_2', 'respuesta_3', 'respuesta_4', 
                     'respuesta_correcta', 'porcentaje_aciertos', 'cantidad_fallos', 
                     'cantidad_aciertos', 'cantidad_veces_preguntada']
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(lista_preguntas)
    except Exception as e:
        print(f"Error al guardar el archivo CSV: {e}")

def actualizar_estadistica_pregunta(lista_preguntas, indice_pregunta, respuesta_correcta):
    """Actualiza las estadísticas de una pregunta específica"""
    if 0 <= indice_pregunta < len(lista_preguntas):
        pregunta = lista_preguntas[indice_pregunta]
        pregunta["cantidad_veces_preguntada"] += 1
        
        if respuesta_correcta:
            pregunta["cantidad_aciertos"] += 1
        else:
            pregunta["cantidad_fallos"] += 1
        
        # Calcular porcentaje de aciertos
        total_respuestas = pregunta["cantidad_aciertos"] + pregunta["cantidad_fallos"]
        if total_respuestas > 0:
            pregunta["porcentaje_aciertos"] = (pregunta["cantidad_aciertos"] / total_respuestas) * 100
        else:
            pregunta["porcentaje_aciertos"] = 0

def obtener_pregunta_por_indice(lista_preguntas, indice):
    """Obtiene una pregunta específica por su índice"""
    if 0 <= indice < len(lista_preguntas):
        return lista_preguntas[indice]
    return None

# Cargar preguntas al importar el módulo
lista_preguntas = cargar_preguntas_desde_csv()

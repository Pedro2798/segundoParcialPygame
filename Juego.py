import pygame
from Constantes import *
from Preguntas import *
from Funciones import *

pygame.init()

pygame.display.set_caption("PREGUNTADOS")
icono = pygame.image.load("icono.png")
pygame.display.set_icon(icono)

pantalla = pygame.display.set_mode(PANTALLA)
datos_juego = {"puntuacion":0,"vidas":CANTIDAD_VIDAS,"nombre":"","tiempo_restante":30,"respuestas_correctas_seguidas":0}
fondo_pantalla = pygame.transform.scale(pygame.image.load("fondo.jpg"),PANTALLA)

#Elemento del juego
caja_pregunta = crear_elemento_juego("textura_pregunta.jpg",ANCHO_PREGUNTA,ALTO_PREGUNTA,(ANCHO-ANCHO_PREGUNTA)//2,80)
boton_respuesta_uno = crear_elemento_juego("textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON,(ANCHO-ANCHO_BOTON)//2,245)
boton_respuesta_dos = crear_elemento_juego("textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON,(ANCHO-ANCHO_BOTON)//2,345)
boton_respuesta_tres = crear_elemento_juego("textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON,(ANCHO-ANCHO_BOTON)//2,445)
boton_respuesta_cuatro = crear_elemento_juego("textura_respuesta.jpg",ANCHO_BOTON,ALTO_BOTON,(ANCHO-ANCHO_BOTON)//2,545)

# Comodines
comodines = crear_comodines()
# Agregar estado activo a los botones de respuesta
botones_respuesta = [boton_respuesta_uno, boton_respuesta_dos, boton_respuesta_tres, boton_respuesta_cuatro]
for boton in botones_respuesta:
    boton["activo"] = True

mezclar_lista(lista_preguntas)

corriendo = True
reloj = pygame.time.Clock()
evento_tiempo = pygame.USEREVENT
pygame.time.set_timer(evento_tiempo,1000)

def mostrar_juego(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    retorno = "juego"
    pregunta_actual = lista_preguntas[datos_juego['indice']]
    
    if datos_juego["vidas"] == 0 or datos_juego["tiempo_restante"] == 0:
        retorno = "terminado"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                # Verificar si se clickeó un comodín
                comodin_clickeado = verificar_click_comodin(comodines, evento.pos)
                if comodin_clickeado != -1:
                    # Aplicar comodín según el índice
                    if comodin_clickeado == 0:  # Bomba
                        if datos_juego.get("bomba_usado", False) == False:
                            aplicar_comodin_bomba(pregunta_actual, botones_respuesta)
                            datos_juego["bomba_usado"] = True
                            CLICK_SONIDO.play()
                    elif comodin_clickeado == 1:  # X2
                        if datos_juego.get("x2_usado", False) == False:
                            aplicar_comodin_x2(datos_juego)
                            datos_juego["x2_usado"] = True
                            CLICK_SONIDO.play()
                    elif comodin_clickeado == 2:  # Doble chance
                        if datos_juego.get("doble_chance_usado", False) == False:
                            aplicar_comodin_doble_chance(datos_juego)
                            datos_juego["doble_chance_usado"] = True
                            CLICK_SONIDO.play()
                    elif comodin_clickeado == 3:  # Pasar
                        if datos_juego.get("pasar_usado", False) == False:
                            aplicar_comodin_pasar(datos_juego)
                            datos_juego["pasar_usado"] = True
                            CLICK_SONIDO.play()
                            
                            # Avanzar automáticamente a la siguiente pregunta
                            datos_juego['indice'] += 1
                            if datos_juego['indice'] == len(lista_preguntas):
                                mezclar_lista(lista_preguntas)
                                datos_juego['indice'] = 0
                            
                            pregunta_actual = cambiar_pregunta(lista_preguntas,datos_juego['indice'],caja_pregunta,boton_respuesta_uno,boton_respuesta_dos,boton_respuesta_tres,boton_respuesta_cuatro)
                            # Reactivar todos los botones para la nueva pregunta
                            for boton in botones_respuesta:
                                boton["activo"] = True
                else:
                    # Verificar clicks en respuestas
                    respuesta = obtener_respuesta_click(boton_respuesta_uno,boton_respuesta_dos,boton_respuesta_tres,boton_respuesta_cuatro,evento.pos)
                    if respuesta != None:
                        # Verificar si el botón está activo (para comodín bomba)
                        if botones_respuesta[respuesta-1]["activo"]:
                            if verificar_respuesta(datos_juego,pregunta_actual,respuesta,lista_preguntas,datos_juego['indice']) == True:
                                CLICK_SONIDO.play()
                            else:
                                ERROR_SONIDO.play()
                            
                            datos_juego['indice'] += 1
                            if datos_juego['indice'] == len(lista_preguntas):
                                mezclar_lista(lista_preguntas)
                                datos_juego['indice'] = 0
                            
                            pregunta_actual = cambiar_pregunta(lista_preguntas,datos_juego['indice'],caja_pregunta,boton_respuesta_uno,boton_respuesta_dos,boton_respuesta_tres,boton_respuesta_cuatro)
                            # Reactivar todos los botones para la nueva pregunta
                            for boton in botones_respuesta:
                                boton["activo"] = True
                
        elif evento.type == evento_tiempo:
            datos_juego["tiempo_restante"] -= 1

    pantalla.blit(fondo_pantalla,(0,0))
    pantalla.blit(caja_pregunta["superficie"],caja_pregunta["rectangulo"])
    
    # Mostrar botones de respuesta solo si están activos
    for i, boton in enumerate(botones_respuesta):
        if boton["activo"]:
            pantalla.blit(boton["superficie"],boton["rectangulo"])
    
    # Mostrar comodines
    for i, comodin in enumerate(comodines):
        # Verificar si el comodín ya fue usado
        usado = False
        if i == 0 and datos_juego.get("bomba_usado", False):
            usado = True
        elif i == 1 and datos_juego.get("x2_usado", False):
            usado = True
        elif i == 2 and datos_juego.get("doble_chance_usado", False):
            usado = True
        elif i == 3 and datos_juego.get("pasar_usado", False):
            usado = True
        
        if not usado:
            # Fondo blanco para comodines
            pygame.draw.rect(pantalla, COLOR_BLANCO, comodin["rectangulo"])
            pygame.draw.rect(pantalla, COLOR_NEGRO, comodin["rectangulo"], 2)
            
            # Mostrar iconos usando imágenes
            if i == 0:  # Bomba
                try:
                    icono_bomba = pygame.image.load("bomba.png")
                    icono_bomba = pygame.transform.scale(icono_bomba, (35, 35))
                    pantalla.blit(icono_bomba, (comodin["rectangulo"].x + 12, comodin["rectangulo"].y + 12))
                except:
                    mostrar_texto(pantalla, "💣", (comodin["rectangulo"].x + 15, comodin["rectangulo"].y + 10), FUENTE_TEXTO, COLOR_NEGRO)
            elif i == 1:  # X2
                mostrar_texto(pantalla, "x2", (comodin["rectangulo"].x + 20, comodin["rectangulo"].y + 10), FUENTE_TEXTO, COLOR_NEGRO)
            elif i == 2:  # Doble chance (trébol)
                try:
                    icono_trebol = pygame.image.load("trebol.png")
                    icono_trebol = pygame.transform.scale(icono_trebol, (40, 40))
                    pantalla.blit(icono_trebol, (comodin["rectangulo"].x + 10, comodin["rectangulo"].y + 10))
                except:
                    mostrar_texto(pantalla, "🍀", (comodin["rectangulo"].x + 15, comodin["rectangulo"].y + 10), FUENTE_TEXTO, COLOR_VERDE)
            elif i == 3:  # Pasar (flecha)
                try:
                    icono_flecha = pygame.image.load("flecha.jpg")
                    icono_flecha = pygame.transform.scale(icono_flecha, (40, 40))
                    pantalla.blit(icono_flecha, (comodin["rectangulo"].x + 10, comodin["rectangulo"].y + 10))
                except:
                    mostrar_texto(pantalla, "➡️", (comodin["rectangulo"].x + 15, comodin["rectangulo"].y + 10), FUENTE_TEXTO, COLOR_ROJO)

    mostrar_texto(caja_pregunta["superficie"],pregunta_actual["pregunta"],(20,20),FUENTE_PREGUNTA,COLOR_NEGRO)
    mostrar_texto(boton_respuesta_uno["superficie"],pregunta_actual["respuesta_1"],(20,20),FUENTE_RESPUESTA,COLOR_BLANCO)
    mostrar_texto(boton_respuesta_dos["superficie"],pregunta_actual["respuesta_2"],(20,20),FUENTE_RESPUESTA,COLOR_BLANCO)
    mostrar_texto(boton_respuesta_tres["superficie"],pregunta_actual["respuesta_3"],(20,20),FUENTE_RESPUESTA,COLOR_BLANCO)
    mostrar_texto(boton_respuesta_cuatro["superficie"],pregunta_actual["respuesta_4"],(20,20),FUENTE_RESPUESTA,COLOR_BLANCO)
    
    mostrar_texto(pantalla,f"VIDAS: {datos_juego['vidas']}",(10,10),FUENTE_TEXTO)
    mostrar_texto(pantalla,f"PUNTUACION: {datos_juego['puntuacion']}",(10,40),FUENTE_TEXTO)
    mostrar_texto(pantalla,f"TIEMPO: {datos_juego['tiempo_restante']} s",(300,10),FUENTE_TEXTO)

    return retorno
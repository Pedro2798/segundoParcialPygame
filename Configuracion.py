import pygame
from Constantes import *
from Funciones import *

pygame.init()

# Elementos de la pantalla de configuración
boton_musica_on = crear_elemento_juego("textura_menu.jpg", 120, 60, (ANCHO-120)//2, 200)
boton_mas_volumen = crear_elemento_juego("mas.webp", 60, 60, (ANCHO-60)//2 + 100, 300)
boton_menos_volumen = crear_elemento_juego("menos.webp", 60, 60, (ANCHO-60)//2 - 100, 300)
boton_volver = crear_elemento_juego("btn_ajustes.jpg", 100, 40, (ANCHO-100)//2, 500)

def mostrar_ajustes(pantalla:pygame.Surface,cola_eventos:list[pygame.event.Event],datos_juego:dict) -> str:
    retorno = "ajustes"
    
    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            retorno = "salir"
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if boton_musica_on["rectangulo"].collidepoint(evento.pos):
                    # Alternar música on/off
                    datos_juego["musica_activa"] = not datos_juego.get("musica_activa", True)
                    CLICK_SONIDO.play()
                    
                    # Aplicar cambios inmediatamente
                    if datos_juego["musica_activa"]:
                        pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
                        if not pygame.mixer.music.get_busy():
                            try:
                                pygame.mixer.music.load("musica.mp3")
                                pygame.mixer.music.play(-1)
                            except:
                                pass  # Si no puede cargar la música, no hace nada
                    else:
                        pygame.mixer.music.stop()
                        
                elif boton_mas_volumen["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] < 100:
                        datos_juego["volumen_musica"] += 10
                        CLICK_SONIDO.play()
                        # Aplicar volumen inmediatamente si la música está activa
                        if datos_juego.get("musica_activa", True):
                            pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
                    else:
                        ERROR_SONIDO.play()
                        
                elif boton_menos_volumen["rectangulo"].collidepoint(evento.pos):
                    if datos_juego["volumen_musica"] > 0:
                        datos_juego["volumen_musica"] -= 10
                        CLICK_SONIDO.play()
                        # Aplicar volumen inmediatamente si la música está activa
                        if datos_juego.get("musica_activa", True):
                            pygame.mixer.music.set_volume(datos_juego["volumen_musica"] / 100)
                    else:
                        ERROR_SONIDO.play()
                        
                elif boton_volver["rectangulo"].collidepoint(evento.pos):
                    CLICK_SONIDO.play()
                    retorno = "menu"
    
    # Dibujar pantalla con fondo personalizado
    try:
        fondo_ajustes = pygame.transform.scale(pygame.image.load("textura_ajustes.jpg"), PANTALLA)
        pantalla.blit(fondo_ajustes, (0, 0))
    except:
        pantalla.fill(COLOR_BLANCO)
    
    # Título
    mostrar_texto(pantalla, "CONFIGURACIÓN", (ANCHO//2 - 115, 80), FUENTE_PREGUNTA, COLOR_NEGRO)
    
    # Sección de música
    mostrar_texto(pantalla, "MÚSICA", (ANCHO//2 - 40, 150), FUENTE_TEXTO, COLOR_NEGRO)
    
    # Botón música on/off - crear superficie nueva cada vez para evitar superposición
    boton_musica_superficie = pygame.transform.scale(pygame.image.load("btn_ajustes.jpg"), (120, 60))
    pantalla.blit(boton_musica_superficie, boton_musica_on["rectangulo"])
    estado_musica = "ON" if datos_juego.get("musica_activa", True) else "OFF"
    # Renderizar texto directamente en la pantalla
    texto_superficie = FUENTE_TEXTO.render(estado_musica, True, COLOR_NEGRO)
    texto_rect = texto_superficie.get_rect(center=boton_musica_on["rectangulo"].center)
    pantalla.blit(texto_superficie, texto_rect)
    
    # Controles de volumen
    mostrar_texto(pantalla, "VOLUMEN", (ANCHO//2 - 60, 270), FUENTE_TEXTO, COLOR_NEGRO)
    
    # Botones de volumen con iconos
    pantalla.blit(boton_menos_volumen["superficie"], boton_menos_volumen["rectangulo"])
    pantalla.blit(boton_mas_volumen["superficie"], boton_mas_volumen["rectangulo"])
    
    # Mostrar porcentaje de volumen
    mostrar_texto(pantalla, f"{datos_juego['volumen_musica']}%", (ANCHO//2 - 60, 360), FUENTE_VOLUMEN, COLOR_NEGRO)
    
    # Barra de volumen visual
    barra_ancho = 200
    barra_alto = 20
    barra_x = (ANCHO - barra_ancho) // 2
    barra_y = 420
    
    # Fondo de la barra
    pygame.draw.rect(pantalla, COLOR_NEGRO, (barra_x, barra_y, barra_ancho, barra_alto), 2)
    # Llenado de la barra según el volumen
    llenado_ancho = int((datos_juego['volumen_musica'] / 100) * (barra_ancho - 4))
    pygame.draw.rect(pantalla, COLOR_VERDE, (barra_x + 2, barra_y + 2, llenado_ancho, barra_alto - 4))
    
    # Botón volver
    boton_volver_superficie = pygame.transform.scale(pygame.image.load("btn_ajustes.jpg"), (100, 40))
    pantalla.blit(boton_volver_superficie, boton_volver["rectangulo"])
    # Renderizar texto directamente en la pantalla
    texto_volver_superficie = FUENTE_TEXTO.render("VOLVER", True, COLOR_NEGRO)
    texto_volver_rect = texto_volver_superficie.get_rect(center=boton_volver["rectangulo"].center)
    pantalla.blit(texto_volver_superficie, texto_volver_rect)

    return retorno
    
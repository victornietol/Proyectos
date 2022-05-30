import re, random, requests
import tkinter
import tkinter as tk
from tkinter import LEFT, PhotoImage, Toplevel, ttk
from tkinter import messagebox  as mb
from unicodedata import normalize
from datetime import datetime
from PIL import Image, ImageTk

class Chatbot:
    def __init__(self):
        self.aux_categorizacion = False
        self.aux_catego_series = False
        self.aux_catego_accion = False
        self.aux_catego_comedia = False   
        self.aux_catego_terror = False 
        self.aux_catego_deporte = False  
        self.aux_catego_animacion = False
        self.aux_catego_docu = False
        self.aux_recomendaciones = False
        self.aux_obtener_info = False
        self.aux_final = False
        self.aux_dialogo_continuo_bot = False
        self.aux_resultado_recom = False
        self.aux_clima = False
        self.aux_cat_principal = False
        self.aux_memoria_cantidad = False
        self.aux_existe_dialogo_bot = False
        self.memoria_cantidad = ''
        self.pregunta_aux = ''
        self.memoria_pel = ''
        self.memoria_temporal = ''

        self.info()
        self.interfaz()

    def info(self):
        self.grafo = {}
        self.grafo['recomendaciones']=['netflix','HBO max','disney+','spotify','youtube']

        # saludos
        self.grafo['saludo']=[f'¿Qué tal?, la temperatura de hoy es de {self.temperatura()}','Hola, hoy siento que tengo poca bateria',
                                    f'{self.saludo_hora().capitalize()}, estoy listo para mostrarte algunas recomendaciones',
                                    f'¿Qué tal?, la fecha de hoy es {(self.fecha_actual())}']
        
        # nefltix
        self.grafo['netflix']=['películas','series','documentales']
        self.grafo['pel_cat_netflix']=['acción','comedia','terror','deporte','animación']
        self.grafo['accion_netflix']=['the adam project','la vieja guardia','el ejército de los ladrones','john wick 3','misión de rescate']
        self.grafo['comedia_netflix']=['volver al futuro 3','paul','super cool','un espía y medio','alerta roja']
        self.grafo['terror_netflix']=['nadie sale con vida','la bruja','eli','las formas antiguas','el rito']
        self.grafo['deporte_netflix']=['rush','jugar en casa','83','la verdad oculta', 'novato']
        self.grafo['animacion_netflix']=['spider man: un nuevo universo','sonic','vivo','shrek','como entrenar a tu dragon 2']
        self.grafo['series_netflix']=['peaky blinders','better call saul','breaking bad','ozark','the witcher'] 
        self.grafo['docu_netflix']=['el último baile','what the health','the toys that made us','making a murderer','ícaro'] 

        # hbo max
        self.grafo['hbo']=['películas','series','documentales'] 
        self.grafo['pel_cat_hbo']=['acción','comedia','terror','deporte','animación']
        self.grafo['accion_hbo']=['batman','ready player one','matrix resurrections','parque jurásico','los juegos del hambre']
        self.grafo['comedia_hbo']=['una pareja explosiva','30 minutos o menos','amigos de armas','guerra de papás']
        self.grafo['terror_hbo']=['la huérfana','no respires 2','saw','la bruja de blair','insidious']
        self.grafo['deporte_hbo']=['rey richard','invictus','american underdog','el juego de la fortuna']
        self.grafo['animacion_hbo']=['space jam','la gran aventura lego','stuart little','el cadáver de la novia']
        self.grafo['series_hbo']=['the big bang theory','game of thrones','friends','rick and morty','the mentalist']
        self.grafo['docu_hbo']=['cuidado con slenderman','mcmillions','the inventor','a la caza de Bin Laden','asesinas']

        # disney+
        self.grafo['disney+']=['películas','series']
        self.grafo['cat_disney']=['pixar','marvel','star wars','disney']
        self.grafo['disney']=['frozen 2','dinosaurio','el libro de la selva','tarzán','zootopía']
        self.grafo['pixar']=['los increibles','red','coco','toy story','cars']
        self.grafo['marvel']=['iron man','capitan america y el soldado del invierno','avengers endgame','thor ragnarok','guardianes de la galaxia']
        self.grafo['starwars']=['rogue one','han solo','una nueva esperanza','el imperio contrataca','el regreso del jedi']
        self.grafo['series_disney']=['hawkeye','moon knight','el libro de boba fett','the mandalorian','loki','what if?...','malcolm','wandavision']

        # spotify
        self.grafo['spotify']=['canciones','podcasts']
        self.grafo['canciones']= ['top 10 global','top 10 méxico','entrenamiento','pop','urbano','romance','cumbia','salsa', 
                                            'rock','hip hop','electronica','jazz','clásica']
        self.grafo['top_global']='canciones/spotify/top_global.txt'
        self.grafo['top_mex']='canciones/spotify/top_mex.txt'
        self.grafo['entrenamiento']='canciones/spotify/entre.txt'
        self.grafo['pop']='canciones/spotify/pop.txt'
        self.grafo['urbano']='canciones/spotify/urbano.txt'
        self.grafo['romance']='canciones/spotify/romance.txt'
        self.grafo['cumbia']='canciones/spotify/cumbia.txt'
        self.grafo['salsa']='canciones/spotify/salsa.txt'
        self.grafo['rock']='canciones/spotify/rock.txt'
        self.grafo['hiphop']='canciones/spotify/hiphop.txt'
        self.grafo['electronica']='canciones/spotify/electronica.txt'
        self.grafo['jazz']='canciones/spotify/jazz.txt'
        self.grafo['clasica']='canciones/spotify/clasica.txt'
        self.grafo['podcasts']=['PARANORMAL','CREATIVO','Asesinos Seriales','La Cotorrisa','Historia para Tontod Podcast','TED Talks Daily',
                                'Gusgri Podcast','Relatos de la Noche','Leyendas Legendarias','Se Regalan Dudas']

        # youtube
        self.grafo['youtube']=['mascotas','videojuegos','cocina','niños','tecnología','autos']
        self.grafo['mascotas']=['Adiestramiento Canino con EricEnPositivo','ADIESTRAMIENTO CANINE-SERVICE','José Luis MartGon','Más que un amigo','Jose Arca','Cesar Millan']
        self.grafo['videojuegos']=['Censored Gaming','98DEMAKE','The Retro Future','Vandal','Eurogamerspain','Zico Tops']
        self.grafo['cocina']=['Mis pastelitos','La capital','Jauja Cocina Mexicana','De mi Rancho a Tu Cocina','Cocina Para Todos','Kiwlimón','Cocina Vegan fácil','Mi Cocina Rápida - Karen',]
        self.grafo['niños']=['toycantando','lunacreciente','Doctor Beet','Super Simple Songs','El Mundo de Luna','Cuentos Infantiles','Telmo y Tula','The Artful Parent']
        self.grafo['tecnologia']=['Isa Marcial','Nate Gentile','Verownika','Tecnonauta','La red de Mario','Mazthertutoriales','jose Tecnofanatico','GioCode']
        self.grafo['autos']=['Darius Motors','vicesat','Tuner Garage','El Dios de los Autos INMORTAL','FERCHO URQUIZA','MatiasAntico','Alfredo Valenzuela']

        # sinopsis
        self.grafo['sinopsis']= { 'the adam project':(open('sinopsis/proy_adam.txt', encoding='utf-8').read()), 
                                    'la vieja guardia':(open('sinopsis/viejag.txt', encoding='utf-8').read()), 
                                    'el ejercito de los ladrones':(open('sinopsis/ejercito_lad.txt', encoding='utf-8').read()), 
                                    'john wick 3':(open('sinopsis/jw3.txt', encoding='utf-8').read()), 
                                    'mision de rescate':(open('sinopsis/mision_r.txt', encoding='utf-8').read()), 
                                    'volver al futuro 3':(open('sinopsis/volver_f3.txt', encoding='utf-8').read()), 
                                    'paul':(open('sinopsis/paul.txt', encoding='utf-8').read()), 
                                    'super cool':(open('sinopsis/super_c.txt', encoding='utf-8').read()), 
                                    'espia y medio':(open('sinopsis/espia_med.txt', encoding='utf-8').read()), 
                                    'alerta roja':(open('sinopsis/alerta_r.txt', encoding='utf-8').read()), 
                                    'nadie sale con vida':(open('sinopsis/nadie_sv.txt', encoding='utf-8').read()), 
                                    'la bruja':(open('sinopsis/bruja.txt', encoding='utf-8').read()), 
                                    'eli':(open('sinopsis/eli.txt', encoding='utf-8').read()), 
                                    'las formas antiguas':(open('sinopsis/formas_ant.txt', encoding='utf-8').read()), 
                                    'el rito':(open('sinopsis/rito.txt', encoding='utf-8').read()),
                                    'rush':(open('sinopsis/rush.txt', encoding='utf-8').read()),
                                    'jugar en casa':(open('sinopsis/jugar_casa.txt', encoding='utf-8').read()),
                                    '83':(open('sinopsis/83.txt', encoding='utf-8').read()),
                                    'la verdad oculta':(open('sinopsis/verdad_oculta.txt', encoding='utf-8').read()),
                                    'novato':(open('sinopsis/novato.txt', encoding='utf-8').read()),
                                    'spider man':(open('sinopsis/spiderman.txt', encoding='utf-8').read()),
                                    'sonic':(open('sinopsis/sonic.txt', encoding='utf-8').read()),
                                    'vivo':(open('sinopsis/vivo.txt', encoding='utf-8').read()),
                                    'shrek':(open('sinopsis/shrek.txt', encoding='utf-8').read()),
                                    'entrenar a tu dragon':(open('sinopsis/entrenar_dragon.txt', encoding='utf-8').read()),
                                    'peaky blinders':(open('sinopsis/p_blinders.txt', encoding='utf-8').read()),
                                    'better call saul':(open('sinopsis/better_c_s.txt', encoding='utf-8').read()),
                                    'breaking bad':(open('sinopsis/breaking_bad.txt', encoding='utf-8').read()),
                                    'ozark':(open('sinopsis/ozark.txt', encoding='utf-8').read()),
                                    'witcher':(open('sinopsis/witcher.txt', encoding='utf-8').read()),
                                    'el ultimo baile':(open('sinopsis/ultimo_baile.txt', encoding='utf-8').read()),
                                    'what the health':(open('sinopsis/what_health.txt', encoding='utf-8').read()),
                                    'toys that made':(open('sinopsis/the_toys.txt', encoding='utf-8').read()),
                                    'making a murderer':(open('sinopsis/making_murderer.txt', encoding='utf-8').read()),
                                    'icaro':(open('sinopsis/icaro.txt', encoding='utf-8').read()),
                                    'batman':(open('sinopsis/batman.txt', encoding='utf-8').read()),
                                    'ready player one':(open('sinopsis/r_player_o.txt', encoding='utf-8').read()),
                                    'matrix':(open('sinopsis/matrix.txt', encoding='utf-8').read()),
                                    'parque jurasico':(open('sinopsis/parque_j.txt', encoding='utf-8').read()),
                                    'juegos del hambre':(open('sinopsis/juegos_hambre.txt', encoding='utf-8').read()),
                                    'pareja explosiva':(open('sinopsis/pareja_exp.txt', encoding='utf-8').read()),
                                    '30 minutos':(open('sinopsis/30_minutos.txt', encoding='utf-8').read()),
                                    'amigos de armas':(open('sinopsis/amigos_armas.txt', encoding='utf-8').read()),
                                    'guerra de papas':(open('sinopsis/guerra_papas.txt', encoding='utf-8').read()),
                                    'huerfana':(open('sinopsis/huerfana.txt', encoding='utf-8').read()),
                                    'no respires':(open('sinopsis/no_respires.txt', encoding='utf-8').read()),
                                    'saw':(open('sinopsis/saw.txt', encoding='utf-8').read()),
                                    'bruja de blair':(open('sinopsis/bruja_blair.txt', encoding='utf-8').read()),
                                    'insidious':(open('sinopsis/insidious.txt', encoding='utf-8').read()),
                                    'rey richard':(open('sinopsis/r_richard.txt', encoding='utf-8').read()),
                                    'invictus':(open('sinopsis/invictus.txt', encoding='utf-8').read()),
                                    'american underdog':(open('sinopsis/underdog.txt', encoding='utf-8').read()),
                                    'el juego de la fortuna':(open('sinopsis/fortuna_juego.txt', encoding='utf-8').read()),
                                    'space jam':(open('sinopsis/space_jam.txt', encoding='utf-8').read()),
                                    'gran aventura lego':(open('sinopsis/lego.txt', encoding='utf-8').read()),
                                    'stuart little':(open('sinopsis/stuart_l.txt', encoding='utf-8').read()),
                                    'cadaver de la novia':(open('sinopsis/cad_novia.txt', encoding='utf-8').read()),
                                    'big bang theory':(open('sinopsis/big_bt.txt', encoding='utf-8').read()),
                                    'game of thrones':(open('sinopsis/game_t.txt', encoding='utf-8').read()),
                                    'friends':(open('sinopsis/friends.txt', encoding='utf-8').read()),
                                    'rick and morty':(open('sinopsis/rick_morty.txt', encoding='utf-8').read()),
                                    'mentalist':(open('sinopsis/mentalist.txt', encoding='utf-8').read()),
                                    'cuidado con slenderman':(open('sinopsis/slenderman.txt', encoding='utf-8').read()),
                                    'mcmillions':(open('sinopsis/mcmillions.txt', encoding='utf-8').read()),
                                    'the inventor':(open('sinopsis/inventor.txt', encoding='utf-8').read()),
                                    'caza de bin laden':(open('sinopsis/bin_laden.txt', encoding='utf-8').read()),
                                    'asesinas':(open('sinopsis/asesinas.txt', encoding='utf-8').read()),
                                    'frozen 2':(open('sinopsis/frozen2.txt', encoding='utf-8').read()),
                                    'dinosaurio':(open('sinopsis/dinosaurio.txt', encoding='utf-8').read()),
                                    'libro de la selva':(open('sinopsis/libro_selva.txt', encoding='utf-8').read()),
                                    'tarzan':(open('sinopsis/tarzan.txt', encoding='utf-8').read()),
                                    'zootopia':(open('sinopsis/zootopia.txt', encoding='utf-8').read()),
                                    'los increibles':(open('sinopsis/increibles.txt', encoding='utf-8').read()),
                                    'red':(open('sinopsis/red.txt', encoding='utf-8').read()),
                                    'coco':(open('sinopsis/coco.txt', encoding='utf-8').read()),
                                    'toy story':(open('sinopsis/toy_story.txt', encoding='utf-8').read()),
                                    'cars':(open('sinopsis/cars.txt', encoding='utf-8').read()),
                                    'rogue one':(open('sinopsis/rogue_one.txt', encoding='utf-8').read()),
                                    'han solo':(open('sinopsis/han_solo.txt', encoding='utf-8').read()),
                                    'una nueva esperanza':(open('sinopsis/n_esperanza.txt', encoding='utf-8').read()),
                                    'imperio contrataca':(open('sinopsis/imp_cont.txt', encoding='utf-8').read()),
                                    'regreso del jedi':(open('sinopsis/reg_jedi.txt', encoding='utf-8').read()),
                                    'iron man':(open('sinopsis/ironman.txt', encoding='utf-8').read()),
                                    'capitan america':(open('sinopsis/capitan_a.txt', encoding='utf-8').read()),
                                    'avengers endgame':(open('sinopsis/a_endgame.txt', encoding='utf-8').read()),
                                    'thor ragnarok':(open('sinopsis/thor.txt', encoding='utf-8').read()),
                                    'guardianes de la galaxia':(open('sinopsis/guardianes_g.txt', encoding='utf-8').read()),
                                    'hawkeye':(open('sinopsis/hawkeye.txt', encoding='utf-8').read()),
                                    'moon knight':(open('sinopsis/moonknight.txt', encoding='utf-8').read()),
                                    'libro de boba fett':(open('sinopsis/boba_fett.txt', encoding='utf-8').read()),
                                    'mandalorian':(open('sinopsis/mandalorian.txt', encoding='utf-8').read()),
                                    'loki':(open('sinopsis/loki.txt', encoding='utf-8').read()),
                                    'what if':(open('sinopsis/what_if.txt', encoding='utf-8').read()),
                                    'malcolm':(open('sinopsis/malcolm.txt', encoding='utf-8').read()),
                                    'wandavision':(open('sinopsis/wandavision.txt', encoding='utf-8').read())
                                }

        # informacion
        self.grafo['info']= { 'netflix':(open('informacion/netflix.txt', encoding='utf-8').read()),
                                'hbo':(open('informacion/hbo.txt', encoding='utf-8').read()),
                                'disney+':(open('informacion/disney.txt', encoding='utf-8').read()),
                                'spotify':(open('informacion/spotify.txt', encoding='utf-8').read()),
                                'youtube':(open('informacion/youtube.txt', encoding='utf-8').read())
                            }

        # datos curiosos
        self.grafo['curiosos'] = 'informacion/curiosos.txt'

        # agradecimiento
        self.grafo['agradecimiento'] = ['De nada','No hay de qué','No es nada','No te preocupes','Está bien',
                                            'Sin problema','Un placer','Estoy para servirle','Las que te ardornan']

        # despedida
        self.grafo['despedida'] = ['Hasta luego :)','Vuelve pronto :)','Nos vemos :)','¡Chao! :)','Hasta pronto :)',
                                        'Saludame a tu mamá :)','Adios :)']

        # variables adicionales
        self.dialogo = 'Chatbot:'
        self.vertices = list(self.grafo.keys())
        self.vertices_sinopsis = list(self.grafo['sinopsis'].keys())
        self.vertices_informacion = list(self.grafo['info'].keys())
        self.vertices_spotify = ['top_global','top_mex','entrenamiento','pop','urbano','romance','cumbia',
                                    'salsa','rock','hiphop','electronica','jazz','clasica']
        self.categorias_principales = ['recomendaciones','netflix','pel_cat_netflix','hbo','pel_cat_hbo','disney+',
                                            'cat_disney','spotify','canciones','youtube']                            

    def quitar_acentos(self,x):
        x = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", x), 0, re.I)
        x = normalize('NFC',x)
        return x

    def clasificacion_pregunta(self,x):
        if ('todas'in x):
            self.memoria_cantidad = 'todas'
        if ('una' in x): 
            if (('una pareja explosiva' in x) == False) and (('una nueva esperanza' in x) == False):
                self.memoria_cantidad = 'una'
            else:
                pass
        if ('dato curioso' in x):
            x = 'curiosos'
        if (('esta' in x) and ('clima' in x)) or ('clima' in x) or ('temperatura' in x):
            self.insertar_texto(f'{self.dialogo} Ingresa la ciudad por favor.')
            self.aux = True
            self.aux_clima = True
        elif ('sinopsis' in x) or ('que trata' in x) or ('resumen' in x):
            self.pelicula = x
            x = 'sinopsis'           
        elif ('fecha' in x) or (('dia' in x) and ('es' in x)):
            x = 'fecha'
        elif ('hora' in x) or (('hora' in x) and ('cual' in x)):
            self.aux_hora = True
            x = 'hora'        
        elif (('que es' in x) and ('netflix' in x)) or \
            (('que es' in x) and ('spotify' in x)) or \
            (('que es' in x) and ('hbo' in x)) or \
            (('que es' in x) and ('disney+' in x)) or\
            (('que es' in x) and ('youtube' in x)) or ('informacion' in x):
            self.informacion = x
            x = 'info'        
        elif (('peliculas' in x) and ('netflix' in x)) or \
            (('recomendaciones' in x) and ('peliculas' in x) and ('netflix' in x)):
            x = 'pel_cat_netflix'
            self.pregunta_aux = 'netflix'
            self.aux_dialogo_continuo_bot = True
            self.insertar_texto(f'{self.dialogo} En Netflix tengo recomendaciones de peliculas de ')
            self.aux_existe_dialogo_bot = True
        elif (('peliculas' in x) and ('hbo' in x)) or \
            (('recomendaciones' in x) and ('peliculas' in x) and ('hbo' in x)):
            x = 'pel_cat_hbo'
            self.pregunta_aux = 'hbo'
            self.aux_dialogo_continuo_bot = True
            self.insertar_texto(f'{self.dialogo} En HBO tengo recomendaciones de peliculas de ')
            self.aux_existe_dialogo_bot = True            
        elif (('peliculas' in x) and ('disney+' in x)) or \
            (('recomendaciones' in x) and ('peliculas' in x) and ('disney+' in x)):
            x = 'cat_disney'
            self.pregunta_aux = 'disney+'
            self.aux_dialogo_continuo_bot = True
            self.insertar_texto(f'{self.dialogo} En Disney+ tengo recomendaciones de peliculas de ')
            self.aux_existe_dialogo_bot = True            
        elif (('series' in x) and ('disney' in x)) or \
            (('recomendaciones' in x) and ('series' in x) and ('disney' in x)):
            x = 'series_disney'
            self.pregunta_aux = 'disney+'
        elif (('series' in x) and ('netflix' in x)) or \
            (('recomendaciones' in x) and ('series' in x) and ('netflix' in x)):
            x = 'series_netflix'
            self.pregunta_aux = 'netflix' 
        elif (('series' in x) and ('hbo' in x)) or \
            (('recomendaciones' in x) and ('series' in x) and ('hbo' in x)):
            x = 'series_hbo'
            self.pregunta_aux = 'hbo'
        elif (('documentales' in x) and ('netflix' in x)) or \
            (('recomendaciones' in x) and ('documentales' in x) and ('netflix' in x)):
            x = 'docu_netflix'
            self.pregunta_aux = 'netflix' 
        elif (('documentales' in x) and ('hbo' in x)) or \
            (('recomendaciones' in x) and ('documentales' in x) and ('hbo' in x)):
            x = 'docu_hbo'
            self.pregunta_aux = 'hbo' 
        elif (('netflix' in x) and ('recomendaciones' in x)) or ('netflix' in x):
            x = 'netflix'
            self.pregunta_aux = 'netflix'
        elif (('spotify' in x) and ('recomendaciones' in x)) or ('spotify' in x):
            x = 'spotify'
            self.pregunta_aux = 'spotify'
        elif (('hbo' in x) and ('recomendaciones' in x)) or ('hbo' in x):
            x = 'hbo'
            self.pregunta_aux = 'hbo'
        elif (('disney+' in x) and ('recomendaciones' in x)) or ('disney+' in x):
            x = 'disney+'
            self.pregunta_aux = 'disney+'
        elif (('youtube' in x) and ('recomendaciones' in x)) or ( 'youtube' in x):
            x = 'youtube'
            self.pregunta_aux = 'youtube'
        elif (('recomendaciones' in x) and ('series' in x)) or ('series' in x):         # comprobando si son series
            if self.pregunta_aux == 'netflix':
                x = 'series_netflix'
            elif self.pregunta_aux == 'hbo':
                x = 'series_hbo'
            elif self.pregunta_aux == 'disney+':
               x = 'series_disney'
            elif self.pregunta_aux == '':       # si es la primera vez que se busca serie
                self.insertar_texto(f'{self.dialogo} Puedo darte recomendaciones de series en plataformas como Netflix, HBO Max y Disney+,'
                +' ¿Qué prefieres?')
                self.aux = True
                self.aux_catego_series = True                                               
        elif (('peliculas' in x) and ('accion' in x)) or ('accion' in x):    # valorando categorias de peliculas
            if self.pregunta_aux == 'netflix':
                x = 'accion_netflix'
            elif self.pregunta_aux == 'hbo':
                x = 'accion_hbo'
            elif self.pregunta_aux == '':
                self.insertar_texto(f'{self.dialogo} Puedo mostrarte peliculas de acción en Netflix y HBO Max, ¿Cuál prefieres?.')
                self.aux = True
                self.aux_catego_accion = True
        elif (('peliculas' in x) and ('comedia' in x)) or ('comedia' in x):
            if self.pregunta_aux == 'netflix':
                x = 'comedia_netflix'
            elif self.pregunta_aux == 'hbo':
                x = 'comedia_hbo'
            elif self.pregunta_aux == '':
                self.insertar_texto(f'{self.dialogo} Puedo mostrarte peliculas de comedia en Netflix y HBO Max, ¿Cuál prefieres?.')
                self.aux = True
                self.aux_catego_comedia = True
        elif (('peliculas' in x) and ('terror' in x)) or ('terror' in x):
            if self.pregunta_aux == 'netflix':
                x = 'terror_netflix'
            elif self.pregunta_aux == 'hbo':
                x = 'terror_hbo'
            elif self.pregunta_aux == '':
                self.insertar_texto(f'{self.dialogo} Puedo mostrarte peliculas de terror en Netflix y HBO Max, ¿Cuál prefieres?.')
                self.aux = True
                self.aux_catego_terror = True            
        elif (('peliculas' in x) and ('deporte' in x)) or ('deporte' in x):
            if self.pregunta_aux == 'netflix':
                x = 'deporte_netflix'
            elif self.pregunta_aux == 'hbo':
                x = 'deporte_hbo'
            elif self.pregunta_aux == '':
                self.insertar_texto(f'{self.dialogo} Puedo mostrarte peliculas de deporte en Netflix y HBO Max, ¿Cuál prefieres?.')
                self.aux = True
                self.aux_catego_deporte = True
        elif (('peliculas' in x) and ('animacion' in x)) or ('animacion' in x):
            if self.pregunta_aux == 'netflix':
                x = 'animacion_netflix'
            elif self.pregunta_aux == 'hbo':
                x = 'animacion_hbo'
            elif self.pregunta_aux == '':
                self.insertar_texto(f'{self.dialogo} Puedo mostrarte peliculas de animadas en Netflix y HBO Max, ¿Cuál prefieres?.')
                self.aux = True
                self.aux_catego_animacion = True            
        elif (('peliculas' in x) and ('pixar' in x)) or ('pixar' in x):
            x = 'pixar'
        elif (('peliculas' in x) and ('marvel' in x)) or ('marvel' in x):
            x = 'marvel'
        elif (('peliculas' in x) and ('star wars' in x)) or ('star wars' in x):
            x = 'starwars'
        elif (('peliculas' in x) and ('disney' in x)) or ('disney' in x):
            x = 'disney'
        elif (('recomendaciones' in x) and ('peliculas' in x)) or ('peliculas' in x)\
            or ('pelicula' in x):  # comprobando si son peliculas
            if self.pregunta_aux == 'netflix':
                x = 'pel_cat_netflix'
            elif self.pregunta_aux == 'hbo':
                x = 'pel_cat_hbo'
            elif self.pregunta_aux == 'disney+':
                x = 'cat_disney'
            elif self.pregunta_aux == '':       # si es la primera vez que se busca pelicula
                self.insertar_texto(f'{self.dialogo} Puedo darte recomendaciones de peliculas en plataformas como Netflix, HBO Max y Disney+,'
                +' ¿Qué prefieres?')
                self.aux = True
                self.aux_categorizacion = True     
        elif (('recomendaciones' in x) and ('documentales' in x)) or ('documentales' in x):     # comprobando si son documentales
            if self.pregunta_aux == 'netflix':
                x = 'docu_netflix'
            elif self.pregunta_aux == 'hbo':
                x = 'docu_hbo'
            elif self.pregunta_aux == '':
                self.insertar_texto(f'{self.dialogo} Puedo mostrarte documentales en Netflix y HBO Max, ¿Cuál prefieres?.')
                self.aux = True
                self.aux_catego_docu = True 
        elif (('canciones' in x) and ('top 10 global' in x)) or ('top 10 global' in x):
            x = 'top_global'
        elif (('canciones' in x) and ('top 10 mexico' in x)) or ('top 10 mexico' in x):
            x = 'top_mex'
        elif (('canciones' in x) and ('entrenamiento' in x)) or ('entrenamiento' in x):
            x = 'entrenamiento'
        elif (('canciones' in x) and ('pop' in x)) or ('pop' in x):
            x = 'pop'
        elif (('canciones' in x) and ('urbano' in x)) or ('urbano' in x):
            x = 'urbano'
        elif (('canciones' in x) and ('romance' in x)) or ('romance' in x):
            x = 'romance'
        elif (('canciones' in x) and ('cumbia' in x)) or ('cumbia' in x):
            x = 'cumbia'
        elif (('canciones' in x) and ('salsa' in x)) or ('salsa' in x):
            x = 'salsa'
        elif (('canciones' in x) and ('rock' in x)) or ('rock' in x):
            x = 'rock'
        elif (('canciones' in x) and ('hip hop' in x)) or ('hip hop' in x):
            x = 'hiphop'
        elif (('canciones' in x) and ('electronica' in x)) or ('electronica' in x):
            x = 'electronica'
        elif (('canciones' in x) and ('jazz' in x)) or ('jazz' in x):
            x = 'jazz'
        elif (('canciones' in x) and ('clasica' in x)) or ('clasica' in x):
            x = 'clasica'
        elif (('recomendaciones' in x) and ('canciones' in x)) or ('canciones' in x)\
            or (('cancion' in x)):
            x = 'canciones'
        elif (('recomendaciones' in x) and ('podcasts' in x)) or ('podcast' in x) or ('podcasts' in x):
            x = 'podcasts'
        elif (('canales' in x) and ('mascotas' in x)) or ('mascotas' in x):
            x = 'mascotas'
        elif (('canales' in x) and ('videojuegos' in x)) or ('videojuegos' in x):
            x = 'videojuegos'
        elif (('canales' in x) and ('cocina' in x)) or ('cocina' in x):
            x = 'cocina'
        elif (('canales' in x) and ('niños' in x)) or ('niños' in x):
            x = 'niños'
        elif (('canales' in x) and ('tecnologia' in x)) or ('tecnologia' in x):
            x = 'tecnologia'
        elif (('canales' in x) and ('autos' in x)) or ('autos' in x):
            x = 'autos'
        elif (('recomendaciones' in x) and ('youtube' in x)) or ('youtube' in x):
            x = 'youtube'
        elif ('recomendaciones' in x):
            x = 'recomendaciones'
            self.pregunta_aux = ''
        else:
            pass
        return x

    def mensaje_rec(self,preg):
        if preg.__contains__('recomendaciones') and preg.__contains__('netflix'):
            self.aux_dialogo_continuo_bot = True
            self.aux_existe_dialogo_bot = True
            self.insertar_texto(f'{self.dialogo} En Netflix tengo recomendaciones de')
        elif preg.__contains__('recomendaciones') and preg.__contains__('spotify'):
            self.aux_dialogo_continuo_bot = True
            self.aux_existe_dialogo_bot = True
            self.insertar_texto(f'{self.dialogo} En Spotify tengo recomendaciones de')
        elif preg.__contains__('recomendaciones') and preg.__contains__('hbo'):
            self.aux_dialogo_continuo_bot = True
            self.aux_existe_dialogo_bot = True
            self.insertar_texto(f'{self.dialogo} En HBO Max tengo recomendaciones de')
        elif preg.__contains__('recomendaciones') and preg.__contains__('disney+'):
            self.aux_dialogo_continuo_bot = True
            self.aux_existe_dialogo_bot = True
            self.insertar_texto(f'{self.dialogo} En Disney+ tengo recomendaciones de')
        elif preg.__contains__('recomendaciones') and preg.__contains__('youtube'):
            self.aux_dialogo_continuo_bot = True
            self.aux_existe_dialogo_bot = True
            self.insertar_texto(f'{self.dialogo} En Youtube tengo recomendaciones de canales '
                                    +'en categorias como')

    def mensaje_inic(self,preg):
        if preg.__contains__('adios') or preg.__contains__('hasta luego') or preg.__contains__('nos vemos'):
            preg = 'despedida'
            self.insertar_texto(f'{self.dialogo} {random.choice(self.grafo[preg])}')
            self.aux = True
        elif preg.__contains__('gracias'):
            preg = 'agradecimiento'
            self.insertar_texto(f'{self.dialogo} {random.choice(self.grafo[preg])}.')
            self.aux = True
        elif preg.__contains__('buenos dias') or preg.__contains__('hola') or preg.__contains__('como estas')\
            or preg.__contains__('que tal') or preg.__contains__('buenas tardes') or preg.__contains__('buenas noches'):
            preg = 'saludo'
            self.insertar_texto(f'{self.dialogo} {random.choice(self.grafo[preg])}.')
            self.aux2 = True
            self.aux_hora = False
        elif preg.__contains__('netflix') or preg.__contains__('hbo') or preg.__contains__('spotify') \
            or preg.__contains__('disney+') or preg.__contains__('youtube') or preg.__contains__('canciones')\
            or preg.__contains__('series') or preg.__contains__('documentales') or preg.__contains__('podcasts')\
            or preg.__contains__('mascotas') or preg.__contains__('videojuegos') or preg.__contains__('cocina')\
            or preg.__contains__('niños') or preg.__contains__('tecnologia') or preg.__contains__('autos')\
            or preg.__contains__('peliculas'):
            pass   
        elif preg.__contains__('recomendaciones'):                
            self.aux_dialogo_continuo_bot = True
            self.insertar_texto(f'{self.dialogo} Tengo recomendaciones en plataformas como ')

    def lectura_recomendaciones(self,preg):
        preg = self.verificar_cat_principales(preg)

        if (self.memoria_cantidad == '') and (self.aux_cat_principal == False):   # memoria de cantidad vacia
            self.insertar_texto(f'{self.dialogo} Antes de continuar, ¿Deseas que te muestre todas '
                                    +'mis recomendaciones o simplemente una?')
            self.aux_memoria_cantidad = True
            self.memoria_temporal = preg

        elif (self.memoria_cantidad == 'una') and (self.aux_cat_principal == False):   # mostrar una recomendacion al azar
            self.insertar_texto(f'{self.dialogo} Podrías echarle un vistazo a '
                                    +f'{(random.choice(self.grafo[preg])).title()}.')

        else:
            try:
                for i in self.grafo[preg]:      # entrando al grafo
                    if preg == 'recomendaciones':       # evaluando si solo se esta pidiendo que recomendaciones se tienen (netflix, spot,etc)
                        self.aux_recomendaciones = True
                        if self.grafo[preg][-1] == i:
                            self.insertar_texto(f'{i.title()}.\n\n')
                        else:
                            self.insertar_texto(f'{i.title()}, ')

                    elif (self.grafo[preg][0] == i) and (self.grafo[preg][-1] == i):    # si es opcion unica
                        self.insertar_texto(f'{self.dialogo} {i.title()}.')

                    elif self.grafo[preg][0] == i:                                          # si es la primera sugerencia
                        self.aux_dialogo_continuo_bot = True
                        if self.aux_existe_dialogo_bot == True:
                            self.insertar_texto(f' {i.title()}, ')
                        else:
                            self.insertar_texto(f'{self.dialogo} {i.title()}, ')
                        self.aux_existe_dialogo_bot = False
                        self.aux_dialogo_continuo_bot = False

                    elif (self.grafo[preg][0] != i) and (self.grafo[preg][-1] != i):    # si es la sugerencia de enmedio
                        self.aux_resultado_recom = True
                        self.insertar_texto(f'{i.title()}, ')

                    elif self.grafo[preg][-1] == i:                                         # si es la sugerencia del final
                        self.aux_resultado_recom = True
                        self.insertar_texto(f'{i.title()}.\n\n')
            except KeyError:                                                                    # si no encuentra el indice
                self.insertar_texto(f'{self.dialogo} Mmmmm... no entiendo lo que dijiste, intenta de nuevo.')       # si no encuentra el indice
        self.aux_cat_principal = False

    def lectura_canciones(self,preg):
        with open(self.grafo[preg], encoding='utf-8') as datos:
            canciones = []
            for linea in datos:
                canciones.append([(x) for x in linea.strip().split(';')])

        if self.memoria_cantidad == 'todas':
            self.aux_dialogo_continuo_bot = True
            self.insertar_texto(f'{self.dialogo} Tal vez podrías escuchar las siguientes canciones...\n')
            for cancion in canciones[0]:
                self.aux_existe_dialogo_bot = True
                if cancion != canciones[0][-1]:
                    self.insertar_texto(f'{cancion.title()};  ')
                else:
                    self.insertar_texto(f'{cancion.title()}\n\n')
            self.aux_existe_dialogo_bot = False
        else:
            self.insertar_texto(f'{self.dialogo} Tal vez podrías escuchar {random.choice(canciones[0])}.')

    def lectura_sinopsis(self,preg):
        encontrado = False
        for sinopsis in self.vertices_sinopsis:
            if self.pelicula.__contains__(sinopsis):
                encontrado = True
                if self.memoria_pel == sinopsis:
                    self.insertar_texto(f'{self.dialogo} Mmmmmm... lee un poco más arriba, esa sinopsis ya te la mostre ;)')                
                else:              #elif (self.memoria_pel == '') or (self.memoria_pel != sinopsis):   <=== otra forma mas larga     
                    self.insertar_texto(f'{self.dialogo} La sinopsis es la siguiente...\n{self.grafo[preg][sinopsis]}')
                    self.memoria_pel = sinopsis
            else:
                pass
        if encontrado == False:
            self.insertar_texto(f'{self.dialogo} Lo siento, esa película no esta dentro de mis'
                    +' recomendaciones. Intenta de nuevo.')

    def lectura_informacion(self,preg):
        encontrado = False
        for info in self.vertices_informacion:
            if self.informacion.__contains__(info):
                encontrado = True
                self.insertar_texto(f'{self.dialogo} Según mis datos {self.grafo[preg][info]}')
            else:
                pass
        if encontrado == False:
            self.insertar_texto(f'{self.dialogo} Lo siento, no cuento con información sobre ese tema.')

    def lectura_Dcuriosos(self,preg):
        with open(self.grafo[preg], encoding='utf-8') as datos:
            lista_datos = []
            for linea in datos:
                lista_datos.append([(x) for x in linea.strip().split(';')])
        
        self.insertar_texto(f'{self.dialogo} {random.choice(lista_datos[0])}')

    def procesar_envio(self,pregunta_):
        self.aux_recomendaciones = False
        self.aux = False
        self.aux2 = False
        pregunta = pregunta_.lower()
        pregunta = self.quitar_acentos(pregunta)

        if self.aux_memoria_cantidad:
            pregunta = self.set_memoria_cantidad(pregunta)

        if self.aux_categorizacion:                     # sub clasificaciones
            pregunta = self.sub_clasificacion_peliculas(pregunta)
        elif self.aux_catego_series:
            pregunta = self.sub_clasificacion_series(pregunta)
        elif self.aux_catego_accion:
            pregunta = self.sub_clasificacion_accion(pregunta)
        elif self.aux_catego_comedia:
            pregunta = self.sub_clasificacion_comedia(pregunta)
        elif self.aux_catego_terror:
            pregunta = self.sub_clasificacion_terror(pregunta)
        elif self.aux_catego_deporte:
            pregunta = self.sub_clasificacion_deporte(pregunta)
        elif self.aux_catego_animacion:
            pregunta = self.sub_clasificacion_animacion(pregunta)
        elif self.aux_catego_docu:
            pregunta = self.sub_clasificacion_docu(pregunta)
        elif self.aux_clima:
            self.clima_actual(pregunta)

        if (pregunta == None) or (self.aux_final == True):      # evalua si viene de una subclasificacion
            pass
        else:
            self.mensaje_inic(pregunta)
            self.mensaje_rec(pregunta)
            pregunta = self.clasificacion_pregunta(pregunta)

        if self.aux:    # evalua si es el final
            pass
        elif self.aux2:     # evalua si es el saludo 
            pass
        elif pregunta in self.vertices_spotify:
                self.lectura_canciones(pregunta)
        elif pregunta == 'sinopsis':
            self.lectura_sinopsis(pregunta)
        elif pregunta == 'fecha':
            self.insertar_texto(f'{self.dialogo} Hoy es {self.fecha_actual()}.')
        elif pregunta == 'hora':
            x = self.hora_actual()
            h = x[0]
            m = x[1]
            s = x[2]
            self.insertar_texto(f'{self.dialogo} Son las {h} horas, con {m} minutos y {s} segundos.')
        elif pregunta == 'info':
            self.lectura_informacion(pregunta)
        elif pregunta == 'curiosos':
            self.lectura_Dcuriosos(pregunta)
        else:
            self.lectura_recomendaciones(pregunta) 
        
        self.aux_final = False

    def recorrer(self):
        for v in self.vertices:
            self.insertar_texto(f'{v} ==> {self.grafo[v]}')

    def fecha_actual(self):
        hoy = datetime.now()
        meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre',
                    'octubre','noviembre','diciembre']
        dia = hoy.day
        mes = meses[hoy.month - 1]
        anio = hoy.year
        fecha = '{} de {} del {}'.format(dia,mes,anio)
        return fecha

    def clima_actual(self, ciudad):
        api_key = '6178f7e3724caaa34a0175e55cf22525'
        url = 'http://api.openweathermap.org/data/2.5/weather?'
        url_completo = url + 'appid=' + api_key + '&q=' + ciudad + '&units=metric'
        response = requests.get(url_completo)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            temp = y["temp"]
            humedad = y["humidity"]
            z = x["weather"]
            descripcion = z[0]["description"]
            self.insertar_texto(f'{self.dialogo} Un momento... Los datos obtenidos para {ciudad.title()} ' 
                    +f'son:\nTemperatura: {temp} °C\nDescripcion: {descripcion}\nHumedad: {humedad}%')
            self.aux_clima = False
            self.aux_final = True
            self.aux = True
        else:
            self.insertar_texto(f'{self.dialogo} No se encuentra la ciudad, intenta de nuevo.')
            self.aux = True

    def temperatura(self):
        api_key = '6178f7e3724caaa34a0175e55cf22525'
        url = 'http://api.openweathermap.org/data/2.5/weather?'
        ciudad = 'ciudad de mexico'
        url_completo = url + 'appid=' + api_key + '&q=' + ciudad + '&units=metric'
        response = requests.get(url_completo)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            temp = y["temp"]
            clima = f'{temp} °C'
            return clima
        else:
            self.insertar_texto(f'{self.dialogo} No se encuentra la ciudad.')                

    def hora_actual(self):
        if self.aux_hora == False:
            hora = datetime.now()
            x = '{}:{}'.format(hora.hour,hora.minute)
            return x
        else:
            hora = datetime.now()
            h = hora.hour
            m = hora.minute
            s = hora.second
            return h,m,s

    def saludo_hora(self):
        hora = datetime.now()
        if (hora.hour >= 0) and (hora.hour <= 5):
            x = 'buenos días... o mejor dicho, buenas madrugadas'
        elif hora.hour <= 12:
            x = 'buenos días'
        elif (hora.hour > 12) and (hora.hour <= 19):
            x = 'buenas tardes'
        else:
            x = 'buenas noches'
        return x

    def insertar_texto(self,texto):
        self.chat.configure(state='normal')
        if texto.__contains__('Chatbot'):
            if self.aux_dialogo_continuo_bot:
                self.chat.insert(tk.END,f'{texto}')
                self.aux_dialogo_continuo_bot = False
            else:    
                self.chat.insert(tk.END,f'{texto}\n\n')
        elif self.aux_recomendaciones == True:
            self.chat.insert(tk.END,f'{texto}')
            self.aux_recomendaciones = False
        elif self.aux_resultado_recom:
            self.chat.insert(tk.END, texto)
            self.aux_resultado_recom = False
        else:
            if self.aux_existe_dialogo_bot:
                self.chat.insert(tk.END,f'{texto}')
            else:
                self.chat.insert(tk.END,f'Tú: {texto}\n\n')
        self.chat.configure(state='disabled')
        self.chat.see(tk.END)

    def enviar(self):
        pregunta = self.captura_texto.get()
        self.insertar_texto(pregunta)
        self.procesar_envio(pregunta)
        self.captura_texto.set('')                                      # si no funciona entonces asignar una variable que reciba la info como self.aux_resultado            

    def sub_clasificacion_peliculas(self,preg):
        self.aux = False
        if preg.__contains__('netflix'):
            self.aux_dialogo_continuo_bot = True
            self.insertar_texto(f'{self.dialogo} En Netflix tengo recomendaciones de peliculas de ')
            self.aux_existe_dialogo_bot = True
            self.aux_final = True
            self.aux_categorizacion = False
            x = 'pel_cat_netflix'
            self.pregunta_aux = 'netflix' # 'pel_cat_netflix'
        elif preg.__contains__('hbo'):
            self.aux_dialogo_continuo_bot = True
            self.insertar_texto(f'{self.dialogo} En HBO tengo recomendaciones de peliculas de ')
            self.aux_existe_dialogo_bot = True
            self.aux_final = True
            self.aux_categorizacion = False
            x = 'pel_cat_hbo'
            self.pregunta_aux = 'hbo'  # 'pel_cat_hbo'
        elif preg.__contains__('disney+'):
            self.aux_dialogo_continuo_bot = True
            self.insertar_texto(f'{self.dialogo} En Disney+ tengo recomendaciones de peliculas de ')
            self.aux_existe_dialogo_bot = True
            self.aux_final = True
            self.aux_categorizacion = False
            x = 'cat_disney'
            self.pregunta_aux = 'disney+'  # 'cat_disney'
        elif preg.__contains__('salir') or preg.__contains__('sueltame') or preg.__contains__('olvidalo'):
            self.aux = True
            self.aux_categorizacion = False
            self.insertar_texto(f'{self.dialogo} Ok.')
            return None               
        else:
            self.insertar_texto(f'{self.dialogo} No entendí lo que dijiste, intenta de nuevo.')
            self.aux = True
            x = None
        return x     

    def sub_clasificacion_series(self,preg):
        self.aux = False
        if preg.__contains__('netflix'):
            self.insertar_texto(f'{self.dialogo} En Netflix podrías ver...') 
            self.aux_final = True           
            self.aux_catego_series = False
            x = 'series_netflix'
            self.pregunta_aux = 'netflix'
        elif preg.__contains__('hbo'):
            self.insertar_texto(f'{self.dialogo} En HBO Max podrías ver...')
            self.aux_final = True
            self.aux_catego_series = False
            x = 'series_hbo'
            self.pregunta_aux = 'hbo'
        elif preg.__contains__('disney+'):
            self.insertar_texto(f'{self.dialogo} En Disney+ podrías ver...')
            self.aux_final = True
            self.aux_catego_series = False
            x = 'series_disney'
            self.pregunta_aux = 'disney+' 
        elif preg.__contains__('salir') or preg.__contains__('sueltame') or preg.__contains__('olvidalo'):
            self.aux = True
            self.aux_catego_series = False
            self.insertar_texto(f'{self.dialogo} Ok.')
            return None             
        else:
            self.insertar_texto(f'{self.dialogo} No entendí lo que dijiste, intenta de nuevo.')
            self.aux = True
            x = None
        return x              

    def sub_clasificacion_accion(self,preg):
        self.aux = False
        if preg.__contains__('netflix'):
            self.insertar_texto(f'{self.dialogo} En Netflix podrías ver...')
            self.aux_final = True
            self.aux_catego_accion = False
            x = 'accion_netflix'
        elif preg.__contains__('hbo'):
            self.insertar_texto(f'{self.dialogo} En hbo podrías ver...')
            self.aux_final = True
            self.aux_catego_accion = False
            x = 'accion_hbo' 
        elif preg.__contains__('salir') or preg.__contains__('sueltame') or preg.__contains__('olvidalo'):
            self.aux = True
            self.aux_catego_accion = False
            self.insertar_texto(f'{self.dialogo} Ok.')
            return None             
        else:
            self.insertar_texto(f'{self.dialogo} No entendí lo que dijiste, intenta de nuevo.')
            self.aux = True
            x = None
        return x        

    def sub_clasificacion_comedia (self,preg):
        self.aux = False
        if preg.__contains__('netflix'):
            self.insertar_texto(f'{self.dialogo} En Netflix podrías ver...')
            self.aux_final = True
            self.aux_catego_comedia = False
            x = 'comedia_netflix'
        elif preg.__contains__('hbo'):
            self.insertar_texto(f'{self.dialogo} En hbo podrías ver...')
            self.aux_final = True
            self.aux_catego_comedia = False
            x = 'comedia_hbo' 
        elif preg.__contains__('salir') or preg.__contains__('sueltame') or preg.__contains__('olvidalo'):
            self.aux = True
            self.aux_catego_comedia = False
            self.insertar_texto(f'{self.dialogo} Ok.')
            return None             
        else:
            self.insertar_texto(f'{self.dialogo} No entendí lo que dijiste, intenta de nuevo.')
            self.aux = True
            x = None
        return x

    def sub_clasificacion_terror(self,preg):
        self.aux = False
        if preg.__contains__('netflix'):
            self.insertar_texto(f'{self.dialogo} En Netflix podrías ver...')
            self.aux_final = True
            self.aux_catego_terror = False
            x = 'terror_netflix'
        elif preg.__contains__('hbo'):
            self.insertar_texto(f'{self.dialogo} En hbo podrías ver...')
            self.aux_final = True
            self.aux_catego_terror = False
            x = 'terror_hbo'
        elif preg.__contains__('salir') or preg.__contains__('sueltame') or preg.__contains__('olvidalo'):
            self.aux = True
            self.aux_catego_terror = False
            self.insertar_texto(f'{self.dialogo} Ok.')
            return None              
        else:
            self.insertar_texto(f'{self.dialogo} No entendí lo que dijiste, intenta de nuevo.')
            self.aux = True
            x = None
        return x

    def sub_clasificacion_deporte(self,preg):
        self.aux = False
        if preg.__contains__('netflix'):
            self.insertar_texto(f'{self.dialogo} En Netflix podrías ver...')
            self.aux_final = True
            self.aux_catego_deporte = False
            x = 'deporte_netflix'
        elif preg.__contains__('hbo'):
            self.insertar_texto(f'{self.dialogo} En hbo podrías ver...')
            self.aux_final = True
            self.aux_catego_deporte = False
            x = 'deporte_hbo'
        elif preg.__contains__('salir') or preg.__contains__('sueltame') or preg.__contains__('olvidalo'):
            self.aux = True
            self.aux_catego_deporte = False
            self.insertar_texto(f'{self.dialogo} Ok.')
            return None             
        else:
            self.insertar_texto(f'{self.dialogo} No entendí lo que dijiste, intenta de nuevo.')
            self.aux = True
            x = None
        return x 

    def sub_clasificacion_animacion(self,preg):
        self.aux = False
        if preg.__contains__('netflix'):
            self.insertar_texto(f'{self.dialogo} En Netflix podrías ver...')
            self.aux_final = True
            self.aux_catego_animacion = False
            x = 'animacion_netflix'
        elif preg.__contains__('hbo'):
            self.insertar_texto(f'{self.dialogo} En hbo podrías ver...')
            self.aux_final = True
            self.aux_catego_animacion = False
            x = 'animacion_hbo'
        elif preg.__contains__('salir') or preg.__contains__('sueltame') or preg.__contains__('olvidalo'):
            self.aux = True
            self.aux_catego_animacion = False
            self.insertar_texto(f'{self.dialogo} Ok.')
            return None              
        else:
            self.insertar_texto(f'{self.dialogo} No entendí lo que dijiste, intenta de nuevo.')
            self.aux = True
            x = None
        return x

    def sub_clasificacion_docu(self,preg):
        self.aux = False
        if preg.__contains__('netflix'):
            self.insertar_texto(f'{self.dialogo} En Netflix podrías ver...')
            self.aux_final = True
            self.aux_catego_docu = False
            x = 'docu_netflix'
        elif preg.__contains__('hbo'):
            self.insertar_texto(f'{self.dialogo} En hbo podrías ver...')
            self.aux_final = True
            self.aux_catego_docu = False
            x = 'docu_hbo'
        elif preg.__contains__('salir') or preg.__contains__('sueltame') or preg.__contains__('olvidalo'):
            self.aux = True
            self.aux_catego_docu = False
            self.insertar_texto(f'{self.dialogo} Ok.')
            return None              
        else:
            self.insertar_texto(f'{self.dialogo} No entendí lo que dijiste, intenta de nuevo.')
            self.aux = True
            x = None
        return x   

    def verificar_cat_principales(self,preg):
        try: 
            self.grafo[preg]   # verificar si es un mensaje válido
            for cat in self.categorias_principales:
                if cat == preg:
                    self.aux_cat_principal = True
                    return preg 
                else:
                    pass
            self.aux_cat_principal = False
            return preg
        except KeyError:    # si no es válido
            self.aux_cat_principal = True
            return preg       

    def set_memoria_cantidad(self,preg):
        if preg.__contains__('todas') or preg.__contains__('muchas') or preg.__contains__('todo'):
            self.memoria_cantidad = 'todas'
            self.aux_memoria_cantidad = False
            self.aux_final = True
            return self.memoria_temporal
        elif preg.__contains__('una') or preg.__contains__('azar') or preg.__contains__('quieras'):
            self.memoria_cantidad = 'una'
            self.aux_memoria_cantidad = False
            self.aux_final = True
            return self.memoria_temporal
        elif preg.__contains__('salir') or preg.__contains__('sueltame') or preg.__contains__('olvidalo'):
            self.aux = True
            self.aux_memoria_cantidad = False
            self.insertar_texto(f'{self.dialogo} Ok.')
            return None       
        else:
            self.insertar_texto(f'{self.dialogo} No logro entender a lo que te refieres, intentalo de nuevo.')
            self.aux = True
            return None

    def codigo_github(self):
        import webbrowser
        webbrowser.open('https://github.com/victornietol/Proyectos/blob/main/Proyecto_Mate_Disc/Actualizacion_27_05_2022/ProyectoMates_Disc/chatbot_pruebas2.py')

    def acerca(self):
        mb.showinfo('Acerca de ...',(open('informacion/acerca.txt', encoding='utf-8').read()) )

    def cerra_ayuda(self):
        self.v_ayuda.destroy()

    def ayuda(self):
        # Nueva ventana
        self.v_ayuda = Toplevel(self.ventana)
        self.v_ayuda.title('Ayuda')
        self.v_ayuda.iconbitmap('imagenes/bot3.ico')
        self.v_ayuda.geometry('445x465')
        self.v_ayuda.config(background='white')
        self.separador_a = ttk.Separator(self.v_ayuda, orient='horizontal')
        self.separador_a.pack(fill='x')

        # Texto
        self.texto_ayuda = tk.Text(self.v_ayuda, height=30, width=60, borderwidth=0, font=('Bahnschrift Light', 10)
                                , wrap='word')
        self.texto_ayuda.place(x=12, y=12)    
        self.texto_ayuda.configure(state='normal')
        self.texto_ayuda.insert(tk.END,(open('informacion/ayuda.txt',encoding='utf-8').read()))  
        self.texto_ayuda.configure(state='disabled')
        self.v_ayuda.resizable(0,0)

        # Parte baja de la ventana
        self.ayuda_frame = tk.Frame(self.v_ayuda,width='445', height='40')
        self.ayuda_frame.pack(side='bottom')

        # Boton
        self.boton_aceptar =ttk.Button(self.ayuda_frame, cursor='hand2', 
                                text='Aceptar', command=self.cerra_ayuda).place(x=360,y=8) 

    def interfaz(self):
        self.ventana = tk.Tk()
        self.ventana.geometry('500x680')
        self.ventana.title('Chatbot')
        self.ventana.iconbitmap('imagenes/bot3.ico')
        self.ventana.resizable(0,0)
        self.v_frame = tk.Frame(self.ventana,width='500', height='570', bg='white')
        self.v_frame2 = tk.Frame(self.ventana,width='500', height='50')
        self.separador = ttk.Separator(self.ventana, orient='horizontal') # linea de separacion entre los dos frames
        self.img = Image.open('imagenes/enviar11.png')
        self.img = ImageTk.PhotoImage(self.img)
        self.img_perfil = tk.PhotoImage(file='imagenes/bot10.png')
        self.img_codigo = tk.PhotoImage(file='imagenes/codigo.png')
        self.img_ayuda = tk.PhotoImage(file='imagenes/inter1.png')
        self.img_info = tk.PhotoImage(file='imagenes/info.png')

        # parte de arriba del chat
        self.v_frame3 = tk.Frame(self.ventana, width='500', height='60', bg='#16345a')
        self.foto_perfil = tk.Label(self.v_frame3, image=self.img_perfil, borderwidth=0)
        self.foto_perfil.place(x=18, y=3)
        self.nombre_bot = tk.Label(self.v_frame3, text='Chatbot', font=('Bahnschrift', 16), 
                                        background='#16345a', foreground='white')
        self.nombre_bot.place(x=80, y=12)

        # caja de texto
        self.chat = tk.Text(self.v_frame, height=30, width=50, borderwidth=0, font=('Bahnschrift', 12)
                                , wrap='word')
        self.chat.place(x=18, y=10)

        # scrollbar
        self.scrollbar = tk.Scrollbar(self.v_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.chat.yview)
        self.chat.config(yscrollcommand=self.scrollbar.set)        
        
        # entrada de texto
        self.captura_texto = tk.StringVar()
        self.entry_texto = ttk.Entry(self.v_frame2, textvariable=self.captura_texto, 
                                        font=('Bahnschrift Light', 12))
        self.entry_texto.config(justify=LEFT)
        self.entry_texto.place(x=10, y=10, width=400, height=30)
        self.entry_texto.bind('<Return>', lambda e:self.enviar())

        # boton enviar
        self.boton_enviar = tk.Button(self.v_frame2, image=self.img, cursor='hand2', borderwidth=0,  
                                        command=self.enviar).place(x=430,y=2)      

        #
        self.v_frame3.pack(side=tk.TOP)
        self.v_frame.pack(fill='both', expand='True')
        self.v_frame2.pack(side='bottom')
        self.separador.pack(fill='x')

        # mensaje inicial
        self.insertar_texto(f'{self.dialogo} Hola, soy Chatbot, ¿en qué te puedo ayudar?')

        # boton codigo
        self.boton_codigo = tk.Button(self.v_frame3, image=self.img_codigo, cursor='hand2', borderwidth=0, 
                                        background='#16345a', command=self.codigo_github).place(x=450, y=12)

        # boton ayuda
        self.boton_ayuda = tk.Button(self.v_frame3, image=self.img_ayuda, cursor='hand2', borderwidth=0,
                                        background='#16345a', command=self.ayuda).place(x=410, y=12)     

        # boton info
        self.boton_info = tk.Button(self.v_frame3, image=self.img_info, cursor='hand2', borderwidth=0,
                                        background='#16345a', command=self.acerca).place(x=375, y=12)                

        
        self.ventana.mainloop()

iniciar = Chatbot()
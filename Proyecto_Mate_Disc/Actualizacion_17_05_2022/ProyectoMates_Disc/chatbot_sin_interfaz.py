import re, random, requests
import numpy as np
from unicodedata import normalize
from datetime import datetime

class Chatbot:
    def __init__(self):
        self.info()
        self.iniciar()

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
        self.grafo['top_global']=(open('canciones/spotify/top_global.txt', encoding='utf-8')).read()
        self.grafo['top_mex']=(open('canciones/spotify/top_mex.txt', encoding='utf-8')).read()
        self.grafo['entrenamiento']=(open('canciones/spotify/entre.txt', encoding='utf-8')).read()
        self.grafo['pop']=(open('canciones/spotify/pop.txt', encoding='utf-8')).read()
        self.grafo['urbano']=(open('canciones/spotify/urbano.txt', encoding='utf-8')).read()
        self.grafo['romance']=(open('canciones/spotify/romance.txt', encoding='utf-8')).read()
        self.grafo['cumbia']=(open('canciones/spotify/cumbia.txt', encoding='utf-8')).read()
        self.grafo['salsa']=(open('canciones/spotify/salsa.txt', encoding='utf-8')).read()
        self.grafo['rock']=(open('canciones/spotify/rock.txt', encoding='utf-8')).read()
        self.grafo['hiphop']=(open('canciones/spotify/hiphop.txt', encoding='utf-8')).read()
        self.grafo['electronica']=(open('canciones/spotify/electronica.txt', encoding='utf-8')).read()
        self.grafo['jazz']=(open('canciones/spotify/jazz.txt', encoding='utf-8')).read()
        self.grafo['clasica']=(open('canciones/spotify/clasica.txt', encoding='utf-8')).read()
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

        self.grafo['info']= { 'netflix':(open('informacion/netflix.txt', encoding='utf-8').read()),
                                'hbo':(open('informacion/hbo.txt', encoding='utf-8').read()),
                                'disney+':(open('informacion/disney.txt', encoding='utf-8').read()),
                                'spotify':(open('informacion/spotify.txt', encoding='utf-8').read()),
                                'youtube':(open('informacion/youtube.txt', encoding='utf-8').read())
                            }

        self.dialogo = 'Chatbot:'
        self.vertices = list(self.grafo.keys())
        self.vertices_sinopsis = list(self.grafo['sinopsis'].keys())
        self.vertices_informacion = list(self.grafo['info'].keys())
        self.vertices_spotify = ['top_global','top_mex','entrenamiento','pop','urbano','romance','cumbia',
                                    'salsa','rock','hiphop','electronica','jazz','clasica']

    def quitar_acentos(self,x):
        x = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", x), 0, re.I)
        x = normalize('NFC',x)
        return x

    def clasificacion_pregunta(self,x):
        if (('esta' in x) and ('clima' in x)) or ('clima' in x) or ('temperatura' in x):
            self.aux_clima = True
            x = 'clima'
        elif ('sinopsis' in x) or ('que trata' in x) or ('resumen' in x):
            self.pelicula = x
            x = 'sinopsis'           
        elif ('fecha' in x) or (('dia' in x) and ('es' in x)):
            x = 'fecha'
        elif ('hora' in x) or (('hora' in x) and ('cual' in x)):
            self.aux_hora = True
            x = 'hora'        
        elif (('que' in x) and ('es' in x) and ('netflix' in x)) or \
            (('que' in x) and ('es' in x) and ('spotify' in x)) or \
            (('que' in x) and ('es' in x) and ('hbo' in x)) or \
            (('que' in x) and ('es' in x) and ('disney+' in x)) or\
            (('que' in x) and ('es' in x) and ('youtube' in x)) or ('informacion' in x):
            self.informacion = x
            x = 'info'        
        elif (('peliculas' in x) and ('netflix' in x)) or \
            (('recomendaciones' in x) and ('peliculas' in x) and ('netflix' in x)):
            x = 'pel_cat_netflix'
            self.pregunta_aux = 'netflix'
        elif (('peliculas' in x) and ('hbo' in x)) or \
            (('recomendaciones' in x) and ('peliculas' in x) and ('hbo' in x)):
            x = 'pel_cat_hbo'
            self.pregunta_aux = 'hbo'
        elif (('peliculas' in x) and ('disney+' in x)) or \
            (('recomendaciones' in x) and ('peliculas' in x) and ('disney+' in x)):
            x = 'cat_disney'
            self.pregunta_aux = 'disney+'
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
                print(f'{self.dialogo} Puedo darte recomendaciones de series en plataformas como Netflix, HBO Max y Disney+,'
                +' o puedo darte una recomendación al azar. ¿Qué prefieres?')
                preg = input('Tú: ')
                if preg.__contains__('netflix'):
                    x = 'series_netflix'
                    self.pregunta_aux = 'netflix'
                elif preg.__contains__('hbo'):
                    x = 'series_hbo'
                    self.pregunta_aux = 'hbo'
                elif preg.__contains__('disney+'):
                    x = 'series_disney'
                    self.pregunta_aux = 'disney+'
        elif (('peliculas' in x) and ('accion' in x)) or ('accion' in x):    # valorando categorias de peliculas
            if self.pregunta_aux == 'netflix':
                x = 'accion_netflix'
            elif self.pregunta_aux == 'hbo':
                x = 'accion_hbo'
            elif self.pregunta_aux == '':
                preg = input(f'{self.dialogo} Puedo mostrarte peliculas de acción en Netflix y HBO Max, ¿Cuál prefieres?.\nTú: ')
                if preg.__contains__('netflix'):
                    x = 'accion_netflix'
                elif preg.__contains__('hbo'):
                    x = 'accion_hbo'
        elif (('peliculas' in x) and ('comedia' in x)) or ('comedia' in x):
            if self.pregunta_aux == 'netflix':
                x = 'comedia_netflix'
            elif self.pregunta_aux == 'hbo':
                x = 'comedia_hbo'
            elif self.pregunta_aux == '':                
                preg = input(f'{self.dialogo} Puedo mostrarte peliculas de comedia en Netflix y HBO Max, ¿Cuál prefieres?.\nTú: ')
                if preg.__contains__('netflix'):
                    x = 'comedia_netflix'
                elif preg.__contains__('hbo'):
                    x = 'comedia_hbo'            
        elif (('peliculas' in x) and ('terror' in x)) or ('terror' in x):
            if self.pregunta_aux == 'netflix':
                x = 'terror_netflix'
            elif self.pregunta_aux == 'hbo':
                x = 'terror_hbo'
            elif self.pregunta_aux == '':                
                preg = input(f'{self.dialogo} Puedo mostrarte peliculas de terror en Netflix y HBO Max, ¿Cuál prefieres?.\nTú: ')
                if preg.__contains__('netflix'):
                    x = 'terror_netflix'
                elif preg.__contains__('hbo'):
                    x = 'terror_hbo'             
        elif (('peliculas' in x) and ('deporte' in x)) or ('deporte' in x):
            if self.pregunta_aux == 'netflix':
                x = 'deporte_netflix'
            elif self.pregunta_aux == 'hbo':
                x = 'deporte_hbo'
            elif self.pregunta_aux == '':                
                preg = input(f'{self.dialogo} Puedo mostrarte peliculas de deporte en Netflix y HBO Max, ¿Cuál prefieres?.\nTú: ')
                if preg.__contains__('netflix'):
                    x = 'deporte_netflix'
                elif preg.__contains__('hbo'):
                    x = 'deporte_hbo'                 
        elif (('peliculas' in x) and ('animacion' in x)) or ('animacion' in x):
            if self.pregunta_aux == 'netflix':
                x = 'animacion_netflix'
            elif self.pregunta_aux == 'hbo':
                x = 'animacion_hbo'
            elif self.pregunta_aux == '':                
                preg = input(f'{self.dialogo} Puedo mostrarte peliculas de animadas en Netflix y HBO Max, ¿Cuál prefieres?.\nTú: ')
                if preg.__contains__('netflix'):
                    x = 'animacion_netflix'
                elif preg.__contains__('hbo'):
                    x = 'animacion_hbo'                 
        elif (('peliculas' in x) and ('pixar' in x)) or ('pixar' in x):
            x = 'pixar'
        elif (('peliculas' in x) and ('marvel' in x)) or ('marvel' in x):
            x = 'marvel'
        elif (('peliculas' in x) and ('star wars' in x)) or ('star wars' in x):
            x = 'starwars'
        elif (('peliculas' in x) and ('disney' in x)) or ('disney' in x):
            x = 'disney'
        elif (('recomendaciones' in x) and ('peliculas' in x)) or ('peliculas' in x):  # comprobando si son peliculas
            if self.pregunta_aux == 'netflix':
                x = 'pel_cat_netflix'
            elif self.pregunta_aux == 'hbo':
                x = 'pel_cat_hbo'
            elif self.pregunta_aux == 'disney+':
                x = 'cat_disney'
            elif self.pregunta_aux == '':       # si es la primera vez que se busca pelicula
                print(f'{self.dialogo} Puedo darte recomendaciones de peliculas en plataformas como Netflix, HBO Max y Disney+,'
                +' o puedo darte una recomendación al azar. ¿Qué prefieres?')
                preg = input('Tú: ')
                if preg.__contains__('netflix'):
                    print(f'{self.dialogo} En Netflix tengo recomendaciones de:')
                    x = 'pel_cat_netflix'
                    self.pregunta_aux = 'netflix' # 'pel_cat_netflix'
                elif preg.__contains__('hbo'):
                    print(f'{self.dialogo} En HBO tengo recomendaciones de:')
                    x = 'pel_cat_hbo'
                    self.pregunta_aux = 'hbo'  # 'pel_cat_hbo'
                elif preg.__contains__('disney+'):
                    print(f'{self.dialogo} En Disney+ tengo recomendaciones de:')
                    x = 'cat_disney'
                    self.pregunta_aux = 'disney+'  # 'cat_disney'       
        elif (('recomendaciones' in x) and ('documentales' in x)) or ('documentales' in x):     # comprobando si son documentales
            if self.pregunta_aux == 'netflix':
                x = 'docu_netflix'
            elif self.pregunta_aux == 'hbo':
                x = 'docu_hbo'
            elif self.pregunta_aux == '':                
                preg = input(f'{self.dialogo} Puedo mostrarte documentales en Netflix y HBO Max, ¿Cuál prefieres?.\nTú: ')
                if preg.__contains__('netflix'):
                    x = 'docu_netflix'
                elif preg.__contains__('hbo'):
                    x = 'docu_hbo'

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
        elif (('recomendaciones' in x) and ('canciones' in x)) or ('canciones' in x):
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
            print(f'{self.dialogo} En Netflix tengo recomendaciones de:')
        elif preg.__contains__('recomendaciones') and preg.__contains__('spotify'):
            print(f'{self.dialogo} En Spotify tengo recomendaciones de:')
        elif preg.__contains__('recomendaciones') and preg.__contains__('hbo'):
            print(f'{self.dialogo} En HBO Max tengo recomendaciones de:')
        elif preg.__contains__('recomendaciones') and preg.__contains__('disney+'):
            print(f'{self.dialogo} En Disney+ tengo recomendaciones de:')
        elif preg.__contains__('recomendaciones') and preg.__contains__('youtube'):
            print(f'{self.dialogo} En Youtube tengo recomendaciones de canales de las siguientes categorias:')

    def mensaje_inic(self,preg):
        if preg.__contains__('adios') or preg.__contains__('hasta luego') or preg.__contains__('nos vemos') or preg.__contains__('gracias'):
            print(f'{self.dialogo} Hasta luego :)')
            self.aux = True
        elif preg.__contains__('buenos dias') or preg.__contains__('hola') or preg.__contains__('como estas')\
            or preg.__contains__('que tal') or preg.__contains__('buenas tardes') or preg.__contains__('buenas noches'):
            preg = 'saludo'
            print(f'{self.dialogo} {random.choice(self.grafo[preg])}', end='.\n')
            self.aux2 = True
            self.aux_hora = False
        elif preg.__contains__('netflix') or preg.__contains__('hbo') or preg.__contains__('spotify') \
            or preg.__contains__('disney+') or preg.__contains__('youtube') or preg.__contains__('canciones')\
            or preg.__contains__('series') or preg.__contains__('documentales') or preg.__contains__('podcasts')\
            or preg.__contains__('mascotas') or preg.__contains__('videojuegos') or preg.__contains__('cocina')\
            or preg.__contains__('niños') or preg.__contains__('tecnologia') or preg.__contains__('autos'):
            pass   
        elif preg.__contains__('recomendaciones'):
            print(f'{self.dialogo} Tengo recomendaciones de las siguientes plaformas:')

    def lectura_recomendaciones(self,preg):
        try:
            if preg == 'recomendaciones':  # si se pregunta por recomendaciones
                print(f'{self.dialogo}', end=' ')
            for i in self.grafo[preg]:      # entrando al grafo
                if preg == 'recomendaciones':       # evaluando si solo se esta pidiendo que recomendaciones se tienen (netflix, spot,etc)
                    if self.grafo[preg][-1] == i:
                        print(f'{i.title()}', end='.\n')
                    else:
                        print(f'{i.title()}', end=', ')
                elif (self.grafo[preg][0] == i) and (self.grafo[preg][-1] == i):    # si es opcion unica
                    print(f'{self.dialogo} {i.title()}', end='.\n')
                elif self.grafo[preg][0] == i:                                          # si es la primera sugerencia
                    print(f'{self.dialogo} {i.title()}', end=', ')
                elif (self.grafo[preg][0] != i) and (self.grafo[preg][-1] != i):    # si es la sugerencia de enmedio
                    print(f'{i.title()}', end=', ')
                elif self.grafo[preg][-1] == i:                                         # si es la sugerencia del final
                    print(f'{i.title()}', end='.\n')
        except KeyError:                                                                    # si no encuentra el indice
            print(f'{self.dialogo} Mmmmm... no entiendo lo que dijiste, intenta de nuevo.')                                                                 # si no encuentra el indice

    def lectura_canciones(self,preg):
        print(f'{self.dialogo} Tal vez podrías escuchar las siguientes canciones:\n{self.grafo[preg]}')

    def lectura_sinopsis(self,preg):
        encontrado = False
        for sinopsis in self.vertices_sinopsis:
            if self.pelicula.__contains__(sinopsis):
                encontrado = True
                if self.memoria_pel == sinopsis:
                    print(f'{self.dialogo} Mmmmmm... lee un poco más arriba, esa sinopsis ya te la mostre ;)')                
                else:              #elif (self.memoria_pel == '') or (self.memoria_pel != sinopsis):   <=== otra forma mas larga     
                    print(f'{self.dialogo} La sinopsis es la siguiente...\n{self.grafo[preg][sinopsis]}')
                    self.memoria_pel = sinopsis
            else:
                pass
        if encontrado == False:
            print(f'{self.dialogo} Lo siento, esa película no esta dentro de mis'
                    +' recomendaciones. Intenta de nuevo.')

    def lectura_informacion(self,preg):
        encontrado = False
        for info in self.vertices_informacion:
            if self.informacion.__contains__(info):
                encontrado = True
                print(f'{self.dialogo} Según mis datos {self.grafo[preg][info]}')
            else:
                pass
        if encontrado == False:
            print(f'{self.dialogo} Lo siento, no cuento con información sobre ese tema.')

    def iniciar(self):
        self.aux = False
        self.pregunta_aux = ''
        self.memoria_pel = ''
        print(f'{self.dialogo} Hola, soy Chatbot, ¿en qué te puedo ayudar?')
        while self.aux == False:
            self.aux2 = False
            pregunta_ = input('Tú: ')
            pregunta = pregunta_.lower()
            pregunta = self.quitar_acentos(pregunta)
            self.mensaje_inic(pregunta)
            self.mensaje_rec(pregunta)
            pregunta = self.clasificacion_pregunta(pregunta)
            if self.aux:    # evalua si es el final
                break
            elif self.aux2:     # evalua si es el saludo 
                pass
            elif pregunta in self.vertices_spotify:
                self.lectura_canciones(pregunta)
            elif pregunta == 'sinopsis':
                self.lectura_sinopsis(pregunta)
            elif pregunta == 'clima':
                self.clima_actual()
            elif pregunta == 'fecha':
                print(f'{self.dialogo} Hoy es {self.fecha_actual()}.')
            elif pregunta == 'hora':
                x = self.hora_actual()
                h = x[0]
                m = x[1]
                s = x[2]
                print(f'{self.dialogo} Son las {h} horas, con {m} minutos y {s} segundos.')
            elif pregunta == 'info':
                self.lectura_informacion(pregunta)
            else:
                self.lectura_recomendaciones(pregunta)

    def recorrer(self):
        for v in self.vertices:
            print(f'{v} ==> {self.grafo[v]}')

    def fecha_actual(self):
        hoy = datetime.now()
        meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre',
                    'octubre','noviembre','diciembre']
        dia = hoy.day
        mes = meses[hoy.month - 1]
        anio = hoy.year
        fecha = '{} de {} del {}'.format(dia,mes,anio)
        return fecha

    def clima_actual(self):
        api_key = '6178f7e3724caaa34a0175e55cf22525'
        url = 'http://api.openweathermap.org/data/2.5/weather?'
        ciudad = input(f'{self.dialogo} Ingrese la ciudad por favor.\nTú: ')
        url_completo = url + 'appid=' + api_key + '&q=' + ciudad + '&units=metric'
        response = requests.get(url_completo)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            temp = y["temp"]
            humedad = y["humidity"]
            z = x["weather"]
            descripcion = z[0]["description"]
            print(f'{self.dialogo} Un momento... Los datos obtenidos para {ciudad.title()} ' 
                    +f'son:\nTemperatura: {temp} °C\nDescripcion: {descripcion}\nHumedad: {humedad}%')
        else:
            print(f'{self.dialogo} No se encuentra la ciudad')

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
            print(f'{self.dialogo} No se encuentra la ciudad')                

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

iniciar = Chatbot()
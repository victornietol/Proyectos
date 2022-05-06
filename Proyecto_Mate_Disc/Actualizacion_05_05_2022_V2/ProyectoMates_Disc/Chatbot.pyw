import re, random
from unicodedata import normalize

class Chatbot:
    def __init__(self):
        self.info()
        self.iniciar()

    def info(self):
        self.grafo = {}
        self.grafo['buenos dias']=['Hola, la temperatura de hoy es de 16 grados', 'Arriba la máquina del Cruz Azul', 'Tardes ya', 'Hola, tengo poca bateria']
        self.grafo['recomendaciones']=['netflix','HBO Max','disney+','spotify','youtube']

        # nefltix
        self.grafo['netflix']=['peliculas','series','documentales']
        self.grafo['pel_cat_netflix']=['acción','comedia','terror','deporte','animación']
        self.grafo['accion_netflix']=['the adam project','la vieja guardia','el ejército de los ladrones','john wick 3','misión de rescate']
        self.grafo['comedia_netflix']=['volver al futuro 3','paul','super cool','un espía y medio','alerta roja']
        self.grafo['terror_netflix']=['nadie sale con vida','la bruja','eli','las formas antiguas','el rito']
        self.grafo['deporte_netflix']=['rush','jugar en casa','83','la verdad oculta', 'novato']
        self.grafo['animacion_netflix']=['spider man: un nuevo universo','sonic','vivo','shrek','como entrenar a tu dragon 2']
        self.grafo['series_nettlix']=['peaky blinders','better call saul','breaking bad','ozark','the witcher'] 
        self.grafo['docu_netflix']=['el último baile','what the health','the toys that made us','making a murderer','ícaro'] 

        # hbo max
        self.grafo['hbo']=['peliculas','series','documentales'] 
        self.grafo['pel_cat_hbo']=['acción','comedia','terror','deporte','animación']
        self.grafo['accion_hbo']=['batman','ready player one','matrix resurrections','parque jurásico','los juegos del hambre']
        self.grafo['comedia_hbo']=['una pareja explosiva','30 minutos o menos','amigos de armas','guerra de papás']
        self.grafo['terror_hbo']=['la huérfana','no respires 2','saw','la bruja de blair','insidious']
        self.grafo['deporte']=['rey richard','invictus','american underdog','el juego de la fortuna']
        self.grafo['animacion_hbo']=['space jam','la gran aventura lego','stuart little','el cadáver de la novia']
        self.grafo['series_hbo']=['the big bang theory','game of thrones','friends','rick and morty','the mentalist']
        self.grafo['docu_hbo']=['cuidado con slenderman','mcmillions','the inventor','a la caza de Bin Laden','asesinas']

        # disney+
        self.grafo['disney+']=['peliculas','series']
        self.grafo['cat_disney']=['pixar','marvel','star wars','disney']
        self.grafo['disney']=['frozen 2','dinosaurio','el libro de la selva','tarzán','zootopía']
        self.grafo['pixar']=['los increibles','red','coco','toy story','cars']
        self.grafo['marvel']=['iron man','capitan america y el soldado del invierno','avengers endgame','thor ragnarok','guardianes de la galaxia']
        self.grafo['starwars']=['rogue one','han solo','una nueva esperanza','el imperio contrataca','el regreso del jedi']
        self.grafo['series_disney']=['hawkeye','moon knight','el libro de boba fett','the mandalorian','loki','what if?','malcolm','wandavision']

        # spotify
        self.grafo['spotify']=['canciones','podcasts']
        self.grafo['canciones_spotify']= ['top 10 global','top 10 méxico','entrenamiento','pop','urbano','romance','cumbia','salsa', 
                                            'rock','hip hop','electronica','jazz','clásica']
        self.grafo['s_top_global']=(open('canciones/spotify/top_global.txt', encoding='utf-8')).read()
        self.grafo['s_top_mex']=(open('canciones/spotify/top_mex.txt', encoding='utf-8')).read()
        self.grafo['s_entrenamiento']=(open('canciones/spotify/entre.txt', encoding='utf-8')).read()
        self.grafo['s_pop']=(open('canciones/spotify/pop.txt', encoding='utf-8')).read()
        self.grafo['s_urbano']=(open('canciones/spotify/urbano.txt', encoding='utf-8')).read()
        self.grafo['s_romance']=(open('canciones/spotify/romance.txt', encoding='utf-8')).read()
        self.grafo['s_cumbia']=(open('canciones/spotify/cumbia.txt', encoding='utf-8')).read()
        self.grafo['s_salsa']=(open('canciones/spotify/salsa.txt', encoding='utf-8')).read()
        self.grafo['s_rock']=(open('canciones/spotify/rock.txt', encoding='utf-8')).read()
        self.grafo['s_hiphop']=(open('canciones/spotify/hiphop.txt', encoding='utf-8')).read()
        self.grafo['s_electronica']=(open('canciones/spotify/electronica.txt', encoding='utf-8')).read()
        self.grafo['s_jazz']=(open('canciones/spotify/jazz.txt', encoding='utf-8')).read()
        self.grafo['s_clasica']=(open('canciones/spotify/clasica.txt', encoding='utf-8')).read()
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
        self.grafo['sinopsis']= { 'the adam project':(open('sinopsis/proy_adam.txt', encoding='utf-8')), 
                                    'la vieja guardia':(open('sinopsis/viejag.txt', encoding='utf-8')), 
                                    'el ejercito de los ladrones':(open('sinopsis/ejercito_lad.txt', encoding='utf-8')), 
                                    'john wick 3':(open('sinopsis/jw3.txt', encoding='utf-8')), 
                                    'mision de rescate':(open('sinopsis/mision_r.txt', encoding='utf-8')), 
                                    'volver al futuro 3':(open('sinopsis/volver_f3.txt', encoding='utf-8')), 
                                    'paul':(open('sinopsis/paul.txt', encoding='utf-8')), 
                                    'super cool':(open('sinopsis/super_c.txt', encoding='utf-8')), 
                                    'un espia y medio':(open('sinopsis/espia_med.txt', encoding='utf-8')), 
                                    'alerta roja':(open('sinopsis/alerta_r.txt', encoding='utf-8')), 
                                    'nadie sale con vida':(open('sinopsis/nadie_sv.txt', encoding='utf-8')), 
                                    'la bruja':(open('sinopsis/bruja.txt', encoding='utf-8')), 
                                    'eli':(open('sinopsis/eli.txt', encoding='utf-8')), 
                                    'las formas antiguas':(open('sinopsis/formas_ant.txt', encoding='utf-8')), 
                                    'el rito':(open('sinopsis/rito.txt', encoding='utf-8')),
                                    'rush':(open('sinopsis/rush.txt', encoding='utf-8')),
                                    'jugar en casa':(open('sinopsis/jugar_casa.txt', encoding='utf-8')),
                                    '83':(open('sinopsis/83.txt', encoding='utf-8')),
                                    'la verdad oculta':(open('sinopsis/verdad_oculta.txt', encoding='utf-8')),
                                    'novato':(open('sinopsis/novato.txt', encoding='utf-8')),
                                    'spiderman':(open('sinopsis/spiderman.txt', encoding='utf-8')),
                                    'sonic':(open('sinopsis/sonic.txt', encoding='utf-8')),
                                    'vivo':(open('sinopsis/vivo.txt', encoding='utf-8')),
                                    'shrek':(open('sinopsis/shrek.txt', encoding='utf-8')),
                                    'como entrenar a tu dragon':(open('sinopsis/entrenar_dragon.txt', encoding='utf-8')),
                                    'peaky blinders':(open('sinopsis/p_blinders.txt', encoding='utf-8')),
                                    'better call saul':(open('sinopsis/better_c_s.txt', encoding='utf-8')),
                                    'breaking bad':(open('sinopsis/breaking_bad.txt', encoding='utf-8')),
                                    'ozark':(open('sinopsis/ozark.txt', encoding='utf-8')),
                                    'the witcher':(open('sinopsis/witcher.txt', encoding='utf-8')),
                                    'el ultimo baile':(open('sinopsis/ultimo_baile.txt', encoding='utf-8')),
                                    'what the health':(open('sinopsis/what_health.txt', encoding='utf-8')),
                                    'the toys that':(open('sinopsis/the_toys.txt', encoding='utf-8')),
                                    'making a murderer':(open('sinopsis/making_murderer.txt', encoding='utf-8')),
                                    'icaro':(open('sinopsis/icaro.txt', encoding='utf-8')),
                                    'batman':(open('sinopsis/batman.txt', encoding='utf-8')),
                                    'ready player one':(open('sinopsis/r_player_o.txt', encoding='utf-8')),
                                    'matrix resurrections':(open('sinopsis/matrix.txt', encoding='utf-8')),
                                    'parque jurasico':(open('sinopsis/parque_j.txt', encoding='utf-8')),
                                    'los juegos del hambre':(open('sinopsis/juegos_hambre.txt', encoding='utf-8')),
                                    'una pareja explosiva':(open('sinopsis/pareja_exp.txt', encoding='utf-8')),
                                    '30 minutos o menos':(open('sinopsis/30_minutos.txt', encoding='utf-8')),
                                    'amigos de armas':(open('sinopsis/amigos_armas.txt', encoding='utf-8')),
                                    'guerra de papas':(open('sinopsis/guerra_papas.txt', encoding='utf-8')),
                                    'la huerfana':(open('sinopsis/huerfana.txt', encoding='utf-8')),
                                    'no respires':(open('sinopsis/no_respires.txt', encoding='utf-8')),
                                    'saw':(open('sinopsis/saw.txt', encoding='utf-8')),
                                    'la bruja de blair':(open('sinopsis/bruja_blair.txt', encoding='utf-8')),
                                    'insidious':(open('sinopsis/insidious.txt', encoding='utf-8')),
                                    'rey richard':(open('sinopsis/r_richard.txt', encoding='utf-8')),
                                    'invictus':(open('sinopsis/invictus.txt', encoding='utf-8')),
                                    'american underdog':(open('sinopsis/underdog.txt', encoding='utf-8')),
                                    'el juego de la fortuna':(open('sinopsis/fortuna_juego.txt', encoding='utf-8')),
                                    'space jam':(open('sinopsis/space_jam.txt', encoding='utf-8')),
                                    'la gran aventura lego':(open('sinopsis/lego.txt', encoding='utf-8')),
                                    'stuart little':(open('sinopsis/stuart_l.txt', encoding='utf-8')),
                                    'el cadaver de la novia':(open('sinopsis/cad_novia.txt', encoding='utf-8')),
                                    'the big bang theory':(open('sinopsis/big_bt.txt', encoding='utf-8')),
                                    'game of thrones':(open('sinopsis/game_t.txt', encoding='utf-8')),
                                    'friends':(open('sinopsis/friends.txt', encoding='utf-8')),
                                    'rick and morty':(open('sinopsis/rick_morty.txt', encoding='utf-8')),
                                    'the mentalist':(open('sinopsis/mentalist.txt', encoding='utf-8')),
                                    'cuidado con slenderman':(open('sinopsis/slenderman.txt', encoding='utf-8')),
                                    'mcmillions':(open('sinopsis/mcmillions.txt', encoding='utf-8')),
                                    'the inventor':(open('sinopsis/inventor.txt', encoding='utf-8')),
                                    'a la casa de bin laden':(open('sinopsis/bin_laden.txt', encoding='utf-8')),
                                    'asesinas':(open('sinopsis/asesinas.txt', encoding='utf-8')),
                                    'frozen 2':(open('sinopsis/frozen2.txt', encoding='utf-8')),
                                    'dinosaurio':(open('sinopsis/dinosaurio.txt', encoding='utf-8')),
                                    'el libro de la selva':(open('sinopsis/libro_selva.txt', encoding='utf-8')),
                                    'tarzan':(open('sinopsis/tarzan.txt', encoding='utf-8')),
                                    'zootopia':(open('sinopsis/zootopia.txt', encoding='utf-8')),
                                    'los increibles':(open('sinopsis/increibles.txt', encoding='utf-8')),
                                    'red':(open('sinopsis/red.txt', encoding='utf-8')),
                                    'coco':(open('sinopsis/coco.txt', encoding='utf-8')),
                                    'toy story':(open('sinopsis/toy_story.txt', encoding='utf-8')),
                                    'cars':(open('sinopsis/cars.txt', encoding='utf-8')),
                                    'rogue one':(open('sinopsis/rogue_one.txt', encoding='utf-8')),
                                    'han solo':(open('sinopsis/han_solo.txt', encoding='utf-8')),
                                    'una nueva esperanza':(open('sinopsis/n_esperanza.txt', encoding='utf-8')),
                                    'el imperio contrataca':(open('sinopsis/imp_cont.txt', encoding='utf-8')),
                                    'el regreso del jedi':(open('sinopsis/reg_jedi.txt', encoding='utf-8')),
                                    'iron man':(open('sinopsis/ironman.txt', encoding='utf-8')),
                                    'capitan america y el soldado del invierno':(open('sinopsis/capitan_a.txt', encoding='utf-8')),
                                    'avengers endgame':(open('sinopsis/a_endgame.txt', encoding='utf-8')),
                                    'thor ragnarok':(open('sinopsis/thor.txt', encoding='utf-8')),
                                    'guardianes de la galaxia':(open('sinopsis/guardianes_g.txt', encoding='utf-8')),
                                    'hawkeye':(open('sinopsis/hawkeye.txt', encoding='utf-8')),
                                    'moon knight':(open('sinopsis/moonknight.txt', encoding='utf-8')),
                                    'el libro de boba fett':(open('sinopsis/boba_fett.txt', encoding='utf-8')),
                                    'the mandalorian':(open('sinopsis/mandalorian.txt', encoding='utf-8')),
                                    'loki':(open('sinopsis/loki.txt', encoding='utf-8')),
                                    'what if?':(open('sinopsis/what_if.txt', encoding='utf-8')),
                                    'malcolm':(open('sinopsis/malcolm.txt', encoding='utf-8')),
                                    'wandavision':(open('sinopsis/wandavision.txt', encoding='utf-8'))
                                }


        self.dialogo = 'Chatbot:'
        self.vertices = list(self.grafo.keys())

    def quitar_acentos(self,x):
        x = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", normalize( "NFD", x), 0, re.I)
        x = normalize('NFC',x)
        return x

    def clasificacion_pregunta(self,x):
        if ('netflix' in x) and ('recomendaciones' in x):
            x = 'netflix'
        elif ('spotify' in x) and ('recomendaciones' in x):
            x = 'spotify'
        elif ('hbo' in x) and ('recomendaciones' in x):
            x = 'hbo'
        elif ('disney+' in x) and ('recomendaciones' in x):
            x = 'disney+'
        elif ('youtube' in x) and ('recomendaciones' in x):
            x = 'youtube'
        elif ('recomendaciones' in x) and ('peliculas' in x):
            x = 'peliculas'
        elif ('recomendaciones' in x) and ('series' in x):
            x = 'series'
        elif ('recomendaciones' in x) and ('documentales' in x):
            x = 'documentales'
        elif ('recomendaciones' in x) and ('canciones' in x):
            x = 'canciones'
        elif ('recomendaciones' in x) and ('listas' in x) and ('reproduccion' in x) :
            x = 'listas de reproduccion'    
        elif ('recomendaciones' in x) and ('podcast' in x):
            x = 'podcasts'
        elif ('recomendaciones' in x) and ('podcast' in x):
            x = 'podcasts'
        elif ('recomendaciones' in x):
            x = 'recomendaciones'
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
        elif (preg == 'buenos dias'):
            print(f'{self.dialogo} {random.choice(self.grafo[preg])}', end='.\n')
            self.aux2 = True
        elif preg.__contains__('netflix') or preg.__contains__('hbo') or preg.__contains__('spotify') or preg.__contains__('disney+') or preg.__contains__('youtube'):
            pass   
        elif preg.__contains__('recomendaciones'):
            print(f'{self.dialogo} Tengo recomendaciones de las siguientes plaformas:')

    def iniciar(self):
        self.aux = False
        print(f'{self.dialogo} Hola, soy Chatbot, ¿en que te puedo ayudar?')
        while self.aux == False:
            self.aux2 = False
            pregunta_ = input('Tú: ')
            pregunta = pregunta_.lower()
            pregunta = self.quitar_acentos(pregunta)
            self.mensaje_inic(pregunta)
            self.mensaje_rec(pregunta)
            pregunta = self.clasificacion_pregunta(pregunta)
            if self.aux:
                break
            elif self.aux2:
                pass
            else:
                try:
                    if pregunta == 'recomendaciones':  # si se pregunta por recomendaciones
                        print(f'{self.dialogo}', end=' ')
                    for i in self.grafo[pregunta]:      # entrando al grafo
                        if pregunta == 'recomendaciones':       # evaluando si solo se esta pidiendo que recomendaciones se tienen (netflix, spot,etc)
                            if self.grafo[pregunta][-1] == i:
                                print(f'{i.capitalize()}', end='.\n')
                            else:
                                print(f'{i.capitalize()}', end=', ')
                        elif (self.grafo[pregunta][0] == i) and (self.grafo[pregunta][-1] == i):    # si es opcion unica
                            print(f'{self.dialogo} {i.capitalize()}', end='.\n')
                        elif self.grafo[pregunta][0] == i:                                          # si es la primera sugerencia
                            print(f'{self.dialogo} {i.capitalize()}', end=', ')
                        elif (self.grafo[pregunta][0] != i) and (self.grafo[pregunta][-1] != i):    # si es la sugerencia de enmedio
                            print(f'{i}', end=', ')
                        elif self.grafo[pregunta][-1] == i:                                         # si es la sugerencia del final
                            print(f'{i}', end='.\n')
                except KeyError:                                                                    # si no encuentra el indice
                    print(f'{self.dialogo} Mmmmm... no entiendo lo que dijiste, intenta de nuevo.')

    def recorrer(self):
        for v in self.vertices:
            print(f'{v} ==> {self.grafo[v]}')

    def interfaz(self):
        pass

iniciar = Chatbot()
#iniciar.recorrer()
import re, random
from unicodedata import normalize

class Chatbot:
    def __init__(self):
        self.info()
        self.iniciar()

    def info(self):
        self.grafo = {}
        self.grafo['buenos dias']=['Hola, la temperatura de hoy es de 16 grados', 'Arriba la máquina del Cruz Azul', 'Tardes ya', 'Hola, tengo poca bateria']
        self.grafo['recomendaciones']=['netflix','hbo max','disney+','spotify','apple music']
        self.grafo['netflix']=['peliculas','series','documentales']
        self.grafo['pel_cat_netflix']=['acción','comedia','terror','deporte','animación']
        self.grafo['accion_netflix']=['the adam project','la vieja guardia','el ejercito de los ladrones','john wick 3','mision de rescate']
        self.grafo['comedia_netflix']=['volver al futuro 3','paul','super cool','un espia y medio','alerta roja']
        self.grafo['terror_netflix']=['nadie sale con vida','la bruja','eli','las formas antiguas','el rito']
        self.grafo['deporte_netflix']=['rush','jugar en casa','83','la verdad oculta', 'novato']
        self.grafo['animacion_netflix']=['spider man: un nuevo universo','sonic','vivo','shrek','como entrenar a tu dragon 2']
        self.grafo['series_nettlix']=['peaky blinders','better call saul','breaking bad','ozark','the witcher'] 
        self.grafo['docu_netflix']=['el ultimo baile','what the health','the toys that made us','making a murderer','icaro'] 

        self.grafo['hbo']=['peliculas','series'] 

        self.grafo['spotify']=['canciones', 'listas de reproduccion', 'podcasts']
        self.grafo['canciones']=['Mis recomendaiciones son cancion 1, cancion 2 cancion 3']
        self.grafo['listas de reproduccion']=['lista 1, lista 2, lista 3']
        self.grafo['podcasts']=['Mis recomendaciones son podcast 1, podcast 2, podcast 3']

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
                                    'como entrenar dragon':(open('sinopsis/entrenar_dragon.txt', encoding='utf-8')),
                                    'peaky blinders':(open('sinopsis/p_blinders.txt', encoding='utf-8')),
                                    'better call saul':(open('sinopsis/better_c_s.txt', encoding='utf-8')),
                                    'breaking bad':(open('sinopsis/breaking_bad.txt', encoding='utf-8')),
                                    'ozark':(open('sinopsis/ozark.txt', encoding='utf-8')),
                                    'the witcher':(open('sinopsis/witcher.txt', encoding='utf-8')),
                                    'el ultimo baile':(open('sinopsis/ultimo_baile.txt', encoding='utf-8')),
                                    'what the health':(open('sinopsis/what_health.txt', encoding='utf-8')),
                                    'the toys that':(open('sinopsis/the_toys', encoding='utf-8')),
                                    'making a murderer':(open('sinopsis/making_murderer', encoding='utf-8')),
                                    'icaro':(open('sinopsis/icaro', encoding='utf-8')),
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

    def mensaje_inic(self,preg):
        if preg.__contains__('adios') or preg.__contains__('hasta luego') or preg.__contains__('nos vemos') or preg.__contains__('gracias'):
            print(f'{self.dialogo} Hasta luego :)')
            self.aux = True
        elif (preg == 'buenos dias'):
            print(f'{self.dialogo} {random.choice(self.grafo[preg])}', end='.\n')
            self.aux2 = True
        elif preg.__contains__('netflix') or preg.__contains__('spotify'):
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
                    if pregunta == 'recomendaciones':
                        print(f'{self.dialogo}', end=' ')
                    for i in self.grafo[pregunta]:
                        if pregunta == 'recomendaciones':
                            if self.grafo[pregunta][-1] == i:
                                print(f'{i.capitalize()}', end='.\n')
                            else:
                                print(f'{i.capitalize()}', end=', ')
                        elif (self.grafo[pregunta][0] == i) and (self.grafo[pregunta][-1] == i):
                            print(f'{self.dialogo} {i.capitalize()}', end='.\n')
                        elif self.grafo[pregunta][0] == i:
                            print(f'{self.dialogo} {i.capitalize()}', end=', ')
                        elif (self.grafo[pregunta][0] != i) and (self.grafo[pregunta][-1] != i):
                            print(f'{i}', end=', ')
                        elif self.grafo[pregunta][-1] == i:
                            print(f'{i}', end='.\n')
                except KeyError:
                    print(f'{self.dialogo} Mmmmm... no entiendo lo que dijiste, intenta de nuevo.')

    def recorrer(self):
        for v in self.vertices:
            print(f'{v} ==> {self.grafo[v]}')

    def interfaz(self):
        pass

iniciar = Chatbot()
#iniciar.recorrer()
import re, random
from unicodedata import normalize

class Chatbot:
    def __init__(self):
        self.info()
        self.iniciar()

    def info(self):
        self.grafo = {}
        self.grafo['buenos dias']=['Hola, la temperatura de hoy es de 16 grados', 'Arriba la máquina del Cruz Azul', 'Tardes ya', 'Hola, tengo poca bateria']
        self.grafo['recomendaciones']=['netflix', 'spotify']
        self.grafo['netflix']=['peliculas', 'series', 'documentales']
        self.grafo['peliculas']=['Mis recomendaciones son Spiderman 3, Doctor S']
        self.grafo['series']=['Mis recomendaciones son Breaking Bad, The Witcher, The Mentalist']
        self.grafo['documentales']=['Mis recomendaciones son nulas porque no he revisado los documentales']
        self.grafo['spotify']=['canciones', 'listas de reproduccion', 'podcasts']
        self.grafo['canciones']=['Mis recomendaiciones son cancion 1, cancion 2 cancion 3']
        self.grafo['listas de reproduccion']=['lista 1, lista 2, lista 3']
        self.grafo['podcasts']=['Mis recomendaciones son podcast 1, podcast 2, podcast 3']

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
        if preg.__contains__('adios') or preg.__contains__('hasta luego') or preg.__contains__('nos vemos'):
            print(f'{self.dialogo} Hasta luego :)')
            self.aux = True
        elif (preg == 'buenos dias'):
            print(f'{self.dialogo} {random.choice(self.grafo[preg])}')
            self.aux2 = True
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
                    for i in self.grafo[pregunta]:
                        print(f'{self.dialogo} {i.capitalize()}')
                except KeyError:
                    print('Chatbot: Mmmmm... no entiendo lo que dijiste, intenta de nuevo')

    def recorrer(self):
        for v in self.vertices:
            print(f'{v} ==> {self.grafo[v]}')

iniciar = Chatbot()
#iniciar.recorrer()
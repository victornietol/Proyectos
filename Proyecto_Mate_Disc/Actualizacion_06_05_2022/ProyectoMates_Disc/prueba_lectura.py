#archivo = open('terminator2.txt', encoding='utf-8')
#print(archivo.read())

graf = {}
'''
graf['ter']= (open('terminator2.txt', encoding='utf-8')).read() 
print(graf['ter'])

graf['ter']= (open('terminator2.txt', encoding='utf-8'))
print(graf['ter'].read())
'''

graf['sin']={ 'la bruja':(open('sinopsis/bruja.txt', encoding='utf-8')), 
              'peaky blinders':(open('sinopsis/p_blinders.txt', encoding='utf-8')) 
            }


vertices = list(graf['sin'].keys())
print(vertices)
prueba = input('Tu: ')
for peliculas in vertices:
  if prueba.__contains__(peliculas):
    print(graf['sin'][peliculas].read())
  else:
    pass
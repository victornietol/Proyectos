#archivo = open('terminator2.txt', encoding='utf-8')
#print(archivo.read())

graf = {}
'''
graf['ter']= (open('terminator2.txt', encoding='utf-8')).read() 
print(graf['ter'])

graf['ter']= (open('terminator2.txt', encoding='utf-8'))
print(graf['ter'].read())
'''

graf['sin']={ 'sin_ter':(open('sinopsis/bruja.txt', encoding='utf-8')), 
              'sin_glad':(open('sinopsis/p_blinders.txt', encoding='utf-8')) 
            }
print(graf['sin']['sin_glad'].read())
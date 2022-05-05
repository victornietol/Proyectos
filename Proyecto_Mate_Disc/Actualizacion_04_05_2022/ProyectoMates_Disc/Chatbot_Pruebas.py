from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
chat = ChatBot('cctmx')
talk= ['hola', '¿que tal?', '¿tengo una pregunta?']
trainer = ListTrainer(chat)
trainer.train(talk)
while True:
  peticion = input('Tu: ')
  respuesta = chat.get_response(peticion)
  print('Bot: ', respuesta)
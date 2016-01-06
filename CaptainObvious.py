#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path
import codecs
import unicodedata
import string
import numpy as np
import matplotlib.pyplot as plt


def strip_accents(s):
	return ''.join(c for c in unicodedata.normalize('NFD', s)
					if unicodedata.category(c) != 'Mn')


PUNTOS_PENALIZACION = 25


# Lectura de parámetros de entrada
args = len(sys.argv)
if args < 5:
	sys.exit("Error: Falta un parámetro de entrada. Uso: CaptainObvious.py NumRonda FicheroPreguntas FicheroRespuestas FicheroGeneral")
elif args > 5:
	sys.exit("Error: Demasiados parámetros. Uso: CaptainObvious.py NumRonda FicheroPreguntas FicheroRespuestas FicheroGeneral")
else:
	NumRonda = int(sys.argv[1])
	FicheroPreguntas = sys.argv[2]
	FicheroRespuestas = sys.argv[3]
	FicheroGeneral = sys.argv[4]

# Verificación de la existencia de los ficheros indicados
if not os.path.isfile(FicheroPreguntas):
	sys.exit("Error: El fichero de preguntas especificado no existe.")
elif not os.path.isfile(FicheroRespuestas):
	sys.exit("Error: El fichero de respuestas especificado no existe.")
elif not os.path.isfile(FicheroGeneral):
	sys.exit("Error: El fichero con la clasificación general especificado no existe.")


# Lectura de las preguntas
preguntas = dict()
contador = 1
for linea in codecs.open(FicheroPreguntas,'r','utf-8').readlines():
	preg = dict()
	linea = linea.strip()
	preg['enunciado'] = linea
	preg['respuestas'] = dict() # A "rellenar" al leer las respuestas de los jugadores para esta ronda
	preguntas[contador] = preg
	contador += 1


# Lectura de la clasificación general
jugadores = dict()
for linea in codecs.open(FicheroGeneral,'r','utf-8').readlines():
	jugador = dict()
	ausencias_jugador = 0
	dummy, nombre_jugador, puntos_jugador = linea.strip().split(' - ')
	# Si el jugador ha faltado en alguna ronda anterior...
	if puntos_jugador[-5:-2] == ' (-':
		ausencias_jugador = int(puntos_jugador[-2]) #...anotamos sus ausencias...
		puntos_jugador = puntos_jugador[:-5] #...y nos quedamos sólo con los puntos del jugador
	puntos_jugador = int(puntos_jugador)
	jugador['juega'] = False # Se convertirá en True si el jugador participa en la ronda actual
	jugador['ausencias'] = ausencias_jugador
	jugador['puntos_general'] = puntos_jugador
	jugador['puntos_ronda'] = 0
	jugador['respuestas'] = dict() # A "rellenar" al leer las respuestas de los jugadores para esta ronda
	jugador['puntos'] = dict() # A "rellenar" al calcular las puntuaciones de cada pregunta
	jugadores[nombre_jugador] = jugador


# Lectura de las respuestas de los jugadores
print "\nParticipantes:\n"
participantes = 0
nuevos_jugadores = list() # Servirá para "detectar" jugadores que se incorporan al juego por 1ª vez
contador = 0
for linea in codecs.open(FicheroRespuestas,'r','utf-8').readlines():
	penalizacion = False
	linea = linea.strip()
	# Las líneas 1, 14, 27, 40... contienen el nombre de un participante
	if contador == 0:
		participantes += 1 # Para las estadísticas
		jugador = linea
		if jugador[-3:] == '***':  # Si el nombre del jugador acaba en "***"...
			jugador = jugador[:-3]
			penalizacion = True    # ...penalización!
		print "{0}".format(jugador)
		if jugador not in jugadores: # Si este jugador no aparece en la general es que es nuevo
			nuevos_jugadores.append(jugador)
			jugadores[jugador] = dict()
			jugadores[jugador]['ausencias'] = NumRonda-1 # Si es nuevo, se habrá perdido todas las rondas anteriores
			jugadores[jugador]['puntos_general'] = 0
			jugadores[jugador]['puntos_ronda'] = 0
			jugadores[jugador]['respuestas'] = dict()
			jugadores[jugador]['puntos'] = dict()
		jugadores[jugador]['juega'] = True
		jugadores[jugador]['penalizacion'] = penalizacion
		if penalizacion:
			jugadores[jugador]['puntos_ronda'] = -PUNTOS_PENALIZACION
	# El resto de líneas contienen respuestas del jugador "jugador"
	else:
		respuesta = linea.lower() # Convertimos la respuesta toda a minúsculas...
		respuesta = strip_accents(respuesta) #...le quitamos tildes...
		for caracter in string.punctuation: #...y signos de puntuación
			respuesta = respuesta.replace(caracter,"")
		jugadores[jugador]['respuestas'][contador] = respuesta
	contador += 1
	if contador == 13:
		contador = 0
print "\n--------------------------------"
print "\nNuevos jugadores en esta ronda:"
for nuevo_jugador in nuevos_jugadores:
	print nuevo_jugador
print "\n--------------------------------"


# Recuento de respuestas y suma de puntuaciones
for preg in range(1,13):
	for jugador in jugadores:
		if jugadores[jugador]['juega']:
			respuesta = jugadores[jugador]['respuestas'][preg]
			# Rellenamos el diccionario "respuestas" de "preguntas[preg]" y sumamos puntos
			if respuesta not in preguntas[preg]['respuestas']:
				preguntas[preg]['respuestas'][respuesta] = 1
			else:
				preguntas[preg]['respuestas'][respuesta] += 1

	print "\n\n[size=150][b]{0}[/b][/size]\n\n\n\n[img]XXX[/img]\n\n\n\nblablabla\n\n\n\n[b][u]Puntuaciones[/u][/b]".format(preguntas[preg]['enunciado'])
	# Ordenamos las respuestas a la pregunta "preg" en orden descendiente de puntos
	for resp in sorted(preguntas[preg]['respuestas'], key=preguntas[preg]['respuestas'].get, reverse=True):
		if preguntas[preg]['respuestas'][resp] == 1: # Si una pregunta ha obtenido un sólo voto...
			preguntas[preg]['respuestas'][resp] = 0 #...contará como un cero!
		print "[b]{0}:[/b] {1}".format(resp, preguntas[preg]['respuestas'][resp])

	print "\n\n\n[b][u]Respuestas de los participantes[/u][/b]"
	# Volvemos a ordenar las respuestas por orden descendiente de puntos...
	for resp in sorted(preguntas[preg]['respuestas'], key=preguntas[preg]['respuestas'].get, reverse=True):
		linea = ''
		for jug in sorted(jugadores):
			if jugadores[jug]['juega']:
				if jugadores[jug]['respuestas'][preg] == resp:
					#...y vamos construyendo la lista de jugadores que han contestado cada opción
					linea = linea + jug + ', '
					jugadores[jug]['puntos'][preg] = preguntas[preg]['respuestas'][resp]
					jugadores[jug]['puntos_ronda'] += preguntas[preg]['respuestas'][resp]
		linea = linea[:-2] + '.' # Para que la lista no acabe en una coma y un espacio en blanco
		print "[b]{0}:[/b] {1}".format(resp, linea)
	print "\n--------------------------------"

	# Clasificación parcial
	# Creamos un nuevo diccionario con los jugadores que participan en esta ronda y los puntos que llevan
	clasificacion_ronda = dict()
	for jug in jugadores:
		if jugadores[jug]['juega']:
			clasificacion_ronda[jug] = jugadores[jug]['puntos_ronda']

	print "\nClasificación después de {0} preguntas:".format(preg)
	contador = 0
	puntos_anterior = -1
	for jug in sorted(clasificacion_ronda, key=clasificacion_ronda.get, reverse=True):
		puntos = clasificacion_ronda[jug]
		# Si el jugador actual lleva los mismos puntos que el anterior, no aumentamos la posición
		if puntos != puntos_anterior:
			posicion = contador + 1 
		# Si el jugador ha tenido penalización, lo indicamos con un asterisco en la clasificación
		if jugadores[jug]['penalizacion']:
			print "{0} - {1} - {2}*".format(posicion, jug, puntos)
		else:
			print "{0} - {1} - {2}".format(posicion, jug, puntos)
		puntos_anterior = puntos
		contador += 1
	print "\n--------------------------------"


# Estadísticas
print "\nParticipantes: {0}".format(participantes)
puntuacion_maxima_real = max(clasificacion_ronda.values())
puntuacion_maxima_posible = 0
# Cálculo de la puntuación máxima posible en esta ronda
for preg in range(1,13):
	puntuacion_maxima_posible += max(preguntas[preg]['respuestas'].values())
print "Puntuación máxima posible: {0}".format(puntuacion_maxima_posible)
print "Puntuación ganador: {0} ({1:.1f}%)".format(puntuacion_maxima_real, 100.0*puntuacion_maxima_real/puntuacion_maxima_posible)
print "Media de puntos: {0:.1f}".format(np.average(clasificacion_ronda.values()))
print "Desviación estándar: {0:.1f}".format(np.std(clasificacion_ronda.values()))
print "\n--------------------------------"
# Funciones de matplotlib para crear un histograma de 10 barras con las puntuaciones de la ronda
plt.hist(clasificacion_ronda.values(),10)
plt.title("Distribucion de puntuaciones")
plt.xlabel("Puntos")
plt.ylabel("Frecuencia")
plt.show()


# Faltan por participar
# Útil para saber a quién "avisar" cuando falta poco para que acabe el plazo de respuestas
print "\nJugadores que no han participado en esta ronda:"
for jug in sorted(jugadores):
	if not jugadores[jug]['juega']: # Si el jugador no ha participado en esta ronda...
		jugadores[jug]['ausencias'] += 1 #...se le aumenta su número de ausencias...
		print "{0}".format(jug) #...y se pone su nombre en la lista de tardones
print "\n--------------------------------"


# Clasificación general
# Mismo mecanismo que para calcular las clasificaciones parciales
print "\nClasificación general"
clasificacion_general = dict()
for jug in jugadores:
	if jugadores[jug]['juega']:
		jugadores[jug]['puntos_general'] += clasificacion_ronda[jug]
	clasificacion_general[jug] = jugadores[jug]['puntos_general']
contador = 0
puntos_anterior = -1
for jug in sorted(clasificacion_general, key=clasificacion_general.get, reverse=True):
	puntos = jugadores[jug]['puntos_general']
	if puntos != puntos_anterior:
		posicion = contador + 1
	if jugadores[jug]['ausencias'] > 0:
		print "{0} - {1} - {2} (-{3})".format(posicion, jug, puntos, jugadores[jug]['ausencias'])
	else:
		print "{0} - {1} - {2}".format(posicion, jug, puntos)
	puntos_anterior = puntos
	contador += 1
print "\n--------------------------------"

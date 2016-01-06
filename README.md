# Captain Obvious

Programa para gestionar un juego del estilo "Captain Obvious": 12 preguntas por ronda, y cada concursante gana tantos puntos como el número de gente que haya contestado lo mismo.


### Requisitos
Para el correcto funcionamiento de este programa, los siguientes módulos de python deben de estar instalados:
* codecs
* matplotlib
* numpy
* os
* string
* sys
* unicodedata


### Sintaxis
`python CaptainObvious.py NumRonda FicheroPreguntas FicheroRespuestas FicheroGeneral`


### Parámetros

* **NumRonda**: Número de la actual ronda del juego. Sirve para calcular las ausencias de posibles nuevos jugadores

* **FicheroPreguntas**: Ruta del fichero que contiene las preguntas de la ronda actual. Detalles sobre su formato más abajo.

* **FicheroRespuestas**: Ruta del fichero que contiene los nombres de los participantes en la ronda actual y sus respuestas. Detalles sobre su formato más abajo.

* **FicheroGeneral**: Ruta del fichero que contiene la clasificación general anterior a la ronda actual. Detalles sobre su formato más abajo.


### Ficheros de entrada

* **FicheroPreguntas**: Solamente debe contener 12 líneas de texto con cada pregunta en una línea diferente. Las preguntas se pueden numerar como se prefiera (aparecerán en la salida tal cual estén en este fichero). **Importante:** Este fichero no puede contener carácteres que no pertenezcan al [conjunto básico ASCII](http://learn.parallax.com/reference/ascii-table-0-127) (es decir, vocales con tilde, eñes, etc.). Ejemplo:
```
1. Una ciudad asiatica
2. Una pelicula de Brad Pitt
3. Una palabra en ingles
4. Una casa de Juego de Tronos
5. Una franquicia NBA que no haya ganado nunca el anillo
6. Un ser mitologico
7. Un pais cuyo idioma oficial sea el Espanol (que no sea Espana)
8. Una princesa Disney
9. Una letra de talla de ropa
10. Un animal en peligro de extincion
11. El forero que mas anima el juego del Captain Obvious (que no sea un organizador)
12. Algo navideno
```

* **FicheroRespuestas**: Este fichero debe contener, en líneas sucesivas, el nombre del participante y sus 12 respuestas para esta ronda. Es decir, la línea 1 contiene el nombre del participante#1, la línea 2 contiene la respuesta#1 del participante#1, y así sucesivamente hasta la línea 13, que contiene la respuesta#12 del participante#1. Entonces la línea 14 contiene el nombre del participante#2 y vuelta a empezar. **Importante:** Los nombres de los participantes no pueden llevar tildes, eñes, ni otros carácteres no pertenecientes al [conjunto básico ASCII](http://learn.parallax.com/reference/ascii-table-0-127). Ejemplo:
```
fulano
respuesta-1-de-fulano
respuesta-2-de-fulano
respuesta-3-de-fulano
respuesta-4-de-fulano
respuesta-5-de-fulano
respuesta-6-de-fulano
respuesta-7-de-fulano
respuesta-8-de-fulano
respuesta-9-de-fulano
respuesta-10-de-fulano
respuesta-11-de-fulano
respuesta-12-de-fulano
mengano
respuesta-1-de-mengano
respuesta-2-de-mengano
...
```

* **FicheroGeneral**: Fichero que contiene la clasificación general previa a la ronda actual. En cada línea aparece un participante con su posición, sus puntos y, en caso de haberse perdido alguna ronda anterior, su número de ausencias entre paréntesis y en negativo). **Importante:** Al igual que en el fichero anterior, los nombres de los participantes no pueden llevar tildes, eñes, ni otros carácteres no pertenecientes al [conjunto básico ASCII](http://learn.parallax.com/reference/ascii-table-0-127). Ejemplo:
```
1 - fulano - 555
2 - mengano - 550
2 - zutano - 550
4 - perengano - 400 (-1)
```


### Salida del programa

El programa vuelca todos los resultados por STDIN (es decir, por pantalla). Como estos resultados pueden ocupar muchas líneas, se recomienda redirigir la salida del programa a un fichero de resultados:
```
python CaptainObvious.py NumRonda FicheroPreguntas FicheroRespuestas FicheroGeneral > FicheroResultados
```

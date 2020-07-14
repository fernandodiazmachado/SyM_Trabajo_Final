# Este es un programa de ejemplo de cómo debería incorporarse la visualización del sistema de Teoría de Colas desarrollado en la primera parte del TP
# Modificar y completar todo lo que consideren necesario

import time
import curses
from curses import wrapper

def imprimirTitulo(screen):
	screen.addstr(0,0,'Servidores (X = ocupado, " " = desocupado)')
	
def imprimirDatos(screen):
	servidores = 100
	
	fila = 1
	columna = 1
	for i in range(servidores):
		screen.addstr(fila,columna,'{:02d}: |   | '.format(i))
		if fila % 20 == 0:
			fila = 1
			columna += 20
		else:
			fila += 1
		
	screen.addstr(22,0,'Cantidad de clientes en espera (en la cola): {}'.format("???"))
	screen.addstr(23,0,'Cantidad de mediciones: {}'.format("???"))
	screen.addstr(24,0,'Tiempo global: {}'.format("???"))
	screen.addstr(26,0,'L: {}'.format("???"))
	screen.addstr(27,0,'Lq: {}'.format("???"))
	screen.addstr(26,50,'W: {}'.format("???"))
	screen.addstr(27,50,'Wq: {}'.format("???"))
		

def actualizarEstadoServidores(screen,ocupado):
	servidores = 100
	fila = 1
	columna = 7
	for i in range(servidores):
		if ocupado:
			screen.addstr(fila,columna,'X')
		else: 
			screen.addstr(fila,columna,' ')
		if fila % 20 == 0:
			fila = 1
			columna += 20
		else:
			fila += 1

def iniciar(screen):
	#1) inicialización de variables	
	#2.1) crear instancia de estadistica
	#2.2) crear instancia de sistema	
	#3) llegada 1er. cliente

	imprimirTitulo(screen)	

	imprimirDatos(screen)
	
	terminar = False
	
	i = 0
	while(not terminar):
		screen.nodelay(True)

		#sistema.procesar()

		#estadistica.procesar()	

		actualizarEstadoServidores(screen,i % 2 == 0)
		
		time.sleep(0.5)
		
		i += 1
		#terminar con la tecla "f"
		if (screen.getch() == ord('f')):
			terminar = True

wrapper(iniciar)


#comentarios:
# A continuacion se detalla el esqueleto de la primera parte del trabajo de Teoria de Colas. El modelo que seguiremos es el de un supermercado con una cola y multiples servidores (o cajas de atencion) 
# prefijo de las variables:
#	f: float
#	i: int
#	v*: vector o lista de tipo *
#   c: instancia de una clase

def distribucionExponencial(lamda):
# implemetntacion de la practica 3

class Cliente:
	def __init__(self, fTiempoLlegada):
	# inicializa las variables y setea el tiempo de llegada del cliente

	def setTiempoInicioAtencion(self,fTiempoInicioAtencion):
	# setter del tiempo del inicio de atencion del cliente
	
	def setTiempoSalida(self, fTiempoSalida):
	# setter del tiempo de salida del cliente
		
class Sistema:
	def __init__(self, fTasaLlegadaClientes, vfTasasAtencionServidores):
	# inicializa: la tasa de llegada de clientes, el tiempo global
	# crea la cola de clientes
	# crea la lista de servidores (llama al metodo creacionServidores)
	# crea la bolsa de eventos

	def creacionServidores(self):
	# crea la lista de servidores respetando la respectivas tasa de antención
	
	def eventoProximoCliente(self):
	# genera un evento de tipo EventoProximoCliente 
	
	def ingresoCliente(self): 
	# callback para la clase EventoProximoCliente.procesar
	# corresponde a la llegada efectiva del cliente
	# 1) crea el Cliente
	# 2) agrega el cliente a la cola
	# 3) crea el nuevo evento de llegada del proximo cliente (llama a self.eventoProximoCliente())
	# 4) agrega el evento a la bolsa de eventos
		
	def procesar(self):
	# es el metodo más importante porque orquesta toda la simulacion 
	# 1) crea el eventoProximoCliente del 1er. cliente
	# while (True):
	#	2) saca el proximo evento de la bolsa de eventos
	#	3) procesa el evento (via polimorfismo)
	#	4) for s in self.servidores:
			# 5) si el servidor esta desocupado y hay algun cliente en la cola
				# 6) desencolar el primer cliente de la cola
				# 7) generar el evento de FinAtencion 
				# 8) agregar a la bolsa de eventos el evento de FinAtencion
	
class Servidor:
	def __init__(self,fTasaAtencionServidor):
	# inicializa variables
		
	def estaOcupado(self):
	# flag: devuelve "true" si el servidor esta ocupado, y "false" si no
		
	def inicioAtencion(self, fTiempoGlobal,cCliente):
	# setea el servidor en "ocupado"
	# setea el tiempo de inicio atencion del cliente
	# crea y devuelve el EventoFinAtencion

	def finAtencion(self,fTiempo):
	# callback para EventoFinAtencion.procesar
	# setea el tiempo de salida del cliente
	# setea la servidor es desocupado

class Cola:
	def __init__(self):
	# crea la lista que representara la cola de clientes
	
	def cantClientes(self):
	# devuelve la cantidad de clientes que hay en la cola

	def llegaCliente(self,cCliente):
	# agregar el cliente a la cola
		
	def proximoCliente(self):
	# devuelve el primer cliente de la cola (si hay alguno)

# clase base de los eventos 	
class Evento:
	def __init__(self, fTiempo):
	# setea el tiempo de ocurrencia futura del evento
		
	# metodo "lower than" para comparar 2 eventos
	def __lt__(self, other):
		return self.tiempo < other.tiempo
	
	# metodo "gerater than" para comparar 2 eventos
	def __gt__(self, other):
		return self.tiempo > other.tiempo

	# metodo abstracto (debe ser implementado por las subclases)
	def procesar(self):
		pass

#evento correspondiente a la futura finalizacion de atencion de un cliente por parte de un servidor
class EventoFinAtencion(Evento):
	
	def __init__(self, fTiempo, cServidor):
	#llama al constructor de la superclase
	#setea el servidor
	
	def procesar(self):
	# llama a servidor.finAtencion

#evento correspondiente a la futura llegada del proximo cliente
class EventoProximoCliente(Evento):
	
	def __init__(self, cSistema, fTiempo):
	#llama al constructor de la susperclase
	#setea el sistema (notar que recibe el sistema como parametro)
	
	def procesar(self):
	# llama al callback sistema.ingresoCliente()

sistema = Sistema(...,...)
sistema.procesar()

#---------------------------------- IMPORT ------------------------------------------------------------------------
import numpy as np
import math
import heapq
import time
import curses
from curses import wrapper

#----------------------------- METODOS GLOBALES --------------------------------------------------------------------
def uniform():  
  return np.random.random()

def distribucionExponencial(lamda):
  u = uniform()
  return round(-(1/lamda)*math.log(1-u),3)

#----------VISUAL-----------------VISUAL-----------------VISUAL-----------------VISUAL-----------------VISUAL-------
#se comienza a explicar esta parte en el video: clase13-7 minuto 34
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
	screen.addstr(24,0,'Tiempo global: {}'.format("???")) #sistema.tiempoglobal
	screen.addstr(26,0,'L: {}'.format("???")) #sistema.estadistica.l()
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

			#lamda = 2
			#lstSistema = [0.2, 0.3, 0.7] #contiene las distintas tasa de atencion de clientes de cada caja (servidor)
			#Instancio una clase estadistica y se la paso al sistema y el sistema a su vez se la pasa a los servidores
			

	#2.1) crear instancia de estadistica

			#estadistica = Estadistica()

	#2.2) crear instancia de sistema

			#sistema = Sistema(lamda,lstSistema, estadistica)

	#3) llegada 1er. cliente

			#sistema.proximoCliente()  ---> INGRESO EL PRIMER CLIENTE ANTES DE ENTRAR AL WHILE (TRUE) [LO SACO DEL METODO SISTEMA.PROCESAR()

	imprimirTitulo(screen)	

	imprimirDatos(screen)
	
	terminar = False
	
	i = 0
	screen.nodelay(True)
	while(not terminar):

		#sistema.procesar()

		#estadistica.procesar()	---> no iria...  SE REALIZA DENTRO DE SISTEMA

		#clase13-7 minuto 39 comienza a explicar esto
		actualizarEstadoServidores(screen,i % 2 == 0)
		
		time.sleep(0.5)
		
		i += 1
		#terminar con la tecla "f"
		if (screen.getch() == ord('f')):
			terminar = True

wrapper(iniciar)

#----------VISUAL-------fin----------VISUAL--------fin---------VISUAL---------fin--------VISUAL------fin--------

#--------------------------------- ESTADISTICA ------------------------------------------------------------------
class Estadistica:
	def __init__(self):
		#acumulador del tiempo total que pasaron los cleientes en el sistma
		self.tiempoTotalClientesEnSistema = 0
		
		#acumulador del tiempo total que pasaron los clientes en la cola
		self.tiempoTotalClientesEnCola = 0
		
		#acumulador de clientes que fueron atendidos
		self.cantClientesAtendidos = 0
		
		#acumulador de clientes que esperaron en la cola
		self.cantClientesQueEsperaron = 0
		
		#VARIABLES AGREGADAS POR EL PROFESOR PARA CALCULAR L Y Lq -> video 13-7 minuto 32
		self.cantClientesTotalEnSistema = 0         
		self.cantClientesTotalEnCola = 0

		self.cantMediciones = 0
		
	def W(self):
		#W: tiempo promedio que paso un cliente en el sistema
		w = (self.tiempoTotalClientesEnSistema / self.cantClientesAtendidos)
		return w
		
	def Wq(self):
		#Wq: tiempo promedio que paso un cliente en la cola
		wq = (self.tiempoTotalClientesEnCola / self.cantClientesQueEsperaron)
		return wq
		
	def L(self, sistema):                      # NO HACE FALTA RECIBIR POR PARAMETRO EL SISTEMA
		#L: promedio de clientes en el sistema
		l = (self.cantClientesTotalEnSistema / self.cantMediciones)
		return l
		
	def Lq(self,cola):                         # NO HACE FALTA RECIBIR POR PARAMETRO LA COLA
		#Lq: promedio de clientes en la cola
		lq = (self.cantClientesTotalEnCola / self.cantMediciones)
		return lq

	def acumularTiempoTotalClientesEnSistema(self, tiempoClienteEnSistema):
		self.cantClientesAtendidos += 1
		self.tiempoTotalClientesEnSistema += tiempoClienteEnSistema

	def acumularTiempoTotalClientesEnCola(self,tiempoTotalClientesEnCola):
		self.cantClientesQueEsperaron += 1
		self.tiempoTotalClientesEnCola += tiempoTotalClientesEnCola
  
	def actualizarCantidadClientes(self,iCantClientesTotalEnSistema,iCantClientesTotalEnCola): #FALTA UBICAR EL LUGAR DENTRO DEL WHILE DE SISTEMA DONDE LLAMARLO
		self.cantMediciones += 1
		self.cantClientesTotalEnSistema += iCantClientesTotalEnSistema
		self.cantClientesTotalEnCola += iCantClientesTotalEnCola

#--------------------------------- CLIENTE ------------------------------------------------------------------------
class Cliente:
  def __init__(self, fTiempoLlegada):
    # inicializa las variables y setea el tiempo de llegada del cliente
    self.tiempoLlegada = fTiempoLlegada  

  #Llamado desde el servidor
  def setTiempoInicioAtencion(self,fTiempoInicioAtencion):
    # setter del tiempo del inicio de atencion del cliente 
    self.tiempoInicioAtencion = fTiempoInicioAtencion
    self.tiempoPermanenciaEnCola = self.tiempoInicioAtencion - self.tiempoLlegada  #AL MISMO TIEMPO QUE SETEO EL TIEMPO DE ATENCION, SETEO EL TIEMPO DE PERMANENCIA EN LA COLA (PARA CALCULAR Wq)

  def setTiempoSalida(self, fTiempoSalida):
    # setter del tiempo de salida del cliente
    self.tiempoSalida = fTiempoSalida
    self.tiempoPermanciaEnSistema = self.tiempoSalida - self.tiempoLlegada  #AL MISMO TIEMPO QUE SETEO EL TIEMPO DE SALIDA, SETEO EL TIEMPO DE PERMANENCIA EN EL SISTEMA (PARA CALCULAR W)
  
  # metodo "lower than" para comparar 2 eventos
  def __lt__(self, other):
    return self.tiempoLlegada < other.tiempoLlegada
	
  # metodo "gerater than" para comparar 2 eventos
  def __gt__(self, other):
    return self.tiempoLlegada > other.tiempoLlegada                               

#--------------------------------- SISTEMA -------------------------------------------------------------------------		
class Sistema:
  #fTasaLlegadaClientes = lamda (valor fijo)
  #vfTasasAtencionServidores = vector correspondiente a la tasa de atencion de clientes => "u"
  def __init__(self, fTasaLlegadaClientes, vfTasasAtencionServidores, cEstadistica):
    # inicializa: la tasa de llegada de clientes, el tiempo global (guardar fTasaLlegadaClientes en una variable)
    self.tiempoGlobal = 0.0 
    self.tasaLlegadaClientes = fTasaLlegadaClientes
    # crea la cola de clientes
    self.colaClientes = Cola()
	  # crea la lista de servidores (llama al metodo creacionServidores) --> recorro vfTasasAtencionServidores para instanciar cada servidor
    self.vfTasasAtencionServidores = vfTasasAtencionServidores
    self.estadistica = cEstadistica  
    self.listaServidores = []
    self.creacionServidores()        
	  # crea la bolsa de eventos 
    self.bolsaEventos = []
    heapq.heapify(self.bolsaEventos)    

  def creacionServidores(self):
    # crea la lista de servidores respetando la respectivas tasa de antención
    for tasa in self.vfTasasAtencionServidores:
      self.listaServidores.append(Servidor(tasa, self.estadistica))
     
  def eventoProximoCliente(self):
    # genera un evento de tipo EventoProximoCliente
    tiempoFuturo = distribucionExponencial(self.tasaLlegadaClientes) + self.tiempoGlobal    
    evento = EventoProximoCliente(tiempoFuturo, self)
    heapq.heappush(self.bolsaEventos,evento)

  def obtenerServidoresOcupados(self):
    cantServidoresOcupados = 0
    for s in self.listaServidores:
      if s.ocupado:
        cantServidoresOcupados += 1
    return cantServidoresOcupados 

  def obtenerTotalClientes(self):
    cantTotalClientes = self.obtenerServidoresOcupados() + self.colaClientes.cantClientes()
    return cantTotalClientes   

  def ingresoCliente(self): 
	  # callback para la clase EventoProximoCliente.procesar
	  # corresponde a la llegada efectiva del cliente
	  # 1) crea el Cliente
    self.cliente = Cliente(self.tiempoGlobal)
	  # 2) agrega el cliente a la cola
    self.colaClientes.llegaCliente(self.cliente)
	  # 3) crea el nuevo evento de llegada del proximo cliente (llama a self.eventoProximoCliente())
    self.eventoProximoCliente()
	  # 4) agrega el evento a la bolsa de eventos -->hecho en eventoProximoCliente()
    
  def procesar(self): 
	  # 1) crea el eventoProximoCliente del 1er. cliente
    #self.eventoProximoCliente() LO LLAMO DIRECTAMENTE EN VISUAL POR FUERA DEL METODO PROCESAR
    corridas = 0
    evento = heapq.heappop(self.bolsaEventos)
      #	3) procesa el evento (via polimorfismo)
    self.tiempoGlobal = evento.tiempoFuturo
    evento.procesar()
    corridas = corridas + 1
      #	4) for s in self.servidores:
    for s in self.listaServidores:
		# 5) si el servidor esta desocupado y hay algun cliente en la cola
    	if(s.ocupado==False and self.colaClientes.cantClientes()>0):
			# 6) desencolar el primer cliente de la cola
          	primerCliente = self.colaClientes.proximoCliente()
			# 7) llama al metodo servidor.inicioAtencion
          	evento = s.inicioAtencion(self.tiempoGlobal,primerCliente)
			# 8) agregar a la bolsa de eventos el evento de FinAtencion
          	heapq.heappush(self.bolsaEventos,evento)

    self.estadistica.actualizarCantidadClientes(self.obtenerTotalClientes(),self.colaClientes.cantClientes()) #HAY QUE ENCONTRAR EL LUGAR CORRECTO dentro del while PARA COLOCARLO. Minuto 30 video clase 13/7
	
	#while (corridas < 50):
      #	2) saca el proximo evento de la bolsa de eventos
      #evento = heapq.heappop(self.bolsaEventos)
      #	3) procesa el evento (via polimorfismo)
      #self.tiempoGlobal = evento.tiempoFuturo
      #evento.procesar()
      #corridas = corridas + 1
      #	4) for s in self.servidores:
      #for s in self.listaServidores:
        # 5) si el servidor esta desocupado y hay algun cliente en la cola
        #if(s.ocupado==False and self.colaClientes.cantClientes()>0):
          # 6) desencolar el primer cliente de la cola
          #primerCliente = self.colaClientes.proximoCliente()
				  # 7) llama al metodo servidor.inicioAtencion
          #evento = s.inicioAtencion(self.tiempoGlobal,primerCliente)
				  # 8) agregar a la bolsa de eventos el evento de FinAtencion
          #heapq.heappush(self.bolsaEventos,evento)

      #self.estadistica.actualizarCantidadClientes(self.obtenerTotalClientes(),self.colaClientes.cantClientes()) #HAY QUE ENCONTRAR EL LUGAR CORRECTO dentro del while PARA COLOCARLO. Minuto 30 video clase 13/7
#--------------------------------- SERVIDOR -----------------------------------------------------------------------	
#Cajas	
#fTasaAtencionServidor (para cada caja es distinto) = cantidad de clientes que puede atender por unidad de tiempo (este valor se pasa a la exponencial como lamda)
class Servidor:

  def __init__(self,fTasaAtencionServidor, cEstadistica):
    # inicializa variables
    self.ocupado = False
    self.tasaAtencion = fTasaAtencionServidor	 #Va a ser el parámetro de la exponencial, y nos dirá cuanto tiempo demorará en atender a dicho cliente
    self.estadistica = cEstadistica

  def estaOcupado(self):
    # flag: devuelve "true" si el servidor esta ocupado, y "false" si no
    return self.ocupado   
	
  def inicioAtencion(self, fTiempoGlobal,cCliente):   
	  # setea el servidor en "ocupado"
    self.ocupado = True
	  # setea el tiempo de inicio atencion del cliente
    self.clienteActual=cCliente
    self.clienteActual.setTiempoInicioAtencion(fTiempoGlobal)
    self.estadistica.acumularTiempoTotalClientesEnCola(self.clienteActual.tiempoPermanenciaEnCola)    #DUDA: PUEDO LLAMAR A UN METODO DE LA CLASE ESTADISTICA ASI? SIN RECIBIRLA POR PARAMETRO?
    # crea y devuelve el EventoFinAtencion                                               
    tiempoFinAtencion = distribucionExponencial(self.tasaAtencion) + fTiempoGlobal   
    eventoFin = EventoFinAtencion(tiempoFinAtencion,self)  
    return eventoFin                        
    
  def finAtencion(self,fTiempo):
	  # callback para EventoFinAtencion.procesar
	  # setea el tiempo de salida del cliente
    self.clienteActual.setTiempoSalida(fTiempo)
    self.estadistica.acumularTiempoTotalClientesEnSistema(self.clienteActual.tiempoPermanciaEnSistema) #CUANDO EL SERVIDOR SETEA EL TIEMPO DE SALIDA, SE CARGA LA VARIABLE DE tiempoPermanciaEnSistema Y SE LA PASA A LA CLASE ESTADISTICA
	  # setea la servidor es desocupado
    self.ocupado = False
    

#--------------------------------- COLA -------------------------------------------------------------------------
class Cola:
  def __init__(self):
	  # crea la lista que representara la cola de clientes
    self.lstClientes = []
    heapq.heapify(self.lstClientes)
	
  def cantClientes(self):
	  # devuelve la cantidad de clientes que hay en la cola
    return len(self.lstClientes)

  def llegaCliente(self,cCliente):
    # agregar el cliente a la cola            **************¿Se eliminan los clientes alguna vez ?????
    heapq.heappush(self.lstClientes,cCliente)
    #self.lstClientes.append(cCliente)
		
  def proximoCliente(self):
	  # devuelve el primer cliente de la cola (si hay alguno)
    if self.cantClientes() > 0:
      return heapq.heappop(self.lstClientes)
      #return self.lstClientes[0]

#--------------------------------- EVENTO CLASE BASE --------------------------------------------------------------
# clase base de los eventos 	
class Evento:
  #fTiempo -> Moldela un tiempo futuro
  #Para EventoProximoCliente: Tiempo de llegada del proximo cliente (acumulador de tiempo)
  #Para EventoFinAtencion: Tiempo en el que se finalice de atender a un cliente

  def __init__(self, fTiempo):
    # setea el tiempo de ocurrencia futura del evento
    self.tiempoFuturo = fTiempo
	  		
  # metodo "lower than" para comparar 2 eventos
  def __lt__(self, other):
    return self.tiempoFuturo < other.tiempoFuturo
	
  # metodo "gerater than" para comparar 2 eventos
  def __gt__(self, other):
    return self.tiempoFuturo > other.tiempoFuturo

  # metodo abstracto (debe ser implementado por las subclases)
  def procesar(self):
    pass  

#--------------------------------- EVENTO FIN ATENCION --------------------------------------------------------
#evento correspondiente a la futura finalizacion de atencion de un cliente por parte de un servidor
class EventoFinAtencion(Evento):

  def __init__(self, fTiempo, cServidor):
    #llama al constructor de la superclase
    Evento.__init__(self, fTiempo)
    #setea el servidor
    self.servidor = cServidor
    self.tiempo = fTiempo
	  
  def procesar(self):
    # llama a servidor.finAtencion
    print("Proceso EventoFinAtencion--> Tiempo: " + str(self.tiempo))
    self.servidor.finAtencion(self.tiempo)    
	   
#--------------------------------- EVENTO PROXIMO CLIENTE ----------------------------------------------------
#evento correspondiente a la futura llegada del proximo cliente
class EventoProximoCliente(Evento):
	
  def __init__(self, fTiempo, cSistema):
    #llama al constructor de la susperclase
    Evento.__init__(self, fTiempo)
    #setea el sistema (notar que recibe el sistema como parametro)
    self.sistema = cSistema
	
  def procesar(self):
    # llama al callback sistema.ingresoCliente()    
    print("Proceso EventoProximoCliente--> Tiempo: " + str(self.sistema.tiempoGlobal))
    self.sistema.ingresoCliente()

#--------------------------------- MAIN -----------------------------------------------------------------------
#lamda = 2
#lstSistema = [0.2, 0.3, 0.7] #contiene las distintas tasa de atencion de clientes de cada caja (servidor)
#Instancio una clase estadistica y se la paso al sistema y el sistema a su vez se la pasa a los servidores
#estadistica = Estadistica()
#sistema = Sistema(lamda,lstSistema, estadistica)
#sistema.procesar()
#print("PASO TODOS LOS METODOS")




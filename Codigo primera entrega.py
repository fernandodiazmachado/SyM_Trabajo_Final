
#comentarios:
# A continuacion se detalla el esqueleto de la primera parte del trabajo de Teoria de Colas.
#El modelo que seguiremos es el de un supermercado con una cola y multiples servidores (o cajas de atencion) 
# prefijo de las variables:
#	f: float
#	i: int
#	v*: vector o lista de tipo *
# c: instancia de una clase

#---------------------------------- IMPORT ------------------------------------------------------------------------
import numpy as np
import math
import heapq
import time

#----------------------------- METODOS GLOBALES --------------------------------------------------------------------
def uniform():  
  return np.random.random()

#lamda: cantidad de ocurrencias por unidad de tiempo (lamda = 5 --> llegan 5 clientes en una unidad de tiempo a la cola)
#Devuelve el tiempo que va a tardar en llegar el proximo cliente a la fila

#Llegada del proximo cliente a la cola
#lamda = cantidad de ocurrencia de eventos por unidad de tiempo
#Ejemplo: lamda=5 => llegan 5 clientes por unidad de tiempo a la cola
#RETORNA el tiempo que va a tardar en llegar el proximo cliente a la fila
def distribucionExponencial(lamda):
  u = uniform()
  return round(-(1/lamda)*math.log(1-u),3)

#--------------------------------- CLIENTE ------------------------------------------------------------------------
class Cliente:
  def __init__(self, fTiempoLlegada):
    # inicializa las variables y setea el tiempo de llegada del cliente
    self.tiempoLlegada = fTiempoLlegada  

  #Llamado desde el servidor
  def setTiempoInicioAtencion(self,fTiempoInicioAtencion):
    # setter del tiempo del inicio de atencion del cliente 
    self.tiempoInicioAtencion = fTiempoInicioAtencion            

  def setTiempoSalida(self, fTiempoSalida):
    # setter del tiempo de salida del cliente
    self.tiempoSalida = fTiempoSalida  

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
  def __init__(self, fTasaLlegadaClientes, vfTasasAtencionServidores):
    # inicializa: la tasa de llegada de clientes, el tiempo global (guardar fTasaLlegadaClientes en una variable)
    self.tiempoGlobal = 0.0 
    self.tasaLlegadaClientes = fTasaLlegadaClientes
    # crea la cola de clientes
    self.colaClientes = Cola()
	  # crea la lista de servidores (llama al metodo creacionServidores) --> recorro vfTasasAtencionServidores para instanciar cada servidor
    self.vfTasasAtencionServidores = vfTasasAtencionServidores  
    self.listaServidores = []
    self.creacionServidores()        
	  # crea la bolsa de eventos 
    self.bolsaEventos = []
    heapq.heapify(self.bolsaEventos)    

  def creacionServidores(self):
    # crea la lista de servidores respetando la respectivas tasa de antención
    for tasa in self.vfTasasAtencionServidores:
      self.listaServidores.append(Servidor(tasa))
     
  def eventoProximoCliente(self):
    # genera un evento de tipo EventoProximoCliente
    tiempoFuturo = distribucionExponencial(self.tasaLlegadaClientes) + self.tiempoGlobal    
    evento = EventoProximoCliente(tiempoFuturo, self)
    heapq.heappush(self.bolsaEventos,evento)

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
    self.eventoProximoCliente()

    corridas = 0
    while (corridas < 50):
      #	2) saca el proximo evento de la bolsa de eventos
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
          
          
#--------------------------------- SERVIDOR -----------------------------------------------------------------------	
#Cajas	
#fTasaAtencionServidor (para cada caja es distinto) = cantidad de clientes que puede atender por unidad de tiempo (este valor se pasa a la exponencial como lamda)
class Servidor:

  def __init__(self,fTasaAtencionServidor):
    # inicializa variables
    self.ocupado = False
    self.tasaAtencion = fTasaAtencionServidor	 #Va a ser el parámetro de la exponencial, y nos dirá cuanto tiempo demorará en atender a dicho cliente
    

  def estaOcupado(self):
    # flag: devuelve "true" si el servidor esta ocupado, y "false" si no
    return self.ocupado   
	
  def inicioAtencion(self, fTiempoGlobal,cCliente):   
	  # setea el servidor en "ocupado"
    self.ocupado = True
	  # setea el tiempo de inicio atencion del cliente
    self.clienteActual=cCliente
    self.clienteActual.setTiempoInicioAtencion(fTiempoGlobal)
    # crea y devuelve el EventoFinAtencion                                               
    tiempoFinAtencion = distribucionExponencial(self.tasaAtencion) + fTiempoGlobal   
    eventoFin = EventoFinAtencion(tiempoFinAtencion,self)  
    return eventoFin                        
    
  def finAtencion(self,fTiempo):
	  # callback para EventoFinAtencion.procesar
	  # setea el tiempo de salida del cliente
    self.clienteActual.setTiempoSalida(fTiempo)
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
lamda = 2
lstSistema = [0.2, 0.3, 0.7] #contiene las distintas tasa de atencion de clientes de cada caja (servidor)
sistema = Sistema(lamda,lstSistema)
sistema.procesar()
print("PASO TODOS LOS METODOS")
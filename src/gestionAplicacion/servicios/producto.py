
import random

class Producto():
    def __init__(self, nombre = "", tamaño = "", tipoProducto = "", precio = 0.0, cantidad = 0, genero = "", sucursalSede = None) :
        self._genero=genero
        self._nombre=nombre
        self._precio=precio
        self._tamaño=tamaño
        self._tipoProducto=tipoProducto
        self._cantidad=cantidad
        self._valoracionComida=4.0
        self._sucursalSede=sucursalSede
        self._totalEncuestasDeValoracionRealizadasComida=25
        self._strikeCambio = False

    def comprobarBonoEnOrden(self, servicio):
        for producto in servicio.getOrden():
            if producto.getNombre() == self._nombre and producto.getTamaño() == self._tamaño and producto.getPrecio() > 0:
               return True 
        return False
    
	#Description: Este metodo se encarga de generar un codigo aleatorio para los bonos creados.
	#param longitud :  se pasa el como parametro la longitud que se desea el codigo
	#@return <b>Bono</b> :  Se retorna el bono creado
	
    def generarCodigoAleatorio(longitud):
     caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
     codigo = ''.join(random.choice(caracteres) for _ in range(longitud))
     return codigo
    

    #Description: Este metodo se encarga de revisar que un producto tenga unidades disponibles en el inventario, 
	#ya que con esto se hace una evaluacion a si unaproducto es apta para calificar o no.

    def verificarInventarioProducto(self):
        if len(self.inventarioCine) <= len(self.tiposDeMembresia):
            return False
        else:
            return True
        
    @classmethod
    def obtenerProductosPorNombre(cls, nombreProducto, productos):

       
        
        filtroPeliculasMismoNombre = []

        for producto in productos:
            if producto._nombre == nombreProducto:
                filtroPeliculasMismoNombre.append(producto)
        
        return filtroPeliculasMismoNombre

    def getGenero(self):
        return self._genero

    def setGenero(self, genero):
        self._genero = genero

    def getNombre(self):
        return self._nombre

    def setNombre(self, nombre):
        self._nombre = nombre

    def getPrecio(self):
        return self._precio

    def setPrecio(self, precio):
        self._precio = precio

    def getTamaño(self):
        return self._tamaño

    def setTamaño(self, tamaño):
        self._tamaño = tamaño

    def getTipoProducto(self):
        return self._tipoProducto

    def setTipoProducto(self, tipoProducto):
        self._tipoProducto = tipoProducto

    def getCantidad(self):
        return self._cantidad

    def setCantidad(self, cantidad):
        self._cantidad = cantidad

    def getValoracionComida(self):
        return self._valoracionComida

    def setValoracionComida(self, valoracionComida):
        self._valoracionComida = valoracionComida

    def getSucursalSede(self):
        return self._sucursalSede

    def setSucursalSede(self, sucursalSede):
        self._sucursalSede = sucursalSede

    def getTotalEncuestasDeValoracionRealizadasComida(self):
        return self._totalEncuestasDeValoracionRealizadasComida

    def setTotalEncuestasDeValoracionRealizadasComida(self, totalEncuestasDeValoracionRealizadasComida):
        self._totalEncuestasDeValoracionRealizadasComida = totalEncuestasDeValoracionRealizadasComida

    def getStrikeCambio(self):
        return self._strikeCambio

    def setStrikeCambio(self, strikeCambio):
        self._strikeCambio = strikeCambio



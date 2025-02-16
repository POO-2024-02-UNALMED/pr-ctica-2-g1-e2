import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Añadir el directorio raíz del proyecto al PYTHONPATH
#project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#if project_root not in sys.path:
#    sys.path.insert(0, project_root)



import tkinter as tk
import random
from gestionAplicacion.servicios.bono import *
from tkinter import ttk, messagebox
from datetime import datetime, time, timedelta
from gestionAplicacion.usuario.tipoDocumento import TipoDocumento
from gestionAplicacion.sucursalCine import SucursalCine
from gestionAplicacion.usuario.cliente import Cliente
from gestionAplicacion.servicios.herencia.servicioComida import ServicioComida
from gestionAplicacion.servicios.herencia.servicioSouvenirs import ServicioSouvenir
from gestionAplicacion.servicios.herencia.servicio import Servicio 
from gestionAplicacion.servicios.producto import Producto
from gestionAplicacion.proyecciones.pelicula import Pelicula
from gestionAplicacion.proyecciones.salaCine import SalaCine
from gestionAplicacion.usuario.membresia import Membresia
from gestionAplicacion.usuario.metodoPago import MetodoPago
from excepciones.uiExceptions import UiEmptyValues, UiDefaultValues
from excepciones.pagosExceptions import PagoSinCompletar, CerrarPago
from excepciones.timeExceptions import ExpiredMembershipException, NoMoreFilmsException
from excepciones.errorAplicacion import ErrorAplicacion
from gestionAplicacion.usuario.tarjetaCinemar import TarjetaCinemar
from gestionAplicacion.servicios.arkade import Arkade
from gestionAplicacion.usuario.ticket import Ticket
from baseDatos.serializador import Serializador
from baseDatos.deserializador import Deserializador
from gestionAplicacion.servicios.bono import Bono

class FieldFrame(tk.Frame):

    _clienteProceso = None
    _frameMenuPrincipal = None
    _framesFuncionalidades = []

    def __init__(self, tituloProceso='', descripcionProceso='', tituloCriterios = "", textEtiquetas = "", tituloValores = "", infoElementosInteractuables = None, habilitado = None, botonVolver = False, desplazarBotonesFila = 0, frameAnterior = None):
        super().__init__(ventanaLogicaProyecto)
        self._tituloCriterios = tituloCriterios
        self._infoEtiquetas = textEtiquetas
        self._tituloValores = tituloValores
        self._infoElementosInteractuables = infoElementosInteractuables
        self._habilitado = habilitado

        self._elementosInteractivos = []
        self._frameAnterior = frameAnterior
        
        self.config(bg = "#F0F8FF")
        ventanaLogicaProyecto.config(bg= "#F0F8FF")
        tituloFrame = tk.Label(self, text=tituloProceso, font= ("courier new",27, "bold italic"), anchor="center", bg="#F0F8FF")
        tituloFrame.grid(row=0, column=0, columnspan=4, sticky='we')

        descripcionFrame = tk.Label(self, text=descripcionProceso, font= ("courier new",10), anchor="center", wraplength=500, bg = "#F0F8FF")
        descripcionFrame.grid(row=1, column=0, columnspan=4, sticky='we')

        tituloCrit = tk.Label(self, text = tituloCriterios, font= ("courier new",15, "bold"), anchor="center", bg = "#F0F8FF")
        tituloCrit.grid(column=0, row=2, padx = (10,10), pady = (10,10))

        tituloVal = tk.Label(self, text = tituloValores, font= ("courier new",15, "bold"), anchor="center", bg = "#F0F8FF")
        tituloVal.grid(column=1, row=2, padx = (10,10), pady = (10,10))

####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################

        for i in range(len(textEtiquetas)):

            labelCriterio = tk.Label(self, text = textEtiquetas[i], font= ("courier new",12), anchor="center", bg = "#F0F8FF")
            labelCriterio.grid(column=0, row=i+3, padx = (10,10), pady = (10,10))

            elementoInteractivo = None

            if infoElementosInteractuables[i] is None:
                elementoInteractivo = tk.Entry(self)
            
            elif len(infoElementosInteractuables[i]) == 1:
                elementoInteractivo = tk.Entry(self)
                elementoInteractivo.insert(0, infoElementosInteractuables[i][0])

            else:
                elementoInteractivo = ttk.Combobox(self, values=infoElementosInteractuables[i][0])
                elementoInteractivo.set(infoElementosInteractuables[i][1])


            elementoInteractivo.grid(column=1, row=i+3,columnspan=1, padx = (10,10), pady = (10,10))

            if not habilitado[i]:

                if isinstance(elementoInteractivo, ttk.Combobox):
                    elementoInteractivo.configure(state='readonly')
                else:
                    elementoInteractivo.configure(state='disabled')

            self._elementosInteractivos.append(elementoInteractivo)

        if botonVolver:
            frameBotones = tk.Frame(self, bg = "#F0F8FF" )

            tk.Button(frameBotones, text="Aceptar", font = ("courier new", 12), fg = "black", bg = "#87CEFA",command=self.funAceptar,
            width=12,height=2).grid(pady = (10,10), padx=(20, 20), column = 0, row = len(self._infoEtiquetas)+3, sticky = 'we')
            tk.Button(frameBotones, text="Volver", font = ("courier new", 12), fg = "black", bg = "#87CEFA", command=self.funVolver,
            width=12,height=2).grid(pady = (10,10), padx=(20, 20), column = 1, row = len(self._infoEtiquetas)+3, sticky = 'we')
            tk.Button(frameBotones, text="Borrar", font = ("courier new", 12), fg = "black", bg = "#87CEFA",command=self.funBorrar,
            width=12,height=2).grid(pady = (10,10), padx=(20, 20), column = 2, row = len(self._infoEtiquetas)+3, sticky = 'we')

            frameBotones.grid(column = 0, row = len(self._infoEtiquetas) + 3 + desplazarBotonesFila, columnspan=2, sticky='we')
        
        else:
            tk.Button(self, text="Borrar", font = ("courier new", 12), fg = "black", bg = "#87CEFA",command=self.funBorrar,
            width=12,height=2).grid(pady = (10,10), padx=(10,10), column = 1, row = len(self._infoEtiquetas)+3 + desplazarBotonesFila)
            tk.Button(self, text="Aceptar", font = ("courier new", 12), fg = "black", bg = "#87CEFA", command=self.funAceptar,
            width=12,height=2).grid(pady = (10,10), padx=(10,10), column = 0, row = len(self._infoEtiquetas)+3 + desplazarBotonesFila)

    def getValue(self, criterio):
        indice = self._infoEtiquetas.index(criterio)
        return self._elementosInteractivos[indice].get()

    def setValueEntry(self, criterio, valor):
        indice = self._infoEtiquetas.index(criterio)
        self._elementosInteractivos[indice].delete("0","end")
        self._elementosInteractivos[indice].insert(0, valor)
    
    def setValueComboBox(self, criterio):
        indice = self._elementosInteractivos.index(criterio)
        criterio.set(self._infoElementosInteractuables[indice][1])

    @classmethod
    def setFrameMenuPrincipal(cls, frameMenuPrincipal):
        FieldFrame._frameMenuPrincipal = frameMenuPrincipal

    @classmethod
    def getFrameMenuPrincipal(cls):
        return FieldFrame._frameMenuPrincipal

    def funBorrar(self):
        for elementoInteractivo in self._elementosInteractivos:
            if isinstance(elementoInteractivo, ttk.Combobox):
                self.setValueComboBox(elementoInteractivo)
            else:
                elementoInteractivo.delete("0","end")
    
    def evaluarExcepciones(self):
        try:
            valoresVacios = self.tieneCamposVacios()
            if len(valoresVacios) > 0:
                raise UiEmptyValues(valoresVacios)

            valoresPorDefecto = self.tieneCamposPorDefecto()
            if len(valoresPorDefecto) > 0:
                raise UiDefaultValues(valoresPorDefecto)
            
            return True
        
        except ErrorAplicacion as e:
            messagebox.showerror('Error', e.mostrarMensaje())
            return False
    
    def funAceptar(self):
        pass

    def funVolver(self):
        self._frameAnterior.mostrarFrame()
    
    def mostrarFrame(self):

        for widget in ventanaLogicaProyecto.winfo_children():

            if isinstance(widget, tk.Frame):
                widget.pack_forget()

        self.pack(expand=True)
    
    @classmethod
    def getClienteProceso(cls):
        return FieldFrame._clienteProceso
    
    @classmethod
    def setClienteProceso(cls, clienteProceso):
        FieldFrame._clienteProceso = clienteProceso

    @classmethod
    def getFramesFuncionalidades(cls):
        return FieldFrame._framesFuncionalidades
    
    @classmethod
    def setFramesFuncionalidades(cls, framesFuncionalidades):
        FieldFrame._framesFuncionalidades = framesFuncionalidades
    
    def tieneCamposPorDefecto(self):

        camposPorDefecto = []

        for i in range(0, len(self._infoElementosInteractuables)):

            valorPorDefecto = '' if self._infoElementosInteractuables[i] == None else self._infoElementosInteractuables[i][0] if len(self._infoElementosInteractuables[i]) == 1 else self._infoElementosInteractuables[i][1]

            if self.getValue(self._infoEtiquetas[i]) == valorPorDefecto:
                camposPorDefecto.append(self._infoEtiquetas[i])
        
        return camposPorDefecto
    
    def tieneCamposVacios(self):

        camposVacios = []

        for elemento in self._elementosInteractivos:

            if elemento.get() == '':
                camposVacios.append(self._infoEtiquetas[self._elementosInteractivos.index(elemento)])
        
        return camposVacios

    def getElementosInteractivos(self):
        return self._elementosInteractivos

    def logicaInicioProcesosFuncionalidades(self, clienteProceso):

        FieldFrame.setClienteProceso(clienteProceso)

        FieldFrame._frameMenuPrincipal = FrameVentanaPrincipal()

        self.refrescarFramesFuncionalidades()

        #Ejecutamos la lógica de la ventana del menú principal
        FieldFrame.getFrameMenuPrincipal().construirMenu()
        FieldFrame.getFrameMenuPrincipal().mostrarFrame()
    
    def refrescarFramesFuncionalidades(self):
        #Creación Frames funcionalidades
        framesFuncionalidades = [
            FrameFuncionalidad1(), # <_ Funcionalidad 1
            FrameFuncionalidad2(), # <- Funcionalidad 2
            FrameFuncionalidad3Calificaciones(), # <- Funcionalidad 3
            FrameZonaJuegos(), # <- funcionalidad 4
            FrameFuncionalidad5() # <- Funcionalidad 5
        ]

        #Setteamos los frames de las funcionalidades al atributo de clase
        FieldFrame.setFramesFuncionalidades(framesFuncionalidades)
    
    def getFrameAnterior(self):
        return self._frameAnterior

####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################
####################################################################################################

class FrameReclamoDeBonos(FieldFrame):
    def __init__(self, servicio):

        self._servicio=servicio
        self._sucursalActual = self._clienteProceso.getCineUbicacionActual()
        self._servicio._sucursalUbicacion = self._sucursalActual
        self._servicio.actualizarBonos()

        super().__init__(
            tituloProceso = "Bonos",
            descripcionProceso = "En este apartado podras reclamar los bonos que tenes asociados",
            textEtiquetas = ['Bonos Disponibles'],
            infoElementosInteractuables = [[servicio.mostrarBonos(self._servicio), "Seleccione un Producto"]],
            habilitado = [False],
        )

        tituloV = tk.Label(self, text = "Productos en tu orden:", font= ("courier new",14), anchor="center", bg = "#F0F8FF" )
        tituloV.grid(column=2, row=2, padx = (10,10), pady = (10,10))

        labelCriterio = tk.Label(self, text = servicio.mostrarOrden(),anchor="w", font= ("courier new",10), bg = "#F0F8FF" )
        labelCriterio.grid(row=3, column=2, sticky="w")

        agregarb = tk.Button(self,text="Agregar Producto", font = ("courier new", 12), fg = "black", bg = "#87CEFA",command=self.agregar,
        width=15,height=2).grid(pady = (10,10), padx=(10,10), column = 2, row = 4,)

    def agregar(self):
        condicion = True
        if self.evaluarExcepciones():
            nombreProducto = self._elementosInteractivos[0].get()
            for pro in self._servicio.getBonosCliente():
                nombrep = f"\n{pro.getProducto().getNombre()} {pro.getProducto().getTamaño()}"
                if nombrep == nombreProducto:
                    if len(self._servicio.getOrden()) !=0:
                        for p in self._servicio.getOrden():
                            nombre = f"\n{p.getNombre()} {p.getTamaño()}"
                            if nombre == nombreProducto and condicion:
                                if messagebox.askokcancel("Dialogo de confirmacion","Preciona aceptar para agregar el producto a la compra o presiona cancelar para descontarlo de la compra"):
                                    condicion=False
                                    self._servicio.agregarOrden(pro.getProducto())
                                    self._servicio.setBonosCliente([])
                                    self._servicio._sucursalUbicacion.getBonosCreados().remove(pro)
                                    FrameReclamoDeBonos(self._servicio).mostrarFrame()
                                else:
                                    condicion=False
                                    for i in range(0,len(self._servicio.getOrden())):
                                        if p == self._servicio.getOrden()[i]:
                                            self._servicio.getOrden()[i].setPrecio(self._servicio.getOrden()[i].getPrecio()-(self._servicio.getOrden()[i].getPrecio()/self._servicio.getOrden()[i].getCantidad()))
                                            self._servicio.setBonosCliente([])
                                            self._servicio._sucursalUbicacion.getBonosCreados().remove(pro)
                                            FrameReclamoDeBonos(self._servicio).mostrarFrame()
                    else:
                        self._servicio.agregarOrden(pro.getProducto())
                        self._servicio.setBonosCliente([])
                        self._servicio._sucursalUbicacion.getBonosCreados().remove(pro)
                        FrameReclamoDeBonos(self._servicio).mostrarFrame()

            if condicion:
                for pro in self._servicio.getBonosCliente():
                    condicion=False
                    self._servicio.agregarOrden(pro.getProducto())
                    self._servicio.setBonosCliente([])
                    self._servicio._sucursalUbicacion.getBonosCreados().remove(pro)
                    FrameReclamoDeBonos(self._servicio).mostrarFrame()
    
    def funAceptar(self):
        total = self._servicio.calcularTotal()
        self._servicio.setValorPedido(total)
        FramePasarelaDePagos(self.getFrameMenuPrincipal(),total,self._servicio).mostrarFrame()

class FrameGeneracionDeProductos(FieldFrame):
    def __init__(self, servicio):

        self._sucursalActual = self._clienteProceso.getCineUbicacionActual()
        servicio._sucursalUbicacion = self._sucursalActual

        self._servicio = servicio
        servicio.setCliente(self._clienteProceso)
        servicio.setInventario(servicio.actualizarInventario())

        super().__init__(
            tituloProceso = "Generacion de orden",
            descripcionProceso = "En este apartado podras seleccionar los productos que deseas comprar",
            tituloCriterios = "Criterio de la orden",
            textEtiquetas = ['Producto',"Cantidad"],
            tituloValores = "Datos de compra",
            infoElementosInteractuables = [[servicio.mostrarInventario(), "Seleccione un Producto"],None],
            habilitado = [False,True,True],
        )
        tituloV = tk.Label(self, text = "Productos en tu orden:", font= ("courier new",14, "bold"), anchor="center", bg = "#F0F8FF" )
        tituloV.grid(column=2, row=2, padx = (10,10), pady = (10,10))

        self._labelCriterio = tk.Label(self, text = "",anchor="w", font= ("courier new",10))
        self._labelCriterio.grid(row=3, column=2,rowspan=2, sticky="w")

        self._agregarb = tk.Button(self,text="Agregar Producto", font = ("courier new", 12), fg = "black", bg = "#87CEFA",command = self.agregar,
        width=15,height=2).grid(pady = (10,10), padx=(10,10), column = 2, row = 5,)

        self._eliminarb=None

        self.getElementosInteractivos()[0].grid_configure(sticky="we")
        
    def agregar(self):
        if self.evaluarExcepciones():
            nombreProducto = self._elementosInteractivos[0].get()
            n = 0
            for productos in self._servicio.getInventario():
                nombre = f"{productos.getNombre()} {productos.getTamaño()}"
                if nombre == nombreProducto:
                    if productos.getCantidad() >= int(self._elementosInteractivos[1].get()):
                        self._servicio.agregarOrden(self._servicio.hacerPedido(n ,int(self._elementosInteractivos[1].get()) ,self._clienteProceso.getCineUbicacionActual()))
                        self.mostrar()
                        self._eliminarb = tk.Button(self,text="Eliminar producto", font = ("Verdana", 12), fg = "white", bg = "gray",command = self.eliminar,
            width=15,height=2).grid(pady = (10,10), padx=(10,10), column = 1, row = 6)
                        break
                    else:
                        messagebox.showerror("Error",f"No hay suficiente cantidad de {productos.getNombre()} {productos.getTamaño()}, solo hay: {productos.getCantidad()}")
                        break
                n+=1
            self.funBorrar()
    
    def eliminar(self):
        if self.evaluarExcepciones():
            producto = self._servicio.hacerPedido(self.getElementosInteractivos()[0].current() ,int(self._elementosInteractivos[1].get()),self._clienteProceso.getCineUbicacionActual())
            cantidad = int(self._elementosInteractivos[1].get())

            for p in self._servicio.getOrden():

                if p.getNombre() == producto.getNombre() and p.getCantidad()>=cantidad and p.getTamaño() == producto.getTamaño():

                    if p.getCantidad()==cantidad:

                        self._servicio.getOrden().remove(p)
                        self._servicio.getInventario()[self.getElementosInteractivos()[0].current()].setCantidad( self._servicio.getInventario()[self.getElementosInteractivos()[0].current()].getCantidad() + (cantidad*2))
                    else:
 
                        p.setCantidad(p.getCantidad()-cantidad)
                        p.setPrecio(p.getPrecio()-(self._servicio.getInventario()[self.getElementosInteractivos()[0].current()].getPrecio()*cantidad))
                        self._servicio.getInventario()[self.getElementosInteractivos()[0].current()].setCantidad( self._servicio.getInventario()[self.getElementosInteractivos()[0].current()].getCantidad() + (cantidad*2))
                self.mostrar()
                self.funBorrar()

    def funAceptar(self):
        if len(self._servicio.getOrden()) > 0:
            productoDescuento = self._servicio.descuentarPorGenero(self._clienteProceso.getCineUbicacionActual())
            if productoDescuento != None:
                messagebox.showinfo("Descuento","🎉🎉Felicidades obtuviste un descuento 🎉🎉 \n Por comprar un producto del mismo genero que el tiket que compraste")
                productoDescuento.setPrecio(productoDescuento.getPrecio()*0.9)
        FrameReclamoDeBonos(self._servicio).mostrarFrame()
    def mostrar(self):
        self._labelCriterio.configure(text = self._servicio.mostrarOrden())

    
class FrameFuncionalidad2(FieldFrame):
    def __init__(self):

        self._sucursalActual = self._clienteProceso.getCineUbicacionActual()


        super().__init__(
            tituloProceso = "Generacion de orden",
            descripcionProceso = "En este apartado podras seleccionar el servicio que deseas para generar una orden",
            tituloCriterios = "Criterio servicio",
            textEtiquetas = ['Seleccione tipo de servicio'],
            tituloValores = "Dato servicio",
            infoElementosInteractuables = [[self._sucursalActual.mostrarServicios(), "Seleccione un servicio"]],
            habilitado = [False]
        )
        

    def funAceptar(self):
        if self.evaluarExcepciones():
            if len(self._sucursalActual.getServicios())>1:
                if self._elementosInteractivos[0].get() == "Servicio comida":
                    FrameGeneracionDeProductos(self._sucursalActual.getServicios()[0]).mostrarFrame()
                else:
                    FrameGeneracionDeProductos(self._sucursalActual.getServicios()[1]).mostrarFrame()
            else:
                FrameGeneracionDeProductos(self._sucursalActual.getServicios()[0]).mostrarFrame()

class FrameInicioSesion(FieldFrame):

    #Construimos el frame usando FieldFrame
    def __init__(self):
        super().__init__(
            tituloProceso = 'Iniciar Sesión',
            descripcionProceso = 'En este apartado gestionamos la lógica de inicio de sesión',
            tituloCriterios = "Criterios Ingreso", 
            textEtiquetas = ['Seleccionar Tipo D.I. :', 'Número D.I. :', 'Seleccionar Sucursal :'], 
            tituloValores = "Datos Ingreso", 
            infoElementosInteractuables = [[TipoDocumento.listadoTiposDeDocumentos(), 'Seleccionar D.I.'], None, [[sede.getUbicacion() for sede in SucursalCine.getSucursalesCine()], 'Seleccionar Sucursal']], 
            habilitado = [False, True, False]
        )
    
    def funAceptar(self):

        #Evaluamos las excepciones de UI
        if self.evaluarExcepciones():

            #Obtenemos el tipo de documento ingresado
            tipoDocumentoSeleccionado = self.getValue('Seleccionar Tipo D.I. :')

            #obtenemos el numero de documento ingresado y evaluamos si es de tipo int
            try:
                numDocumentoSeleccionado = int(self.getValue('Número D.I. :'))
            except ValueError:
                messagebox.showerror('Error', f'El campo {self._infoEtiquetas[1].strip(':')}debe ser numérico')
                return

            #Obtenemos la sucursal seleciconada
            sucursalSeleccionada = self.getValue('Seleccionar Sucursal :')
            indiceSucursal = self.getElementosInteractivos()[2].current()
            sucursalProceso = SucursalCine.getSucursalesCine()[indiceSucursal]
            
            #Confirmamos las elecciones hechas por el usuario
            confirmacionUsuario = messagebox.askokcancel('Confirmación de datos', f'Los datos ingresados son:\nTipo de documento: {tipoDocumentoSeleccionado}\nNúmero de documento: {numDocumentoSeleccionado}\nSucursal seleccionada: {sucursalSeleccionada}')
            
            if confirmacionUsuario:
                #Evaluamos si es la primera vez que visita nuestro cine
                clienteProceso = SucursalCine.buscarCliente(numDocumentoSeleccionado, tipoDocumentoSeleccionado)

                if clienteProceso is None:
                    #Si es la primera vez, nos dirigimos al frame de crear usuario para crearlo
                    FrameCrearUsuario(tipoDocumentoSeleccionado, numDocumentoSeleccionado, sucursalProceso).mostrarFrame()
                elif type(clienteProceso) == str:
                    #Detectamos que el número de documento ya se encuentra asignado a otro cliente
                    messagebox.showerror('Error', 'Hemos detectado que este número de documento se encuentra asociado a otro cliente, por favor verifica el tipo o número de documento digitado.')
                else:
                    #En caso de que no, ingresamos al menú principal de nuestro cine
                    messagebox.showinfo('Inicio de sesión exitoso', f'{clienteProceso.getNombre()}, Bienvenid@ a cinemar sede {sucursalSeleccionada}')
                    clienteProceso.setCineUbicacionActual(sucursalProceso)
                    self.logicaInicioProcesosFuncionalidades(clienteProceso)


class FrameCrearUsuario(FieldFrame):

    #Construimos el frame usando FieldFrame
    def __init__(self, tipoDocumentoSeleccionado, numDocumentoSeleccionado, sucursalSeleccionada):

        super().__init__(
            tituloProceso = 'Crear Usuario', 
            descripcionProceso = 'Hemos detectado que es la primera vez que visitas nuestras sucursales, te invitamos a diligenciar el siguiente formulario de registro',
            tituloCriterios = 'Criterios registro',
            textEtiquetas = ['Nombre :', 'Edad :'],
            tituloValores = 'Datos registro',
            infoElementosInteractuables = [None, None],
            habilitado = [True, True]
            )
        
        #Guardamos los valores obtenidos en el inicio de sesión en vars de instancia
        self._tipoDocumentoCliente = tipoDocumentoSeleccionado
        self._numDocumentoCliente = numDocumentoSeleccionado
        self._sucursalActual = sucursalSeleccionada

        
    def funAceptar(self):

        #Evaluamos las excepciones
        if self.evaluarExcepciones():
            #Obtenemos el nombre ingresado
            nombreCliente = self.getValue('Nombre :')

            #Obtenemos la edad ingresada y verificamos si es de tipo int
            try:
                edadCliente = int(self.getValue('Edad :'))
            except ValueError:
                messagebox.showerror('Error', f'El campo {self._infoEtiquetas[1].strip(':')}debe ser numérico')
                return
            
            #Confirmamos las elecciones hechas por el ususario
            confirmacionCliente = messagebox.askokcancel('Confirmación datos', f'Los datos ingresados son:\nNombre: {nombreCliente}\nEdad: {edadCliente}')

            if confirmacionCliente:
                #Verificamos que tenga la edad mínima para ingresar al cine
                if edadCliente > 5:
                    #Verificamos que la edad ingresada sea apropiada para el documento seleccionado
                    if (self._tipoDocumentoCliente == TipoDocumento.CC.value and edadCliente >= 18) or (self._tipoDocumentoCliente == TipoDocumento.TI.value and edadCliente < 18) or (self._tipoDocumentoCliente == TipoDocumento.CE.value and edadCliente >= 18):
                        #Creamos el cliente y nos dirigimos al menú principal de nuestro cine
                        clienteCreado = Cliente(nombreCliente, edadCliente, self._numDocumentoCliente, [tipoDocumento for tipoDocumento in TipoDocumento if tipoDocumento.value == self._tipoDocumentoCliente][0], self._sucursalActual)
                        MetodoPago.asignarMetodosDePago(clienteCreado)
                        self.logicaInicioProcesosFuncionalidades(clienteCreado)
                    
                    else: 
                        messagebox.showerror('Error', 'Debes seleccionar una edad apropiada para el documento seleccionado anteriormente')
                
                else:
                    messagebox.showerror('Error', 'La edad mínima para acceder a nuestras instalaciones es de 5 años')      
                 
class FrameVentanaPrincipal(FieldFrame):

    def __init__(self):
        super().__init__( textEtiquetas = [] )

        self._imagenFramePrincipal = tk.PhotoImage(file = 'src/iuMain/imagenes/fachadaCine.png')
        
        self._labelImagen = tk.Label(self, image = self._imagenFramePrincipal)
        self._labelImagen.grid(row=0, column=0)



        FieldFrame.setFrameMenuPrincipal(self)



        #Se buscan los widget que tenga FieldFrame y se eliminan para este frame.
        for widget in self.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()
        
        self._barraMenuPrincipal = None
        self._menuArchivo = None
        self._menuProcesosConsultas = None
        self._menuAyuda = None

        self._clienteProceso = FieldFrame.getClienteProceso()

    def construirMenu(self):
        self._barraMenuPrincipal = tk.Menu(ventanaLogicaProyecto, font=("Times New Roman", 10))
        ventanaLogicaProyecto.config(menu=self._barraMenuPrincipal)
        self._menuArchivo = tk.Menu(self._barraMenuPrincipal, tearoff= 0, font=("Times New Roman", 10), activebackground= "light blue", activeforeground="black")
        self._menuProcesosConsultas = tk.Menu(self._barraMenuPrincipal, tearoff= 0, font=("Times New Roman", 10), activebackground= "light blue", activeforeground="black")
        self._menuAyuda = tk.Menu(self._barraMenuPrincipal, tearoff= 0, font=("Times New Roman", 10), activebackground= "light blue", activeforeground="black")

        self._barraMenuPrincipal.add_cascade(label="Archivo", menu=self._menuArchivo, font=("Times New Roman", 10))
        self._barraMenuPrincipal.add_cascade(label="Procesos y Consultas", menu= self._menuProcesosConsultas, font=("Times New Roman", 10))
        self._barraMenuPrincipal.add_cascade(label="Ayuda", menu= self._menuAyuda, font=("Times New Roman", 10))
        
        self._menuArchivo.add_command(label="Aplicación", command=self.mostrarDescripcionSistema)
        self._menuArchivo.add_command(label="Salir", command=self.mostrarVentanaInicio)

        self._menuProcesosConsultas.add_command(label = "Sistema proyecciones", command = self.ingresarFuncionalidad1)
        self._menuProcesosConsultas.add_command(label="Zona de juegos", command=self.ingresarFuncionalidad4)
        self._menuProcesosConsultas.add_command(label="Calificaciones", command=self.ingresarFuncionalidad3)
        self._menuProcesosConsultas.add_command(label="Servicio de comida/souvenir", command= self.ingresarFuncionalidad2)
        self._menuProcesosConsultas.add_command(label="Sistema de membresías", command=self.ingresarFuncionalidad5)

        self._menuAyuda.add_command(label="Acerca de", command=self.avanzarDia)
    
    def mostrarDescripcionSistema(self):
         messagebox.showinfo("Información del Sistema", "En este programa puedes:\n•Comprar Tickets\n•Comprar comida y regalos\n•Usar la zona de juegos\n•Adquirir membresias\n•Calificar nuestros servicios")
    
    def mostrarVentanaInicio(self):
        ventanaLogicaProyecto.withdraw()
        ventanaInicio.deiconify()

    def ingresarFuncionalidad1(self):
        FieldFrame.getFramesFuncionalidades()[0].mostrarFrame()
    
    def ingresarFuncionalidad2(self):
        FieldFrame.getFramesFuncionalidades()[1].mostrarFrame()

    def ingresarFuncionalidad3(self):
        FieldFrame.getFramesFuncionalidades()[2].mostrarFrame()    

    def ingresarFuncionalidad4(self): 
        FieldFrame.getFramesFuncionalidades()[3].mostrarFrame()

    def ingresarFuncionalidad5(self):
        FieldFrame.getFramesFuncionalidades()[4].mostrarFrame()

    def mostrarNombreAutores(self):
         messagebox.showinfo("Autores de la Aplicación", "• Juan José Gonzalez Morales - Alias: El Juanjo\n• Edinson Andrés Ariza Mendoza - Alias: Pana Andy\n• Rusbel Danilo Jaramillo Hincapie - Alias: El Indigente\n• Gerson Bedoya Hinestroza - Alias: El viejo Gerson\n• Santiago Castro Herrera - Alias: EL LuisMi")

    def logicaMembresia(self):

        SucursalCine.notificarFechaLimiteMembresia(self._clienteProceso)

        if self._clienteProceso.getMembresia() != None:

            diasRestantes = self.evaluarDiasRestantes()

            if diasRestantes < 6:
                try:
                    raise ExpiredMembershipException(diasRestantes)
                except ErrorAplicacion as e:
                    messagebox.showerror('Error', e.mostrarMensaje())

    def avanzarDia(self):

        #facilitamos el acceso a la sede y creamos una boolean de validación
        sucursalCineActual = FieldFrame.getClienteProceso().getCineUbicacionActual()
        sucursalCineActual.setFechaActual((sucursalCineActual.getFechaActual() + timedelta( seconds= 20 )))
        noHayHorariosPresentaciones = True

        #Iteramos sobre cada sala de cine, consultando si tiene horarios de películas en presentación
        for salaCine in sucursalCineActual.getSalasDeCine():
            if salaCine.tieneHorariosPresentacionHoy():
                noHayHorariosPresentaciones = False
                break
        
        if noHayHorariosPresentaciones:
            try:
                raise NoMoreFilmsException(self._clienteProceso.getCineUbicacionActual().getFechaActual())
            except ErrorAplicacion as e:
                messagebox.showerror('Error', e.mostrarMensaje())
            sucursalCineActual.setFechaActual((sucursalCineActual.getFechaActual() + timedelta( days = 1 )).replace(hour = SucursalCine.getInicioHorarioLaboral().hour, minute = SucursalCine.getInicioHorarioLaboral().minute)) #Inicio de la jornada laboral al otro día
    
        sucursalCineActual.avanzarTiempo() #Avanzamos el tiempo y ejecutamos lógica semenal o diaria según el caso
        self.logicaMembresia()
        self.refrescarFramesFuncionalidades() #Actualizamos los frames, ya que se han visto modificados por el avance de tiempo

    def getBarraMenuPrincipal(self):
        return self._barraMenuPrincipal

    def getMenuArchivo(self):

        return self._menuArchivo
    
    def getMenuProcesosConsultas(self):

        return self._menuProcesosConsultas

    def getMenuAyuda(self):
        return self._menuAyuda

    def evaluarDiasRestantes(self):
        #Se verifica si la fecha actual esta pasada a la fecha limite de la membresia.
        if (self._clienteProceso.getCineUbicacionActual().getFechaActual().date() >= self._clienteProceso.getFechaLimiteMembresia()):
            return 0

            
        #En caso de que falten 5 días o menos para que la membresía expire, se actualiza el mensaje con una advertencia.
        elif (self._clienteProceso.getCineUbicacionActual().getFechaActual().date() < self._clienteProceso.getFechaLimiteMembresia()):
            return (self._clienteProceso.getFechaLimiteMembresia() - self._clienteProceso.getCineUbicacionActual().getFechaActual().date()).days

###########################################################################################################################################

class FrameZonaJuegos(FieldFrame):
    
    

    def __init__(self):

        self.clienteProceso = FieldFrame.getClienteProceso()
        tituloProceso = 'Zona de Juegos\n'
        descripcionProceso ='En este espacio podras hacer uso de todos nuestros juegos y conseguir recompensas pagando con tu tarjeta cinemar, la cual podras adquirir y recargar en este mismo espacio.\n'
        botonVolver = True
        fecha = f'Fecha Actual : {FieldFrame.getClienteProceso().getCineUbicacionActual().getFechaActual().date()}\nHora actual : {FieldFrame.getClienteProceso().getCineUbicacionActual().getFechaActual().time().replace(microsecond = 0)}\n'

        super().__init__(
            tituloProceso = tituloProceso,
            descripcionProceso = descripcionProceso,
            botonVolver = botonVolver, 
            frameAnterior = FieldFrame.getFrameMenuPrincipal() 
        )


        #se destruyen todos los widgets creados por el init del padre
        for widget in self.winfo_children():

            widget.destroy()
        
        #se añaden widgets con el uso de canvas para dar mas estetica
        self._imagenFondo = tk.PhotoImage(file = 'src/iuMain/imagenes/ZonaJuegos.png')

        self.canvas =tk.Canvas(self, width=self._imagenFondo.width(), height=self._imagenFondo.height())
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self._imagenFondo)
        
        self.canvas.create_text(320, 100, text=tituloProceso, fill="black", font= ("Showcard Gothic",30))
        self.canvas.create_text(320, 200, text=descripcionProceso, fill="black", font= ("Lucida Console",15, "bold"), width=500)
        self.canvas.create_text(320, 310, text=fecha, fill="black", font= ("Lucida Console",15, "bold"))

        boton1 = tk.Button(self, text="Ingresar", font= ("Lucida Console",15, "bold"), fg = "black", bg = "light blue",command=self.funAceptar, width=12,height=2)
        boton2 = tk.Button(self, text="Volver", font= ("Lucida Console",15, "bold"), fg = "black", bg = "light blue", command=self.funVolver, width=12,height=2)
        
        self.canvas.create_window(230, 380, window=boton1, anchor="center")
        self.canvas.create_window(420, 380, window=boton2, anchor="center")
    
    #Metodo para el boton ingresar
    def funAceptar(self):
        if FieldFrame.getClienteProceso().verificarCuenta():
            FrameEleccion(self).mostrarFrame()
        else: 
            self.AlertaSinCuenta()

    #Metodo para mostrar alerta cuando el cliente no tiene cuenta
    def AlertaSinCuenta(self):

        mensaje = messagebox.askyesno("Sin Cuenta", "•No tienes una Tarjeta Cinemar asociada, ¿Deseas Adquirirla?  🤔 -> 💳❔")

        if mensaje:

            label_ids = [] #lista que almacena los label_ids

            #Se añaden al canvas para simular una cuenta regresiva con el for
            for i in range(5,0,-1):

                label = tk.Label(
                        self, 
                        text="Se le restará el precio de la tarjeta($5000) al saldo de su tarjeta. Redireccionando en " + str(i), 
                        font=("Lucida Console", 11, "bold"), 
                        width=500, 
                        fg="black", 
                        bg="sky blue", 
                        bd=2, 
                        relief="solid",
                        wraplength= 500
                        
                    )
                
                #Se añaden al canvas para simular una cuenta regresiva
                self.canvas.after(1500 * (5 - i), lambda lbl=label: label_ids.append(self.canvas.create_window(320, 450, window=lbl)))


            #Metodos para eliminar los labels creados
            def eliminar_labels():
                for label_id in label_ids:
                    self.canvas.delete(label_id)
                

                Arkade.asociarTarjetaCliente(self.clienteProceso)
                FrameTarjetaCinemar(self).mostrarFrame() 
                
            
            self.canvas.after(7500, eliminar_labels)
            
            
               

        else:
            label = tk.Label(
                        self, 
                        text="Recuerda que para Ingresar debes tener una Tarjeta Cinemar", 
                        font=("Lucida Console", 11, "bold"), 
                        width=500, 
                        fg="black", 
                        bg="sky blue", 
                        bd=2, 
                        relief="solid",
                        wraplength= 500
                        
                    )

            label_id = self.canvas.create_window(320, 450, window=label)

            # Usar lambda para eliminar el Label después de 5 segundos
            self.canvas.after(4000, lambda: self.canvas.delete(label_id))

class FrameTarjetaCinemar(FieldFrame):
    

    def __init__(self, frameAnterior):

        self.clienteProceso = FieldFrame.getClienteProceso()

        super().__init__(
                tituloProceso = 'Personalización Tarjeta Cinemar',
                descripcionProceso = 'En este espacio podras personalizar tu tarjeta cinemar a tu gusto\n',
                tituloCriterios = 'Criterios',
                textEtiquetas = ['Seleccione color de la tarjeta :', 'Seleccione fuente de la tarjeta :', 'Seleccione color de la fuente :'], 
                tituloValores = 'Elecciones',
                infoElementosInteractuables = [
                    [["coral","sky blue","lime green","gold" ,"fuchsia","violet","turquoise"], 'Color de la tarjeta'], 
                    [["Helvetica", "Arial", "Courier New", "Comic Sans MS", "Verdana", "Times New Roman", "Georgia"], 'Fuente de la tarjeta'], 
                    [["salmon", "light sea green", "medium orchid", "pale turquoise", "deep pink", "dodger blue", "light goldenrod yellow"], 'Color de la fuente']
                ],
                habilitado = [False, False, False],
                botonVolver = True,
                frameAnterior = frameAnterior
            )
        
        self.widgets = []
        
        for widget in self.winfo_children():

            self.widgets.append(widget)

        self.widgets[2].grid_configure(row=5, column=0)
        self.widgets[3].grid_configure(row=5, column=1)
        self.widgets[4].grid_configure(row=6, column=0)
        self.widgets[5].grid_configure(row=6, column=1)
        self.widgets[6].grid_configure(row=7, column=0)
        self.widgets[7].grid_configure(row=7, column=1)
        self.widgets[8].grid_configure(row=8, column=0)
        self.widgets[9].grid_configure(row=8, column=1)
        self.widgets[10].grid_configure(row=9, column=0, sticky = "we", columnspan = 4)

        tk.Button(self.widgets[-1], text="Ingresar", fg = "white", bg = "gray",command=self.funIngresar,
            ).grid(pady = (10,10), padx=(20, 20), column = 4, row = len(self._infoEtiquetas)+3, sticky = 'we')

        self.FrameTarjeta = tk.Frame(self, width=300, height=150)
        self.FrameTarjeta.grid(row =2, rowspan= 3, column= 0, columnspan= 4)

        self.canvas = tk.Canvas(self.FrameTarjeta, width=300, height=150)
        self.canvas.pack()

        # Crear la tarjeta con personalizaciones
        FrameTarjetaCinemar.crear_tarjeta(self.canvas, self.clienteProceso.getNombre() , self.clienteProceso.getCuenta().getSaldo(), self.clienteProceso._colorFondoTarjeta, 
                    (self.clienteProceso._fuenteTarjeta, 16, "bold italic"), (self.clienteProceso._fuenteTarjeta, 12), self.clienteProceso._colorTextoTarjeta)

       
        for i, widget in enumerate(self.widgets[-1].winfo_children()):
            
            if i ==0:
                widget.config(text = "Aplicar",font= ("courier new", 16, "bold"), width = 8, height = 1, bg = "#87CEFA", fg = "black")
            else: widget.config(font= ("courier new", 16, "bold"), width = 8, height = 1, bg = "#87CEFA", fg = "black")

        tamaños = [21,11,15,15,12,12,12,12,12,12]

        self.widgets[-1].config(bg = "#F0F8FF")
        self.widgets.pop(-1)
        
        for i, w in enumerate(self.widgets):
            if isinstance(w, ttk.Combobox):
                pass
            else:
                w.config(font = ("courier new", tamaños[i]), bg = "#F0F8FF")

        self.widgets[0].config(font = ("courier new", 21, "bold"))
        self.widgets[2].config(font = ("courier new", 15, "bold"))
        self.widgets[3].config(font = ("courier new", 15, "bold"))
        
        ventanaLogicaProyecto.config(bg= "#F0F8FF")
        self.config(bg= "#F0F8FF")   

    def funAceptar(self):

        valores = []
        if self.evaluarExcepciones():
            for comboBox in self.widgets:
                if isinstance(comboBox, ttk.Combobox):
                    valores.append(comboBox.get())

            if valores[0] != 'Color de la tarjeta':

                self.clienteProceso._colorFondoTarjeta = valores[0]

                FrameTarjetaCinemar.crear_tarjeta(self.canvas, self.clienteProceso.getNombre() , self.clienteProceso.getCuenta().getSaldo(), self.clienteProceso._colorFondoTarjeta, 
                    (self.clienteProceso._fuenteTarjeta, 16, "bold italic"), (self.clienteProceso._fuenteTarjeta, 12), self.clienteProceso._colorTextoTarjeta)
                

            if valores[1] != 'Fuente de la tarjeta':

                self.clienteProceso._fuenteTarjeta = valores[1]

                FrameTarjetaCinemar.crear_tarjeta(self.canvas, self.clienteProceso.getNombre() , self.clienteProceso.getCuenta().getSaldo(), self.clienteProceso._colorFondoTarjeta, 
                    (self.clienteProceso._fuenteTarjeta, 16, "bold italic"), (self.clienteProceso._fuenteTarjeta, 12), self.clienteProceso._colorTextoTarjeta)

            if valores[2] != 'Color de la fuente':

                self.clienteProceso._colorTextoTarjeta = valores[2]

                FrameTarjetaCinemar.crear_tarjeta(self.canvas, self.clienteProceso.getNombre() , self.clienteProceso.getCuenta().getSaldo(), self.clienteProceso._colorFondoTarjeta, 
                    (self.clienteProceso._fuenteTarjeta, 16, "bold italic"), (self.clienteProceso._fuenteTarjeta, 12), self.clienteProceso._colorTextoTarjeta)
    
    def funIngresar(self):
            FrameEleccion(self).mostrarFrame()

    def evaluarExcepciones(self):
        try:
            valoresPorDefecto = self.tieneCamposPorDefecto()
            if len(valoresPorDefecto) == 3:
                raise UiDefaultValues(valoresPorDefecto)
            
            return True
        
        except ErrorAplicacion as e:
            messagebox.showerror('Error', e.mostrarMensaje())
            return False

    # Función para crear la tarjeta en un Canvas
    @classmethod
    def crear_tarjeta(cls, canvas, nombre, saldo, color_fondo, fuente_titulo, fuente_texto, color_texto):
        # Tarjeta principal (rectángulo grande)
        canvas.create_rectangle(0, 0, 300, 150, fill=color_fondo, outline="black", width=3)

        # Borde decorativo
        canvas.create_rectangle(5, 5, 295, 145, outline="white", width=2)

        # Título de la tarjeta (con fuente y color personalizados)
        canvas.create_text(150, 30, text="Tarjeta Cinemar", font=fuente_titulo, fill=color_texto)

        # Espacio para el nombre del titular (con fuente y color personalizados)
        canvas.create_text(150, 60, text=f"Nombre: {nombre}", font=fuente_texto, fill=color_texto)

        # Espacio para el saldo (con fuente y color personalizados)
        canvas.create_rectangle(50, 80, 250, 120, fill=color_fondo, outline="black", width=2)
        canvas.create_text(150, 100, text=f"Saldo: {saldo}$", font=fuente_texto, fill=color_texto)

        #Código de barras (simulado)
        for i in range(18):
            # Dibuja cada barra con un ancho de 5 píxeles y espaciado de 10 píxeles
            x1 = 20 + i * 15  # Posición horizontal inicial y espaciado
            x2 = x1 + 5  # Ancho de la barra
            canvas.create_rectangle(x1, 125, x2, 145, fill="black")


class FrameEleccion(FieldFrame):

    def __init__(self, frameAnterior):

        self.clienteProceso = FieldFrame.getClienteProceso()

        super().__init__(
                tituloProceso = 'Servicios de Arkade',
                descripcionProceso = 'En este espacio podras escoger si:\n •Ir a jugar\n•Recargar tu tarjeta\n•Personalizar tu tarjeta',
                tituloCriterios = 'Criterios',
                textEtiquetas = ['Seleccione proceso a realizar :'], 
                tituloValores = ' Proceso',
                infoElementosInteractuables = [
                    [["Ingresar a los juegos","Recargar tarjeta Cinemar","Personalizar tarjeta Cinemar"], '                          Proceso'], 
                    
                ],
                habilitado = [False],
                botonVolver = True,
                frameAnterior = frameAnterior
            )
        
        self.widgets = []
        
        for widget in self.winfo_children():

            self.widgets.append(widget)

        self.widgets[-1].grid_configure(row=7, column=0, sticky = "we", columnspan = 4) 
        self.FrameTarjeta = tk.Frame(self, bg ="black", width=300, height=150)
        self.FrameTarjeta.grid(row = 4, rowspan= 3, column= 0, columnspan= 4)

        self.canvas = tk.Canvas(self.FrameTarjeta, width=300, height=150)
        self.canvas.pack()

        FrameTarjetaCinemar.crear_tarjeta(self.canvas, self.clienteProceso.getNombre() , self.clienteProceso.getCuenta().getSaldo(), self.clienteProceso._colorFondoTarjeta, 
                    (self.clienteProceso._fuenteTarjeta, 16, "bold italic"), (self.clienteProceso._fuenteTarjeta, 12), self.clienteProceso._colorTextoTarjeta)

        for widget in self.widgets[-1].winfo_children():
            
            widget.config(font= ("courier new", 16, "bold"), bg = "#87CEFA", fg = "black")

        tamaños = [21,12,15,15,12]

        self.widgets[-1].config(bg = "#F0F8FF")
        self.widgets.pop(-1)
        
        
        for i, w in enumerate(self.widgets):
            if isinstance(w, ttk.Combobox):
                w.config(width = 30)
            else:
                w.config(font = ("courier new", tamaños[i]), bg = "#F0F8FF")

        self.widgets[0].config(font = ("courier new", 21, "bold"))
        self.widgets[2].config(font = ("courier new", 15, "bold"))
        self.widgets[3].config(font = ("courier new", 15, "bold"))
        
        ventanaLogicaProyecto.config(bg= "#F0F8FF")
        self.config(bg= "#F0F8FF")   
    
    def funAceptar(self):

        self.valorComoBox = []

        if self.evaluarExcepciones():

            for w in self.widgets:
                if isinstance(w, ttk.Combobox):
                    self.valorComoBox.append(w.get())
            if self.valorComoBox[0] == "Ingresar a los juegos":
                FrameEleccionJuego(self).mostrarFrame()
            elif self.valorComoBox[0] == "Recargar tarjeta Cinemar":
                FrameRecargarTarjetaCinemar().mostrarFrame()
            elif self.valorComoBox[0] == "Personalizar tarjeta Cinemar":
                FrameTarjetaCinemar(FrameZonaJuegos()).mostrarFrame() 
    


class FrameEleccionJuego(FieldFrame):

    def __init__(self, frameAnterior):

        self.clienteProceso = FieldFrame.getClienteProceso()
        
        self.codigosDescuentoCliente = [self.clienteProceso.getCodigosDescuento()[:] , "                Codigo"] if len(self.clienteProceso.getCodigosDescuento()) != 0 else ['   😞Sin Codigos😞']
        
        if len(self.codigosDescuentoCliente) == 2 and "Ninguno" not in self.codigosDescuentoCliente[0]:
            self.codigosDescuentoCliente[0].insert(0, "Ninguno")
        self.generosJuegos = list(map(lambda game: game.getGeneroServicio(), SucursalCine.getJuegos()))
        

        super().__init__(
                tituloProceso = 'Juegos y categorias disponibles\n',
                descripcionProceso = 'En este espacio podrás escoger tu juego favorito y su categoria, ademas podrá redimir codigos de descuento(Solo aplica el descuento si juegas un juego de igual categoria al codigo que redimas)',
                tituloCriterios = 'Criterios',
                textEtiquetas = ['Unico Juego :', 'Seleccione la Categoria : ', 'Seleccione Codigo a redimir :'], 
                tituloValores = 'Juegos y Categorias',
                infoElementosInteractuables = [
                    ['      Hang Man'], 
                    [self.generosJuegos, "               Categoria"],
                    self.codigosDescuentoCliente
                ],
                habilitado = [False, False, False],
                botonVolver = True,
                frameAnterior = frameAnterior
            )

        self.widgets = []
        
        
        for widget in self.winfo_children():

            self.widgets.append(widget)

        for widget in self.widgets[-1].winfo_children():
            
            widget.config(font= ("courier new", 16, "bold"), bg = "#87CEFA", fg = "black")

        tamaños = [21,12,15,15,12,9,12,9,12,9]

        self.widgets[-1].config(bg = "#F0F8FF")
        self.widgets.pop(-1)
        
        
        for i, w in enumerate(self.widgets):
            if isinstance(w, ttk.Combobox):
                pass
            else:
                w.config(font = ("courier new", tamaños[i]), bg = "#F0F8FF")

        self.widgets[0].config(font = ("courier new", 21, "bold"))
        self.widgets[2].config(font = ("courier new", 15, "bold"))
        self.widgets[3].config(font = ("courier new", 15, "bold"))
        
        ventanaLogicaProyecto.config(bg= "#F0F8FF")
        self.config(bg= "#F0F8FF")

        labelrelleno = tk.Label(self, text="", bg="#F0F8FF")
        labelrelleno.grid(row=7, column=0, columnspan=3)

        self.labelPrecio = tk.Label(self, text="", font=("Courier New", 15, "bold italic"), bg="#F0F8FF")
        self.labelPrecio.grid(row=8, column=0, columnspan=3)

        self.comboBoxCategorias = self.getElementosInteractivos()[1]
        self.comboBoxCategorias.bind('<<ComboboxSelected>>', self.mostrarLabelPrecio)

        self.interactuableCodigosDescuento = self.getElementosInteractivos()[2]

        
        if isinstance(self.interactuableCodigosDescuento, ttk.Combobox):
            self.interactuableCodigosDescuento.bind('<<ComboboxSelected>>', self.mostrarLabelPrecioDescuento)
        

    def mostrarLabelPrecio(self, event):
            
        self.precio = 0

        for genero in self.generosJuegos:
            if genero == self.comboBoxCategorias.get():
                indice = self.generosJuegos.index(genero)
                self.precio = SucursalCine.getJuegos()[indice].getValorServicio()
                break
        self.labelPrecio.config(text= f"Precio: {self.precio}$")

        if isinstance(self.interactuableCodigosDescuento, ttk.Combobox) and self.interactuableCodigosDescuento.get() != "                Codigo" and self.interactuableCodigosDescuento.get() != "Ninguno":
            PrecionConDescuento = self.precio-self.precio*0.2
            if self.comboBoxCategorias.get() == Ticket.encontrarGeneroCodigoPelicula(self.interactuableCodigosDescuento.get()):
                    self.labelPrecio.config(text= f"Precio Anterior: {self.precio}$ -> Precio con Descuento: {PrecionConDescuento}$", font=("Courier New", 13, "bold italic"))
    
    def mostrarLabelPrecioDescuento(self, event):
        texto_label = ""

        
        if self.comboBoxCategorias.get() != "               Categoria":
            PrecionConDescuento = self.precio-self.precio*0.2
            if self.interactuableCodigosDescuento.get() != "Ninguno":
                if self.comboBoxCategorias.get() == Ticket.encontrarGeneroCodigoPelicula(self.interactuableCodigosDescuento.get()):
                    self.labelPrecio.config(text= f"Precio Anterior: {self.precio}$ -> Precio con Descuento: {PrecionConDescuento}$", font=("Courier New", 13, "bold italic"))
                else:
                    self.labelPrecio.config(text= f"Precio: {self.precio}$")
            else:
                self.labelPrecio.config(text= f"Precio: {self.precio}$")
    
    def funBorrar(self):

        for elementoInteractivo in self._elementosInteractivos:
            if isinstance(elementoInteractivo, ttk.Combobox):
                self.setValueComboBox(elementoInteractivo)
            else:
                elementoInteractivo.delete("0","end")
        
        self.labelPrecio.config(text= "")

    def tieneCamposPorDefecto(self):

        camposPorDefecto = []
        if isinstance(self.interactuableCodigosDescuento, ttk.Combobox):
            for i in range(1, len(self._infoElementosInteractuables)):

                valorPorDefecto = '' if self._infoElementosInteractuables[i] == None else self._infoElementosInteractuables[i][1]

                if self.getValue(self._infoEtiquetas[i]) == valorPorDefecto:
                    camposPorDefecto.append(self._infoEtiquetas[i])
            
            return camposPorDefecto
        else:
            for i in range(1, len(self._infoElementosInteractuables)-1):

                valorPorDefecto = '' if self._infoElementosInteractuables[i] == None else self._infoElementosInteractuables[i][1]

                if self.getValue(self._infoEtiquetas[i]) == valorPorDefecto:
                    camposPorDefecto.append(self._infoEtiquetas[i])
            
            return camposPorDefecto

    def funVolver(self):
        FrameEleccion(FrameZonaJuegos()).mostrarFrame()



    def funAceptar(self):
        if self.evaluarExcepciones():
             precio = 0
             indice = 0
             generoJuego = ""
             for genero in self.generosJuegos:
                if genero == self.comboBoxCategorias.get():
                    indice = self.generosJuegos.index(genero)
                    generoJuego = genero
                    precio = SucursalCine.getJuegos()[indice].getValorServicio()
                    break
             if isinstance(self.interactuableCodigosDescuento, ttk.Combobox):
                 if self.interactuableCodigosDescuento.get() == "Ninguno":
                    if self.clienteProceso.getCuenta().getSaldo() >= precio:
                        self.clienteProceso.getCuenta().hacerPago(precio)
                        messagebox.showinfo("Nuevo Saldo", f"El nuevo saldo de tu tarjeta es : {self.clienteProceso.getCuenta().getSaldo()}$")
                        
                        FrameJuego(SucursalCine.getJuegos()[indice].getPalabras(), generoJuego, False).mostrarFrame()#Linea para llamar al frame del juego
                    else: 
                        respuesta = messagebox.askyesno("Saldo Insuficiente", "No tienes saldo suficiente para continuar. ¿Desea ir a recargar la tarjeta?")
                        if respuesta:
                            #Linea para llamar al frame de recargar tarjeta
                            FrameRecargarTarjetaCinemar().mostrarFrame()

                 else:
                     if self.comboBoxCategorias.get() == Ticket.encontrarGeneroCodigoPelicula(self.interactuableCodigosDescuento.get()):
                         precio = precio -precio*0.2 
                         if self.clienteProceso.getCuenta().getSaldo() >= precio:
                            self.clienteProceso.getCuenta().hacerPago(precio)
                            self.clienteProceso.getCodigosDescuento().remove(self.interactuableCodigosDescuento.get())
                            messagebox.showinfo("Nuevo Saldo", f"El nuevo saldo de tu tarjeta es : {self.clienteProceso.getCuenta().getSaldo()}$")
                            FrameJuego(SucursalCine.getJuegos()[indice].getPalabras(), generoJuego, True).mostrarFrame()#Linea para llamar al frame del juego
                            

                         else: 
                            respuesta = messagebox.askyesno("Saldo Insuficiente", "No tienes saldo suficiente para continuar. ¿Desea ir a recargar la tarjeta?")
                            if respuesta:
                                #Linea para llamar al frame de recargar tarjeta
                                FrameRecargarTarjetaCinemar().mostrarFrame()

                     else:
                         messagebox.showerror("Error", "Has seleccionado un codigo con genero diferente al juego, por lo que no puedes redimirlo")
             else:
                 if self.clienteProceso.getCuenta().getSaldo() >= precio:
                        self.clienteProceso.getCuenta().hacerPago(precio)
                        messagebox.showinfo("Nuevo Saldo", f"El nuevo saldo de tu tarjeta es : {self.clienteProceso.getCuenta().getSaldo()}$")
                        
                        FrameJuego(SucursalCine.getJuegos()[indice].getPalabras(), generoJuego, False).mostrarFrame()#Linea para llamar al frame del juego
                 else: 
                    respuesta = messagebox.askyesno("Saldo Insuficiente", "No tienes saldo suficiente para continuar. ¿Desea ir a recargar la tarjeta?")
                    if respuesta:
                        #Linea para llamar al frame de recargar tarjeta
                        FrameRecargarTarjetaCinemar().mostrarFrame()
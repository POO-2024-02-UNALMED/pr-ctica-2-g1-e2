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
    
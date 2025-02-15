class ErrorAplicacion(Exception):
    
    def __init__(self, mensaje):
        super().__init__(mensaje)
        self._mensaje = f'Manejo de errores de la aplicación: {mensaje}'
    
    def mostrarMensaje(self):
        return self._mensaje
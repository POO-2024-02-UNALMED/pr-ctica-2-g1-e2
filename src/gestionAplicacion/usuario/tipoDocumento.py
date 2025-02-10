from enum import Enum

class TipoDocumento(Enum):
    
    CC = 'Cédula de Ciudadanía'
    TI = 'Tarjeta de Identidad'
    CE = 'Cédula de Extranjería'

    @classmethod
    def listadoTiposDeDocumentos(cls):
        return [tipoDocumento.value for tipoDocumento in TipoDocumento]
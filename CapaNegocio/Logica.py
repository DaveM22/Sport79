from CapaDatos.Datos import CatalogoArticulos,CatalogoDetalles,CatalogoStocks

class ControladorLocal():

    def __init__(self):
        self.articulosdata = CatalogoArticulos()
        self.detallesdata = CatalogoDetalles()
        self.movstockdata = CatalogoStocks()


    def getall_articulos(self):
        return self.articulosdata.getall_articulos()

    def nuevo_articulo(self,articulo):
        self.articulosdata.insert_articulo(articulo)

    def modificar_articulo(self,articulo):
        self.articulosdata.actualizar_articulo(articulo)

    def eliminar_articulo(self,ideliminar):
        self.articulosdata.eliminar_articulo(ideliminar)

    def getAllDetallesSinConfirmar(self):
        return self.detallesdata.getAllDetallesSinConfirmar()

    def sumAllDetallesSinConfimrar(self):
        return self.detallesdata.sumDetallesSinConfimrar()

    def asignarIDDetallesPendientes(self,id):
        self.detallesdata.asignarIDdetallesPendientes(id)

    def SetMovimientoStock(self,movstock):
        return self.movstockdata.setMovimientoStock(movstock)

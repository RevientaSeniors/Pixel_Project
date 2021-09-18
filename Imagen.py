class Imagen():
    def __init__(self, titulo, ancho, alto, filas, columnas, celdas, filtros):
        self.titulo = titulo
        self.ancho = ancho
        self.alto = alto
        self.filas = filas
        self.columnas = columnas
        self.celdas = celdas
        self.filtros = filtros

    def get_titulo(self):
        return self.titulo

    def set_titulo(self,titulo):
        self.titulo = titulo
    
    def get_ancho(self):
        return self.ancho

    def set_ancho(self,ancho):
        self.ancho = ancho

    def get_alto(self):
        return self.alto

    def set_alto(self,alto):
        self.alto = alto

    def get_filas(self):
        return self.filas

    def set_filas(self, filas):
        self.filas = filas

    def get_columnas(self):
        return self.columnas

    def set_columnas(self, columnas):
        self.columnas = columnas

    def get_celdas(self):
        return self.celdas

    def set_celdas(self, celdas):
        self.celdas = celdas

    def get_filtros(self):
        return self.filtros

    def set_filtros(self, filtros):
        self.filtros = filtros



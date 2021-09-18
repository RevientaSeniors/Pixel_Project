class Error():
        def __init__(self, descripcion, fila, columna):
                self.descripcion = descripcion
                self.fila = fila
                self.columna = columna

        def get_descripcion(self):
                return self.descripcion

        def set_descripcion(self, descripcion):
                self.descripcion = descripcion

        def get_fila(self):
                return self.fila

        def set_fila(self, fila):
                self.fila = fila

        def get_columna(self):
                return self.columna

        def set_columna(self, columna):
                self.columna = columna

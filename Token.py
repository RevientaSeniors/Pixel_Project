class Token():
    def __init__(self, tipo, lexema, fila, columna):
        self.tipo = tipo
        self.lexema = lexema
        self.fila = fila
        self.columna = columna

    def get_tipo(self):
        return self.tipo

    def set_tipo(self, tipo):
        self.tipo = tipo

    def get_lexema(self):
        return self.lexema

    def set_lexema(self, lexema):
        self.lexema = lexema

    def get_fila(self):
        return self.fila

    def set_fila(self, fila):
        self.fila = fila

    def get_columna(self):
        return self.columna

    def set_columna(self, columna):
        self.columna = columna
    
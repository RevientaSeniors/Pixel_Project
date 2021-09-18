from os import replace
from sre_constants import CATEGORY_UNI_LINEBREAK
import  tkinter
from typing import SupportsRound
from Token import Token
from Imagen import Imagen
from Error import Error
from tkinter.filedialog import askopenfilename
import re
#import imgkit

#imgkit.from_url('http://google.com', 'out.jpg')
#imgkit.from_file('test.html', 'out.jpg')
#imgkit.from_string('Hello!', 'out.jpg')
#imgkit.from_string('Hello!', 'out.jpg')
contenidoGlobal=[]
listaTokens=[]
listaErrores=[]
def crearVentanaMenu():
    #Crear la ventana
    ventanaMenu = tkinter.Tk()
    #Título de la ventana
    ventanaMenu.title("Menú")
    #Darle tamaño a la ventana pero lo comente porque la ventana agarra el tamaño del Frame
    #ventanaMenu.geometry("550x350")
    #Crear Frame, configurar tamaño.
    frame = tkinter.Frame()
    frame.config(width="550",height="350")
    #Dejar un tamaño fijo de la ventana
    ventanaMenu.resizable(0,0)
    #Crar Label
    label1 = tkinter.Label(frame,text="Menú principal")
    label1.place(x= 225 , y= 20)
    #Crear los botones
    botonCargarArchivo = tkinter.Button(frame,text="Cargar Archivo", command= bLeerArchivo)
    botonCargarArchivo.place(x=225,y=80)
    botonAnalizarArchivo = tkinter.Button(frame, text="Analizar Archivo", command= bAnalizarArchivo)
    botonAnalizarArchivo.place(x=225, y= 120)
    botonVerReporte = tkinter.Button(frame, text="Ver Reporte")
    botonVerReporte.place(x=225, y=160)
    botonSeleccionarImagen = tkinter.Button(frame, text="Seleccionar Imagen")
    botonSeleccionarImagen.place(x=225, y=200)
    botonVerImagen = tkinter.Button(frame, text="Ver Imagen")
    botonVerImagen.place(x=225,y=240)
    botonsalir = tkinter.Button(frame, text="Salir", command= bSalir)
    botonsalir.place(x=225,y=280)
    #Agregar el frame a la ventana
    frame.pack()
    #Mostar la ventana
    ventanaMenu.mainloop()

def bLeerArchivo():
    global contenidoGlobal
    fileName = askopenfilename()
    archivo = open(fileName, 'r')
    contenido = archivo.read()
    archivo.close()
    contenidoGlobal = contenido

def bAnalizarArchivo():
    global listaErrores
    global listaTokens
    global contenidoGlobal
    fila = 1
    columna = 1
    buffer ='' #almacenar el lexema
    centinela ='$'
    contenidoGlobal+=centinela
    estado = 0
    codigoSex=0
    #Automata

    i = 0
    while i < len(contenidoGlobal):
        caracterLeido = contenidoGlobal[i]
        if estado == 0:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
            if re.search('[A-Z]', caracterLeido):
                buffer+=caracterLeido
                columna+=1
            else:
                if buffer == 'TITULO':
                    listaTokens.append(Token('titulo',buffer, fila, columna))
                    buffer=''
                    i-=1
                    print("se encontro titulo")
                    estado  = 1
                elif buffer == 'ANCHO':
                    listaTokens.append(Token('ancho',buffer, fila, columna))
                    buffer=''
                    i-=1
                    estado  = 1
                elif buffer == 'ALTO':
                    listaTokens.append(Token('alto', buffer, fila, columna))
                    buffer=''
                    i-=1
                    estado  = 1
                elif buffer == 'FILAS':
                    listaTokens.append(Token('filas',buffer, fila, columna))
                    buffer=''
                    i-=1
                    estado  = 1
                elif buffer == 'COLUMNAS':
                    listaTokens.append(Token('columnas', buffer, fila, columna))
                    buffer=''
                    i-=1
                    estado  = 1
                elif buffer == 'CELDAS':
                    listaTokens.append(Token('celdas',buffer, fila, columna))
                    buffer=''
                    i-=1
                    estado  = 1
                elif buffer == 'FILTROS':
                    listaTokens.append(Token('filtros', buffer, fila, columna))
                    buffer=''
                    i-=1
                    estado  = 1
                    print("se encontro filtros")
                
        elif estado ==1:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
            elif caracterLeido == '=':
                buffer += caracterLeido
                listaTokens.append(Token('igual', buffer,fila,columna))
                columna+=1
                buffer=''
                estado = 2


        elif estado ==2:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
            elif caracterLeido == '"':
                buffer+=caracterLeido
                columna+=1
                estado = 3
            elif re.search('[0-9]', caracterLeido):
                buffer +=caracterLeido
                columna+=1
                estado = 6
            elif caracterLeido == '{':
                buffer +caracterLeido
                listaTokens.append(Token('llaveAbierta',buffer,fila, columna))
                columna+=1
                buffer = ''
                estado = 7
            elif re.search('[A-Z]', caracterLeido):
                 buffer+=caracterLeido
                 columna+=1
            else:
                if buffer == 'MIRRORX':
                    listaTokens.append(Token('mirrorx',buffer, fila, columna))
                    buffer=''
                    i-=1
                    estado  = 21
                elif buffer == 'MIRRORY':
                    listaTokens.append(Token('mirrory',buffer, fila, columna))
                    buffer=''
                    i-=1
                    estado  = 21
                elif buffer == 'DOUBLEMIRROR':
                    listaTokens.append(Token('doublem', buffer, fila, columna))
                    buffer=''
                    i-=1
                    estado  = 21


            
        elif estado ==3:
            if caracterLeido == '"':
                    buffer += caracterLeido
                    listaTokens.append(Token('cadena',buffer, fila, columna))
                    buffer = ''
                    columna += 1
                    estado=4
            else:
                buffer +=caracterLeido
                columna+=1

        elif estado ==4:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
            elif caracterLeido == ';':
                buffer += caracterLeido
                listaTokens.append(Token('puntocoma',buffer, fila, columna))
                buffer = ''
                columna += 1
                estado=5

        elif estado ==5:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
            elif caracterLeido == '@':
                buffer +=caracterLeido
                if buffer == '@@@@':
                    listaTokens.append(Token('separador',buffer,fila, columna))
                    buffer=''
                    estado=0
            elif caracterLeido != centinela:
                estado =0
                i-=1
            elif caracterLeido== centinela:
                print("se acepto la cadena")
            

        elif estado ==6:
            if re.search('[0-9]',caracterLeido):
                buffer +=caracterLeido
                columna+=1
            elif caracterLeido == ';':
                listaTokens.append(Token('entero',buffer, fila,columna))
                buffer=''
                buffer+=caracterLeido
                listaTokens.append(Token('puntocoma',buffer, fila, columna))
                buffer = ''
                columna += 1
                estado=5

        elif estado ==7:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
            elif caracterLeido == '[':
                buffer += caracterLeido
                listaTokens.append(Token('CorcheteAbierto', buffer, fila, columna))
                buffer =''
                columna +=1
                estado = 8
            
        elif estado ==8:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
            elif re.search('[0-9]',caracterLeido):
                buffer +=caracterLeido
                columna +=1
                estado = 9

        elif estado ==9:
            if re.search('[0-9]',caracterLeido):
                buffer += caracterLeido
                columna +=1
            elif re.search('\s',caracterLeido):
                listaTokens.append(Token('entero', buffer, fila, columna))
                buffer = ''
                buffer += caracterLeido
                listaTokens.append(Token('entero', buffer, fila, columna))
                buffer = ''
                estado = 10
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
            elif caracterLeido == ',':
                listaTokens.append(Token('entero', buffer, fila, columna))
                buffer = ''
                buffer += caracterLeido
                listaTokens.append(Token('coma', buffer, fila, columna))
                buffer = ''
                columna+=1
                estado = 11
            
            
        elif estado ==10:
            if re.search('\s', caracterLeido):
                columna+=1
            elif caracterLeido == ',':
                buffer += caracterLeido
                listaTokens.append(Token('coma', buffer, fila, columna))
                buffer = ''
                columna+=1
                estado = 11
                 
        elif estado == 11:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
            elif re.search('[0-9]',caracterLeido):
                buffer +=caracterLeido
                columna +=1
                estado = 12


        elif estado == 12:
            if re.search('[0-9]',caracterLeido):
                buffer = ''
                columna +=1
            elif re.search('\s',caracterLeido):
                listaTokens.append(Token('entero', buffer, fila, columna))
                buffer =''
                buffer += caracterLeido
                listaTokens.append(Token('entero', buffer, fila, columna))
                buffer = ''
                estado = 13
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
            elif caracterLeido == ',':
                listaTokens.append(Token('entero', buffer, fila, columna))
                buffer =''
                buffer += caracterLeido
                listaTokens.append(Token('coma', buffer, fila, columna))
                buffer = ''
                columna+=1
                estado = 14

        elif estado ==13:
            if re.search('\s', caracterLeido):
                columna+=1
            elif caracterLeido == ',':
                buffer += caracterLeido
                listaTokens.append(Token('coma', buffer, fila, columna))
                buffer = ''
                columna+=1
                estado = 14

        elif estado == 14:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
            if re.search('[A-Z]', caracterLeido):
                buffer+=caracterLeido
                columna+=1
            else:
                if buffer == 'TRUE' or buffer == 'FALSE':
                    listaTokens.append(Token('boleano',buffer, fila, columna))
                    buffer=''
                    i-=1
                    estado  = 15
            

        elif estado ==15:
            if re.search('\s', caracterLeido):
                columna+=1
            elif caracterLeido == ',':
                buffer += caracterLeido
                listaTokens.append(Token('coma', buffer, fila, columna))
                buffer = ''
                columna+=1
                estado = 16
        
        elif estado == 16:
            if re.search('#',caracterLeido):
                buffer += caracterLeido
                listaTokens.append(Token('sharp', buffer, fila, columna))
                buffer = ''
                columna+=1
                estado = 17
            
        elif estado == 17:
            if re.search('[A-F]', caracterLeido) or re.search('[a-f]', caracterLeido) or re.search('[0-9]', caracterLeido):
                codigoSex +=1
                buffer += caracterLeido
                columna+=1
                if codigoSex == 6:
                    listaTokens.append(Token('codigo', buffer, fila, columna))
                    buffer = ''
                    codigoSex = 0
                    estado = 18

        elif estado == 18:
                if caracterLeido == ']':
                    buffer += caracterLeido
                    listaTokens.append(Token('CorcheteCerrado', buffer, fila, columna))
                    buffer =''
                    columna +=1
                    estado = 19
        
        elif estado == 19:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
            elif caracterLeido == ',':
                buffer += caracterLeido
                listaTokens.append(Token('coma', buffer, fila, columna))
                buffer = ''
                columna+=1
                estado = 20
            elif caracterLeido =='}':
                buffer += caracterLeido
                listaTokens.append(Token('llaveCerrada', buffer, fila, columna))
                buffer =''
                columna +=1
                estado = 4

        elif estado == 20:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
            elif caracterLeido == '[':
                buffer += caracterLeido
                listaTokens.append(Token('CorcheteAbierto', buffer, fila, columna))
                buffer =''
                columna +=1
                estado = 8
            

        elif estado == 21:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
            elif caracterLeido == ';':
                buffer+=caracterLeido
                listaTokens.append(Token('puntocoma',buffer, fila, columna))
                buffer = ''
                estado=5
            elif re.search('[A-Z]', caracterLeido):
                 buffer+=caracterLeido
                 columna+=1
            else:
                if buffer == 'MIRRORX':
                    listaTokens.append(Token('mirrorx',buffer, fila, columna))
                    buffer=''
                    i-=1
                    estado  = 22
                elif buffer == 'MIRRORY':
                    listaTokens.append(Token('mirrory',buffer, fila, columna))
                    buffer=''
                    i-=1
                    estado  = 22
                elif buffer == 'DOUBLEMIRROR':
                    listaTokens.append(Token('doublem', buffer, fila, columna))
                    buffer=''
                    i-=1
                    estado  = 22
        
        elif estado == 22:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
            elif re.search('[A-Z]', caracterLeido):
                 buffer+=caracterLeido
                 columna+=1
            else:
                if buffer == 'MIRRORX':
                    listaTokens.append(Token('mirrorx',buffer, fila, columna))
                    buffer=''
                    i-=1
                    estado  = 23
                elif buffer == 'MIRRORY':
                    listaTokens.append(Token('mirrory',buffer, fila, columna))
                    buffer=''
                    i-=1
                    estado  = 23
                elif buffer == 'DOUBLEMIRROR':
                    listaTokens.append(Token('doublem', buffer, fila, columna))
                    buffer=''
                    i-=1
                    estado  = 23
                elif caracterLeido == ';':
                    buffer+=caracterLeido
                    listaTokens.append(Token('puntocoma',buffer, fila, columna))
                    buffer = ''
                    estado=5
    
        elif estado== 23:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
            elif caracterLeido == ';':
                buffer+=caracterLeido
                listaTokens.append(Token('puntocoma',buffer, fila, columna))
                buffer = ''
                estado=5
        i+=1

    #for i in range(len(listaTokens)):
        #print("Token: ", listaTokens[i].get_tipo())

def bSalir():
    exit()

if __name__ == '__main__':
    crearVentanaMenu()
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
listaImagenes=[]
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
                columna=1
            if re.search('[A-Z]', caracterLeido):
                buffer+=caracterLeido
                columna+=1
            else:
                if buffer == 'TITULO':
                    listaTokens.append(Token('titulo',buffer, fila, columna))
                    buffer=''
                    i-=1
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
                else:
                    buffer = caracterLeido
                    mandarAError(buffer, fila, columna)
                    buffer=''

                
        elif estado ==1:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
                columna =1
            elif caracterLeido == '=':
                buffer += caracterLeido
                listaTokens.append(Token('igual', buffer,fila,columna))
                columna+=1
                buffer=''
                estado = 2
            else:
                    buffer = caracterLeido
                    mandarAError(buffer, fila, columna)
                    buffer=''


        elif estado ==2:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
                columna =1
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
                else:
                    buffer = caracterLeido
                    mandarAError(buffer, fila, columna)
                    buffer=''


            
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
                columna =1
            elif caracterLeido == ';':
                buffer += caracterLeido
                listaTokens.append(Token('puntocoma',buffer, fila, columna))
                buffer = ''
                columna += 1
                estado=5
            else:
                buffer = caracterLeido
                mandarAError(buffer, fila, columna)
                buffer=''

        elif estado ==5:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
                columna =1
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
            else:
                buffer = caracterLeido
                mandarAError(buffer, fila, columna)
                buffer=''

        elif estado ==7:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
                columna =1
            elif caracterLeido == '[':
                buffer += caracterLeido
                listaTokens.append(Token('CorcheteAbierto', buffer, fila, columna))
                buffer =''
                columna +=1
                estado = 8
            else:
                buffer = caracterLeido
                mandarAError(buffer, fila, columna)
                buffer=''
            
        elif estado ==8:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
                columna =1
            elif re.search('[0-9]',caracterLeido):
                buffer +=caracterLeido
                columna +=1
                estado = 9
            else:
                buffer = caracterLeido
                mandarAError(buffer, fila, columna)
                buffer=''

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
                columna =1
            elif caracterLeido == ',':
                listaTokens.append(Token('entero', buffer, fila, columna))
                buffer = ''
                buffer += caracterLeido
                listaTokens.append(Token('coma', buffer, fila, columna))
                buffer = ''
                columna+=1
                estado = 11
            else:
                buffer = caracterLeido
                mandarAError(buffer, fila, columna)
                buffer=''
            
            
        elif estado ==10:
            if re.search('\s', caracterLeido):
                columna+=1
            elif caracterLeido == ',':
                buffer += caracterLeido
                listaTokens.append(Token('coma', buffer, fila, columna))
                buffer = ''
                columna+=1
                estado = 11
            else:
                buffer = caracterLeido
                mandarAError(buffer, fila, columna)
                buffer=''
                 
        elif estado == 11:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
                columna =1
            elif re.search('[0-9]',caracterLeido):
                buffer +=caracterLeido
                columna +=1
                estado = 12
            else:
                    buffer = caracterLeido
                    mandarAError(buffer, fila, columna)
                    buffer=''


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
                columna =1
            elif caracterLeido == ',':
                listaTokens.append(Token('entero', buffer, fila, columna))
                buffer =''
                buffer += caracterLeido
                listaTokens.append(Token('coma', buffer, fila, columna))
                buffer = ''
                columna+=1
                estado = 14
            else:
                    buffer = caracterLeido
                    mandarAError(buffer, fila, columna)
                    buffer=''

        elif estado ==13:
            if re.search('\s', caracterLeido):
                columna+=1
            elif caracterLeido == ',':
                buffer += caracterLeido
                listaTokens.append(Token('coma', buffer, fila, columna))
                buffer = ''
                columna+=1
                estado = 14
            else:
                    buffer = caracterLeido
                    mandarAError(buffer, fila, columna)
                    buffer=''

        elif estado == 14:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
                columna =1
            if re.search('[A-Z]', caracterLeido):
                buffer+=caracterLeido
                columna+=1
            else:
                if buffer == 'TRUE' or buffer == 'FALSE':
                    listaTokens.append(Token('boleano',buffer, fila, columna))
                    buffer=''
                    i-=1
                    estado  = 15
                else:
                    buffer = caracterLeido
                    mandarAError(buffer, fila, columna)
                    buffer=''
            

        elif estado ==15:
            if re.search('\s', caracterLeido):
                columna+=1
            elif caracterLeido == ',':
                buffer += caracterLeido
                listaTokens.append(Token('coma', buffer, fila, columna))
                buffer = ''
                columna+=1
                estado = 16
            else:
                    buffer = caracterLeido
                    mandarAError(buffer, fila, columna)
                    buffer=''
        
        elif estado == 16:
            if re.search('#',caracterLeido):
                buffer += caracterLeido
                listaTokens.append(Token('sharp', buffer, fila, columna))
                buffer = ''
                columna+=1
                estado = 17
            else:
                    buffer = caracterLeido
                    mandarAError(buffer, fila, columna)
                    buffer=''
            
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
            else:
                    buffer = caracterLeido
                    mandarAError(buffer, fila, columna)
                    buffer=''   

        elif estado == 18:
                if caracterLeido == ']':
                    buffer += caracterLeido
                    listaTokens.append(Token('CorcheteCerrado', buffer, fila, columna))
                    buffer =''
                    columna +=1
                    estado = 19
                else:
                    buffer = caracterLeido
                    mandarAError(buffer, fila, columna)
                    buffer=''
        
        elif estado == 19:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
                columna =1
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
            else:
                    buffer = caracterLeido
                    mandarAError(buffer, fila, columna)
                    buffer=''

        elif estado == 20:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
                columna =1
            elif caracterLeido == '[':
                buffer += caracterLeido
                listaTokens.append(Token('CorcheteAbierto', buffer, fila, columna))
                buffer =''
                columna +=1
                estado = 8
            else:
                    buffer = caracterLeido
                    mandarAError(buffer, fila, columna)
                    buffer=''
            

        elif estado == 21:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
                columna =1
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
                elif caracterLeido == ',':
                    buffer += caracterLeido
                    listaTokens.append(Token('coma', buffer, fila, columna))
                    buffer = ''
                    columna+=1
                else:
                    buffer = caracterLeido
                    mandarAError(buffer, fila, columna)
                    buffer=''
        
        elif estado == 22:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
                columna =1
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
                elif caracterLeido == ',':
                    buffer += caracterLeido
                    listaTokens.append(Token('coma', buffer, fila, columna))
                    buffer = ''
                    columna+=1
                elif caracterLeido == ';':
                    buffer+=caracterLeido
                    listaTokens.append(Token('puntocoma',buffer, fila, columna))
                    buffer = ''
                    estado=5
                else:
                    buffer = caracterLeido
                    mandarAError(buffer, fila, columna)
                    buffer=''
    
        elif estado== 23:
            if caracterLeido == '\s' or caracterLeido == '\t' :
                columna+=1
            elif caracterLeido == '\n':
                fila +=1
                columna =1
            elif caracterLeido == ';':
                buffer+=caracterLeido
                listaTokens.append(Token('puntocoma',buffer, fila, columna))
                buffer = ''
                columna+=1
                estado=5
            else:
                    buffer = caracterLeido
                    mandarAError(buffer, fila, columna)
                    buffer=''
        i+=1
    crearImagen()
    #for i in range(len(listaTokens)):
        #print("Token: ", listaTokens[i].get_tipo(), " Lexema: ", listaTokens[i].get_lexema(), " Fila: ", listaTokens[i].get_fila(), " Columna: ", listaTokens[i].get_columna()  )
    
    #for i in range(len(listaErrores)):
        #print(listaErrores[i].get_descripcion())

def bSalir():
    exit()

def mandarAError(buffer,fila, columna):
    listaErrores.append(Error('No se reconoció el caracter: '+buffer,fila,columna))

def crearImagen():
    global listaTokens
    global listaImagenes
    j=0
    i=0
    atributosCeldas=[]#[x,y,boolean,color]
    listaCeldas=[]
    listaFiltros=[]
    centi = False
    listaImagenes.append(Imagen('','','','','','',''))
    while i< len(listaTokens):
        token = listaTokens[i]
        
        if token.get_tipo() == "titulo":
            listaImagenes[j].set_titulo(listaTokens[i+2].get_lexema())
        elif token.get_tipo() == "ancho":
            listaImagenes[j].set_ancho(listaTokens[i+2].get_lexema())
        elif token.get_tipo() == "alto":
            listaImagenes[j].set_alto(listaTokens[i+2].get_lexema())
        elif token.get_tipo() == "filas":
            listaImagenes[j].set_filas(listaTokens[i+2].get_lexema())
        elif token.get_tipo() == "columnas":
            listaImagenes[j].set_columnas(listaTokens[i+2].get_lexema())
        elif token.get_tipo() == "llaveCerrada":
            centi=False
            listaImagenes[j].set_celdas(listaCeldas.copy())
            listaCeldas.clear()
        elif token.get_tipo() == "separador":
            listaImagenes[j].set_filtros(listaFiltros.copy())
            listaFiltros.clear()
            j+=1
            listaImagenes.append(Imagen('','','','','','',''))
        elif token.get_tipo() == "llaveAbierta" or centi== True:
            centi = True
            if token.get_tipo()== "entero" or token.get_tipo()=="boleano" or token.get_tipo()=="sharp" or token.get_tipo()=="codigo":
                atributosCeldas.append(listaTokens[i].get_lexema())
            elif token.get_tipo()=="CorcheteCerrado":
                listaCeldas.append(atributosCeldas.copy())
                atributosCeldas.clear()
        elif token.get_tipo()== "mirrorx" or token.get_tipo()== "mirrory" or token.get_tipo()== "doublem":
            listaFiltros.append(listaTokens[i].get_lexema())

        i+=1
    #print("El titulo de la imagen es: ", listaImagenes[0].get_titulo(), "\n El ancho es: ", listaImagenes[0].get_ancho(), "\n El alto es: ", listaImagenes[0].get_alto(), "\n las filas son: ", listaImagenes[0].get_filas(), "\n las columnas son: ", listaImagenes[0].get_columnas()  ) 
    #print("El titulo de la imagen es: ", listaImagenes[1].get_titulo(), "\n El ancho es: ", listaImagenes[1].get_ancho(), "\n El alto es: ", listaImagenes[1].get_alto(), "\n las filas son: ", listaImagenes[1].get_filas(), "\n las columnas son: ", listaImagenes[1].get_columnas()  )      
    #print("propiedades de la primera celda", listaImagenes[0].celdas[0])
    print("filtros de la primera imagen", listaImagenes[0].get_filtros())


#def crearHTML():




if __name__ == '__main__':
    crearVentanaMenu()
import  tkinter


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
    botonCargarArchivo = tkinter.Button(frame,text="Cargar Archivo")
    botonCargarArchivo.place(x=225,y=80)
    botonAnalizarArchivo = tkinter.Button(frame, text="Analizar Archivo")
    botonAnalizarArchivo.place(x=225, y= 120)
    botonVerReporte = tkinter.Button(frame, text="Ver Reporte")
    botonVerReporte.place(x=225, y=160)
    botonSeleccionarImagen = tkinter.Button(frame, text="Seleccionar Imagen")
    botonSeleccionarImagen.place(x=225, y=200)
    botonVerImagen = tkinter.Button(frame, text="Ver Imagen")
    botonVerImagen.place(x=225,y=240)
    botonsalir = tkinter.Button(frame, text="Salir")
    botonsalir.place(x=225,y=280)
    #Agregar el frame a la ventana
    frame.pack()
    #Mostar la ventana
    ventanaMenu.mainloop()

if __name__ == '__main__':
    crearVentanaMenu()
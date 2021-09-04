import  tkinter


def crearVentanaMenu():
    ventanaMenu = tkinter.Tk()
    ventanaMenu.title("Menú")
    ventanaMenu.geometry("550x350")
    ventanaMenu.resizable(0,0)
    label1 = tkinter.Label(ventanaMenu,text="Hola mundo")
    label1.pack()
    ventanaMenu.mainloop()


if __name__ == '__main__':
    crearVentanaMenu()
import Login as log
import Aplicacion as app
if __name__ == "__main__":
    app = app.Aplicacion() #tk
    login = log.Login(app) #toplevel
    app.withdraw()
    app.ventana = login

    app.mainloop()

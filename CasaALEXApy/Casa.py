import tkinter as tk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from io import BytesIO
from tkinter import ttk
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("credentials/iot-proyecto-final-be8fa-firebase-adminsdk-olx16-74669c93a5.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-proyecto-final-be8fa-default-rtdb.firebaseio.com/'
#tienen que descargar las credenciales desde cfierbase y poner la ruta de archivo en credentials.
})


def load_image_from_url(url, size):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize(size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)


def show_programmers():
    global root
    root = tk.Tk()

    frame0 = tk.Frame(root)
    frame0.pack(side=tk.TOP, pady=10)

    frame1 = tk.Frame(root)
    frame1.pack(side=tk.TOP, pady=10)

    frame2 = tk.Frame(root)
    frame2.pack(side=tk.TOP, pady=10)

    title = tk.Label(frame0, text="AlexaHome", font=("Arial", 20))
    title.pack(side=tk.TOP, pady=10)

    size = (50, 50)

    url1 = "https://lh3.googleusercontent.com/a/AGNmyxb5V6WLfiRQEJ2WKGnWem4lUg_bxiyEeUHEpC8a=s96-c-rg-br100"
    url2 = "https://lh3.googleusercontent.com/a-/ACB-R5SROFnbrjU0W_dtpPDt7Z8Y6DHZ9C7vErZN4OAs=s48-p"
    url3 = "https://lh3.googleusercontent.com/a-/ACB-R5QPSQtGLGqaF5BQT8NuJmuu-1S5_M1dzw9A9gSs=s48-p"

    image1 = load_image_from_url(url1, size)
    image2 = load_image_from_url(url2, size)
    image3 = load_image_from_url(url3, size)

    label1 = tk.Label(frame1, image=image1, text="Programador 1\nAlberto Encinas\nalberto.encinas@ucb.edu.bo", compound=tk.TOP)
    label1.pack(side=tk.LEFT, padx=10)

    label2 = tk.Label(frame1, image=image2, text="Programador 2\nCamila Negron\ncarla.negron@ucb.edu.bo", compound=tk.TOP)
    label2.pack(side=tk.LEFT, padx=10)

    label3 = tk.Label(frame1, image=image3, text="Programador 3\nGabriela Portugal\ngabriela.protugal@ucb.edu.bo", compound=tk.TOP)
    label3.pack(side=tk.LEFT, padx=10)

    url4 = "https://img.freepik.com/vector-gratis/casa-vista-superior_23-2147635902.jpg?w=740&t=st=1686251763~exp=1686252363~hmac=8056d7324ab6dcf0ebd74cecc57a5008667440665147103fbacd7fbc34389e45"
    size_big = (300, 300)
    image4 = load_image_from_url(url4, size_big)

    label4 = tk.Label(frame2, image=image4)
    label4.pack(side=tk.TOP, padx=10)
    button = tk.Button(root, text="Mostrar gráficas", command=show_graph)
    button.pack()

    root.mainloop()

def show_graph():
    # Crear la ventana principal
    root = tk.Tk()

    # Crear una cuadrícula de 2x2
    root.geometry("800x600")
    for i in range(2):
        root.rowconfigure(i, weight=1, minsize=300)
        root.columnconfigure(i, weight=1, minsize=300)

    for j in range(2):
        frame = tk.Frame(
            master=root,
            relief=tk.RAISED,
            borderwidth=1
        )
        frame.grid(row=i, column=j, padx=10, pady=10)

        # Obtener los datos de la tabla TablaHorno desde Firebase
        ref = db.reference('xd')
        result = ref.get()

        # Crear una gráfica de ejemplo
        fig, ax = plt.subplots()
        for key, value in result.items():
            hora = value['hora']
            focosala = value['focosala']
            enfriador = value['enfriador']
            set_point = value['set_point']
            sensor_lm35 = value['sensor_lm35']
            ax.plot(hora, focosala, label='focosala')
            ax.plot(hora, enfriador, label='Enfriador')
            ax.plot(hora, set_point, label='Set Point')
            ax.plot(hora, sensor_lm35, label='Sensor LM35')

        ax.legend()
        ax.set_xlabel('Hora Actual')
        ax.set_ylabel('Datos')
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    root.mainloop()


def main():
    show_programmers()
    show_graph()


if __name__ == "__main__":
    main()

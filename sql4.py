import tkinter as tk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from io import BytesIO
from tkinter import ttk
import requests
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate(r"C:\Users\ALBERTO\Desktop\pt\pythonProject\credentials\iot-proyecto-final-be8fa-firebase-adminsdk-olx16-8ad4f5efc5.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-proyecto-final-be8fa-default-rtdb.firebaseio.com/'
})

images = []
def load_image_from_url(url, size):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize(size, Image.ANTIALIAS)
    img_tk = ImageTk.PhotoImage(img)
    images.append(img_tk)
    return img_tk

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
    root = tk.Toplevel()
    root.title("Gráficas según tiempo")

    #back_button = tk.Button(root, text="Volver a programadores", command=show_programmers)
    back_button.pack(side=tk.TOP, pady=10)
    root.geometry("800x600")

    for i in range(2):
        root.rowconfigure(i, weight=1, minsize=300)
        root.columnconfigure(i, weight=1, minsize=300)


    ref = db.reference('casa-iot')
    result = ref.get()


    fig, ax = plt.subplots(2, 2, figsize=(10,10))


    time = []
    humedad = []
    temperatura = []
    #focos
    focosala = []
    fococ1=[]
    fococ2 = []
    fococ3 = []
    fococ4 = []

    ventilador = []

    for i, (key, value) in enumerate(result.items()):
        if 'Focos' in value and 'sala' in value['Focos'] and 'humedad' in value and 'temperatura' in value:

            time.append(i*5)  # asumimos que cada registro ocurre cada 5 minutos
            humedad.append(float(value['humedad']))
            temperatura.append(float(value['temperatura']))
            focosala.append(int(value['Focos']['sala']))
            fococ1.append(int(value['Focos']['cuarto1']))
            fococ2.append(int(value['Focos']['cuarto2']))
            fococ3.append(int(value['Focos']['cuarto3']))

            ventilador.append(int(value['ventilador']))

    ax[0, 0].plot(time, humedad, label='Humedad')
    ax[0, 0].set_xlabel('Tiempo (min)')
    ax[0, 0].set_ylabel('Humedad')
    ax[0, 0].legend()

    ax[0, 1].plot(time, temperatura, label='Temperatura')
    ax[0, 1].set_xlabel('Tiempo (min)')
    ax[0, 1].set_ylabel('Temperatura')
    ax[0, 1].legend()

    ax[1, 0].plot(time, focosala, label='Foco Sala')
    ax[1, 0].set_xlabel('Tiempo (min)')
    ax[1, 0].set_ylabel('Foco Sala')
    ax[1, 0].legend()
    ax[1, 0].plot(time, fococ1, label='fococ1')
    ax[1, 0].set_xlabel('Tiempo (min)')
    ax[1, 0].set_ylabel('fococ1')
    ax[1, 0].legend()
    ax[1, 0].plot(time, fococ2, label='fococ2')
    ax[1, 0].set_xlabel('Tiempo (min)')
    ax[1, 0].set_ylabel('fococ2')
    ax[1, 0].legend()
    ax[1, 0].plot(time, fococ3, label='fococ3')
    ax[1, 0].set_xlabel('Tiempo (min)')
    ax[1, 0].set_ylabel('fococ3')
    ax[1, 0].legend()

    ax[1, 1].plot(time, ventilador, label='Ventildor')
    ax[1, 1].set_xlabel('Tiempo (min)')
    ax[1, 1].set_ylabel('ventilador')
    ax[1, 1].legend()


    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    root.mainloop()



def main():
    show_programmers()

if __name__ == "__main__":
    main()
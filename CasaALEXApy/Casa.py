import tkinter as tk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from io import BytesIO
from tkinter import ttk
import requests
import mysql.connector
#import pyrebase


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="casa_iot"
)

def load_image_from_url(url, size):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize(size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)

def show_programmers():
    global root
    #root.destroy()
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

    show_graph_button = tk.Button(frame2, text="Mostrar gráfica", command=show_graph)
    show_graph_button.pack(side=tk.TOP, pady=10)
    show_table_button = tk.Button(frame1, text="Tabla", command=show_table)
    show_table_button.pack(side=tk.LEFT, padx=10)
    show_energy_info_button = tk.Button(frame2, text="Mostrar información de consumo energético",
                                        command=show_energy_info)
    show_energy_info_button.pack(side=tk.TOP, pady=10)

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

            # Obtener los datos de la tabla TablaHorno
            mycursor = mydb.cursor()
            mycursor.execute("SELECT hora, focosala, Enfriador, Set_Point, SensorLM35 FROM tablahorno")
            result = mycursor.fetchall()

            # Crear una gráfica de ejemplo
            fig, ax = plt.subplots()
            for row in result:
                hora = row[0]
                focosala = row[1]
                enfriador = row[2]
                set_point = row[3]
                sensor_lm35 = row[4]
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

def show_table():
    global root
    root.destroy()
    root = tk.Tk()

    frame = tk.Frame(root)
    frame.pack(side=tk.TOP, pady=10)

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM tablahorno")
    result = mycursor.fetchall()

    table_label = tk.Label(frame, text="Valores de la tabla TablaHorno", font=("Arial", 16))
    table_label.pack()

    cols = ('idcasa', 'fococ1', 'fococ2', 'fococ3', 'focosala', 'ventilador', 'humedad', 'temperatura', 'fecha', 'hora')
    listBox = ttk.Treeview(frame, columns=cols, show='headings')

    for col in cols:
        listBox.heading(col, text=col)

    for row in result:
        listBox.insert("", "end", values=row)

    listBox.pack()

    show_programmers_button = tk.Button(frame, text="Volver a programadores", command=show_programmers)
    show_programmers_button.pack(side=tk.TOP, pady=10)

    root.mainloop()

def show_energy_info():
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

            # Obtener los datos de la tabla TablaHorno
            mycursor = mydb.cursor()
            mycursor.execute("SELECT hora, focosala, ventilador, humedad, temperatura FROM funcionamiento")
            result = mycursor.fetchall()

            # Calcular la información de consumo energético
            total_energy = 0
            for row in result:
                calefactor = row[1]
                enfriador = row[2]
                total_energy += sum(calefactor) + sum(enfriador)

            info_label = tk.Label(frame, text=f"Consumo energético total: {total_energy} kWh", font=("Arial", 16))
            info_label.pack()

    root.mainloop()

show_programmers()

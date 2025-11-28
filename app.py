import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import LPR
import db

lpr = LPR.LPR()

placa_detectada = ""
pasos_proceso = {}

imagenes_proceso = {}  #Para evitar que las imágenes se borren por el garbage collector

def convertir_para_tk(img, tamaño=(240, 160)):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB) if len(img.shape) == 2 else cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_pil = img_pil.resize(tamaño)
    return ImageTk.PhotoImage(img_pil)

def cargar_imagen():
    global placa_detectada, pasos_proceso, imagenes_proceso

    archivo = filedialog.askopenfilename(
        filetypes=[("Imágenes", "*.png *.jpg *.jpeg")]
    )

    if archivo:
        img_cv = cv2.imread(archivo)

        placa_detectada, pasos_proceso = lpr.read_license(img_cv)

        lbl_placa.config(text=f"PLACA DETECTADA: {placa_detectada}")

        #Mostrar todos los pasos en la misma ventana
        filas = [
            ("Original", img_cv),
            ("Grises", pasos_proceso.get("1 - Grises")),
            ("Threshold", pasos_proceso.get("2 - Threshold")),
            ("Recorte", pasos_proceso.get("3 - Placa Recortada")),
            ("Final OCR", pasos_proceso.get("5 - Imagen Final OCR")),
        ]

        for i, (titulo, imagen) in enumerate(filas):
            if imagen is not None:
                img_tk = convertir_para_tk(imagen)
                imagenes_proceso[titulo] = img_tk

                labels_imagenes[i].config(image=img_tk)
                labels_titulos[i].config(text=titulo)

def guardar():
    nombre = entry_nombre.get()
    telefono = entry_telefono.get()
    direccion = entry_direccion.get()
    marca = entry_marca.get()
    modelo = entry_modelo.get()
    año = entry_año.get()

    if not placa_detectada or placa_detectada == "No license plate found":
        messagebox.showerror("Error", "Primero debes cargar una imagen válida.")
        return

    if not nombre or not marca:
        messagebox.showerror("Error", "Nombre y marca son obligatorios.")
        return

    db.guardar_datos(
        nombre, telefono, direccion,
        placa_detectada, marca, modelo, año
    )

    messagebox.showinfo("OK", "Datos guardados correctamente")

    entry_nombre.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)
    entry_marca.delete(0, tk.END)
    entry_modelo.delete(0, tk.END)
    entry_año.delete(0, tk.END)


# ------------------ INTERFAZ ------------------

ventana = tk.Tk()
ventana.title("Sistema de Detección de Placas")
ventana.geometry("1400x900")

btn_img = tk.Button(ventana, text="Cargar Imagen", command=cargar_imagen)
btn_img.pack(pady=10)

lbl_placa = tk.Label(ventana, text="PLACA DETECTADA:", font=("Arial", 14, "bold"))
lbl_placa.pack(pady=10)

# -------- CONTENEDOR DE PROCESO --------
frame_proceso = tk.Frame(ventana)
frame_proceso.pack()

labels_titulos = []
labels_imagenes = []

for i in range(5):
    lbl_t = tk.Label(frame_proceso, text="", font=("Arial", 10, "bold"))
    lbl_t.grid(row=0, column=i, padx=10)
    labels_titulos.append(lbl_t)

    lbl_i = tk.Label(frame_proceso)
    lbl_i.grid(row=1, column=i, padx=10)
    labels_imagenes.append(lbl_i)

# -------- FORMULARIO --------

tk.Label(ventana, text="Nombre del propietario").pack()
entry_nombre = tk.Entry(ventana, width=40)
entry_nombre.pack()

tk.Label(ventana, text="Teléfono").pack()
entry_telefono = tk.Entry(ventana, width=40)
entry_telefono.pack()

tk.Label(ventana, text="Dirección").pack()
entry_direccion = tk.Entry(ventana, width=40)
entry_direccion.pack()

tk.Label(ventana, text="Marca del vehículo").pack()
entry_marca = tk.Entry(ventana, width=40)
entry_marca.pack()

tk.Label(ventana, text="Modelo").pack()
entry_modelo = tk.Entry(ventana, width=40)
entry_modelo.pack()

tk.Label(ventana, text="Año").pack()
entry_año = tk.Entry(ventana, width=40)
entry_año.pack()

btn_guardar = tk.Button(ventana, text="Guardar Información", command=guardar)
btn_guardar.pack(pady=20)

ventana.mainloop()

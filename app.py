import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import LPR
import db

lpr = LPR.LPR()
placa_detectada = ""
imagenes_proceso = {}

def convertir_para_tk(img, tamaño=(240, 160)):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB) if len(img.shape) == 2 else cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_pil = img_pil.resize(tamaño)
    return ImageTk.PhotoImage(img_pil)

def cargar_imagen():
    global placa_detectada, imagenes_proceso

    archivo = filedialog.askopenfilename(
        filetypes=[("Imágenes", "*.png *.jpg *.jpeg")]
    )

    if archivo:
        img_cv = cv2.imread(archivo)
        placa_detectada, pasos_proceso = lpr.read_license(img_cv)

        lbl_placa.config(text=f"PLACA DETECTADA: {placa_detectada}")

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

    db.guardar_datos(
        nombre, telefono, direccion,
        placa_detectada, marca, modelo, año
    )

    messagebox.showinfo("OK", "Datos guardados correctamente")

def consultar():
    placa = entry_buscar.get().upper()

    resultado = db.consultar_por_placa(placa)

    if resultado:
        texto = f"""
Placa: {resultado[0]}
Marca: {resultado[1]}
Modelo: {resultado[2]}
Año: {resultado[3]}

Propietario: {resultado[4]}
Teléfono: {resultado[5]}
Dirección: {resultado[6]}
"""
        lbl_resultado.config(text=texto)
    else:
        lbl_resultado.config(text="Placa no encontrada")


# ------------------ INTERFAZ ------------------

ventana = tk.Tk()
ventana.title("Sistema de Detección de Placas")
ventana.geometry("1400x900")

tabs = ttk.Notebook(ventana)
tabs.pack(expand=1, fill="both")

# -------- TAB 1: REGISTRO --------

tab_registro = ttk.Frame(tabs)
tabs.add(tab_registro, text="Registrar Vehículo")

btn_img = tk.Button(tab_registro, text="Cargar Imagen", command=cargar_imagen)
btn_img.pack(pady=10)

lbl_placa = tk.Label(tab_registro, text="PLACA DETECTADA:", font=("Arial", 14, "bold"))
lbl_placa.pack(pady=10)

frame_proceso = tk.Frame(tab_registro)
frame_proceso.pack()

labels_titulos = []
labels_imagenes = []

for i in range(5):
    lbl_t = tk.Label(frame_proceso, text="")
    lbl_t.grid(row=0, column=i)
    labels_titulos.append(lbl_t)

    lbl_i = tk.Label(frame_proceso)
    lbl_i.grid(row=1, column=i)
    labels_imagenes.append(lbl_i)

tk.Label(tab_registro, text="Nombre").pack()
entry_nombre = tk.Entry(tab_registro)
entry_nombre.pack()

tk.Label(tab_registro, text="Teléfono").pack()
entry_telefono = tk.Entry(tab_registro)
entry_telefono.pack()

tk.Label(tab_registro, text="Dirección").pack()
entry_direccion = tk.Entry(tab_registro)
entry_direccion.pack()

tk.Label(tab_registro, text="Marca").pack()
entry_marca = tk.Entry(tab_registro)
entry_marca.pack()

tk.Label(tab_registro, text="Modelo").pack()
entry_modelo = tk.Entry(tab_registro)
entry_modelo.pack()

tk.Label(tab_registro, text="Año").pack()
entry_año = tk.Entry(tab_registro)
entry_año.pack()

btn_guardar = tk.Button(tab_registro, text="Guardar Información", command=guardar)
btn_guardar.pack(pady=20)

# -------- TAB 2: CONSULTA --------

tab_consulta = ttk.Frame(tabs)
tabs.add(tab_consulta, text="Consultar Vehículo")

tk.Label(tab_consulta, text="Ingrese placa a buscar").pack(pady=20)
entry_buscar = tk.Entry(tab_consulta)
entry_buscar.pack()

btn_buscar = tk.Button(tab_consulta, text="Buscar", command=consultar)
btn_buscar.pack(pady=10)

lbl_resultado = tk.Label(tab_consulta, text="", font=("Arial", 12))
lbl_resultado.pack(pady=20)

ventana.mainloop()

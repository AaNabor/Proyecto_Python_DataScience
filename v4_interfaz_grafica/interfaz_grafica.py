import tkinter as tk
from tkinter import messagebox # Para ventanas emergentes de alerta
from sistema_db import Estudiante, BaseDeDatos # Importamos tu lógica V3.0

# --- CLASE DE LA INTERFAZ ---
class EscuelaApp:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Estudiantes - Data Science")
        self.ventana.geometry("400x350")
        
        # Conexión a la BD (Backend)
        self.db = BaseDeDatos()

        # --- SECCIÓN 1: TÍTULO ---
        # Usamos 'pack' para ponerlo arriba centrado
        tk.Label(ventana, text="Registro de Alumnos", font=("Arial", 16, "bold")).pack(pady=10)

        # --- SECCIÓN 2: FORMULARIO (Frame) ---
        # Usamos un 'marco' para agrupar los campos
        marco = tk.Frame(ventana)
        marco.pack(pady=10)

        # Nombre
        tk.Label(marco, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.campo_nombre = tk.Entry(marco, width=30)
        self.campo_nombre.grid(row=0, column=1, padx=5, pady=5)

        # Edad
        tk.Label(marco, text="Edad:").grid(row=1, column=0, padx=5, pady=5)
        self.campo_edad = tk.Entry(marco, width=10)
        self.campo_edad.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Matrícula
        tk.Label(marco, text="Matrícula:").grid(row=2, column=0, padx=5, pady=5)
        self.campo_matricula = tk.Entry(marco, width=15)
        self.campo_matricula.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Notas
        tk.Label(marco, text="Notas (separadas por coma):").grid(row=3, column=0, padx=5, pady=5)
        self.campo_notas = tk.Entry(marco, width=30)
        self.campo_notas.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # --- SECCIÓN 3: BOTONES DE ACCIÓN ---
        # Botón Guardar
        btn_guardar = tk.Button(ventana, text="💾 Guardar en BD", bg="#4CAF50", fg="white", command=self.guardar_alumno)
        btn_guardar.pack(pady=5, fill=tk.X, padx=20)

        # Botón Exportar
        btn_exportar = tk.Button(ventana, text="📄 Exportar Reporte", bg="#2196F3", fg="white", command=self.exportar_reporte)
        btn_exportar.pack(pady=5, fill=tk.X, padx=20)
        
        # Etiqueta de estado (Status Bar)
        self.lbl_estado = tk.Label(ventana, text="Listo.", fg="grey", relief=tk.SUNKEN, anchor="w")
        self.lbl_estado.pack(side=tk.BOTTOM, fill=tk.X)

    # --- MÉTODOS DE LA INTERFAZ (Eventos) ---
    
    def guardar_alumno(self):
        # 1. Obtenemos datos de los campos
        nombre = self.campo_nombre.get()
        edad_texto = self.campo_edad.get()
        matricula = self.campo_matricula.get()
        notas_texto = self.campo_notas.get()

        # 2. Validaciones básicas
        if not nombre or not matricula or not edad_texto:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            # Convertimos edad a entero
            edad = int(edad_texto)
            
            # 3. CONECTAMOS CON LA LÓGICA (Backend)
            # Aquí se aplica el .strip() y .title() automáticamente gracias al constructor
            nuevo_alumno = Estudiante(nombre, edad, matricula)
            
            # 4. PROCESAMIENTO DE CADENAS (Data Cleaning)

            if notas_texto:
                try:
                    # 1. notas_texto.split(","): Rompe el texto donde haya comas: ["10", "8", "9"]
                    # 2. float(n): Convierte cada pedazo a número decimal.
                    lista_notas = [float(n) for n in notas_texto.split(",")]
            
                    # Usamos * para desempaquetar la lista y enviarla al método
                    nuevo_alumno.agregar_notas(*lista_notas)

                except ValueError:
                    messagebox.showwarning("Atención", "Las notas deben ser números separados por comas. Se guardó el alumno sin notas.")

            # 5. Guardamos en SQL
            self.db.guardar_estudiante(nuevo_alumno)
            
            # 6. Feedback al usuario
            self.lbl_estado.config(text=f"Guardado: {nuevo_alumno.nombre} | Promedio: {nuevo_alumno.promedio_actual: .2f}", fg="green")
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Estudiante y calificaciones registrados correctamente.")
            
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número")

    def exportar_reporte(self):
        # 1. Recuperamos los datos de la pantalla (igual que al guardar)
        nombre = self.campo_nombre.get()
        matricula = self.campo_matricula.get()

        # Validacion
        if not nombre or not matricula:
            messagebox.showwarning("Faltan datos", "Para exportar un reporte, ingrese al menos Nombre y Matrícula.")
            return
        
        # 2. Recreamos el objeto temporalmente solo para usar su método de exportar
        try:
            # Recuperamos edad (o ponemos 0 si está vacío, solo para el reporte)
            edad = int(self.campo_edad.get()) if self.campo_edad.get() else 0

            # Recuperamos notas
            notas_texto = self.campo_notas.get()

            alumno_temp = Estudiante(nombre, edad, matricula)

            if notas_texto:
                lista_notas = [float(n) for n in notas_texto.split(",")]
                alumno_temp.agregar_notas(*lista_notas)

            # 3. Llamamos al MÉTODO DEL BACKEND
            alumno_temp.exportar_boletin()

            messagebox.showinfo("Reporte Generado", f"Se creó el achivo 'boletin_{matricula}.txt' en la carpeta del proyecto.")

        except ValueError:
            messagebox.showerror("Error", "Revise que la edad y las notas sean números válidos.")

    def limpiar_campos(self):
        self.campo_nombre.delete(0, tk.END)
        self.campo_edad.delete(0, tk.END)
        self.campo_matricula.delete(0, tk.END)
        self.campo_notas.delete(0, tk.END)

# --- LANZADOR DE LA APP ---
if __name__ == "__main__":
    root = tk.Tk()
    app = EscuelaApp(root)
    root.mainloop()

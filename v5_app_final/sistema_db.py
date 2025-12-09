import sqlite3 # Importamos el motor de base de datos
from abc import ABC, abstractmethod

# --- CAPA DE DATOS (Lo nuevo: SQLite) ---
class BaseDeDatos:

    def __init__(self, nombre_archivo="escuela.db"):
        self.nombre_archivo = nombre_archivo
        self.conectar()
        
    def conectar(self):
        """Crea la tabla si no existe (Concepto del doc: CREATE TABLE)"""
        try:
            with sqlite3.connect(self.nombre_archivo) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS estudiantes (
                        matricula TEXT PRIMARY KEY,
                        nombre TEXT,
                        edad INTERGER,
                        promedio REAL
                )
            ''')
            print("--- Base de datos conectada correctamente ---")
        except sqlite3.Error as e:
              print(f"Error en la base de datos: {e}")

    def guardar_estudiante(self, estudiante):
        """Guarda o actualiza un objeto Estudiante en la BD (INSERT/REPLACE)"""
        try:
            with sqlite3.connect(self.nombre_archivo) as conn:
                cursor = conn.cursor()
                # Insertamos los datos del objeto
                cursor.execute('''
                    INSERT OR REPLACE INTO estudiantes (matricula, nombre, edad, promedio)
                    VALUES (?, ?, ?, ?)
                ''', (estudiante.matricula, estudiante.nombre, estudiante.edad, estudiante.promedio_actual))
                print(f"Guardado en BD: {estudiante.nombre}")
        except Exception as e:
            print(f"No se pudo guardar: {e}")

# --- CAPA LÓGICA ---
class Persona(ABC):
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

        @abstractmethod
        def mostrar_info(self):
            pass

class Estudiante(Persona):
    def __init__(self, nombre, edad, matricula):
        # --- DATA CLEANING ---
        # .strip() quita espacios sobrantes al inicio y al final
        # .ttile() pone la primera letra mayúscula (Juan Perez)
        # .upper() pone todo en mayúsculas (para matrículas estandarizadas)

        nombre_limpio = nombre.strip().title()
        matricula_limpia = matricula.strip().upper()

        super().__init__(nombre_limpio, edad)
        self.matricula = matricula_limpia
        self.__notas = []
        self.promedio_actual = 0.0 # Variable auxiliar para la BD

    def agregar_notas(self, *calificaciones):
        for nota in calificaciones:
            if 0 <= nota <= 10:
                self.__notas.append(nota)
        self._calcular_promedio()

    def _calcular_promedio(self):
        if self.__notas:
            self.promedio_actual = sum(self.__notas) / len(self.__notas)
        else:
            self.promedio_actual = 0.0
    
    # --- NUEVO: Generar reporte en archivo de texto (Manejo de Archivos) ---
    def exportar_boletin(self):
        nombre_archivo = f"boletin_{self.matricula}.txt"
        try:
            # 'w' creal el archivo o lo sobreescribe
            with open(nombre_archivo, 'w') as archivo:
                archivo.write(f"BOLETÍN OFICIAL - {self.matricula}\n")
                archivo.write("================================\n")
                archivo.write(f"Alumno: {self.nombre}\n")
                archivo.write(f"Edad: {self.edad}\n")
                archivo.write(f"Notas Detalladas: {self.__notas}\n")
                archivo.write(f"Promedio Final: {self.promedio_actual: .2f}\n")
                archivo.write("================================\n")
            print(f"Reporte exportado: {nombre_archivo}")
        except IOError:
            print("Error al crear el archivo de texto.")
    
    def mostrar_info(self):
        print(f"\nAlumno: {self.nombre} | Promedio: {self.promedio_actual: .2f}")

# --- PROGRAMA PRINCIPAÑ ---
if __name__ == "__main__":
    # 1. Iniciamos el gestor de BD
    db = BaseDeDatos()

    # 2. Creamos alumnos (Objetos)
    alumno1 = Estudiante("Cristiano Ronaldo", 20, "DATA-001")
    alumno1.agregar_notas(10, 10, 10)

    # 3. Aplicamos la PERSISTENCIA (SQLite)
    # Guardamos los objetos en la base de datos
    db.guardar_estudiante(alumno1)

    # 4. Aplicamos Manejo de Archivos
    # Generamos un archivo físico .txt para el alumno 1
    alumno1.exportar_boletin()

    
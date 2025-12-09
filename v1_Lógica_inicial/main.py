# --- DEFINICIÓN DE LA CLASE (EL MOLDE) ---
class Estudiante:
    """
    Esta clase define qué es un Estudiante y qué puede hacer.
    """

    # 1. EL CONSTRUCTOR (__init__)
    # Se ejectuta automáticamente al crear un nuevo estudiante.
    def __init__(self, nombre, edad):
        # Atributos (Estado del objeto)
        self.nombre = nombre    # Guardamos el nombre
        self.edad = edad        # Guardamos la edad
        self.notas = []         # Inicializamos una lista vacía para sus notas
        print(f"--> Se ha matriculado a: {self.nombre}")

    # 2. MÉTODOS (COMPORTAMIENTO)
    # Acciones que el estudiante puede realizar

    def agregar_nota(self, calificacion):
        """Recibe una nota y la guarda en su lista personal."""
        self.notas.append(calificacion)
        print(f"Nota {calificacion} agregada a {self.nombre}.")

    def calcular_promedio(self):
        """Calcula y devuelve el promedio de sus propias notas."""
        if len(self.notas) == 0:
            return 0.0
        
        suma = sum(self.notas) # Función de Python para sumar listas
        promedio = suma / len(self.notas)
        return promedio
    
    def mostrar_estado(self):
        """Dice si aprobó o no basándose en su promedio."""
        prom = self.calcular_promedio()
        estado = "APROBADO" if prom >= 6.0 else "REPROBADO"

        print(f"\n--- Boletín de {self.nombre} ---")
        print(f"Edad: {self.edad} años")
        print(f"Notas: {self.notas}")
        print(f"Promedio: {prom: .2f}") # .2f es para mostrar soolo 2 decimales
        print(f"Estado Final: {estado}")
        print("------------------------------")

# --- PROGRAMA PRINCIPAL (USO DE LOS OBJETOS) ---

# 1. Instalación (Crear objetos a partir del molde)
# Aquí nacen "estudiante1" y "estudiante2" con identidad propia.
alumno1 = Estudiante("Juan Pérez", 20)
alumno2 = Estudiante("Ana Gómez", 22)

# 2. Interacción (Usar sus métodos)
# Cada uno gestiona sus propias notas de forma independiente.
alumno1.agregar_nota(8.5)
alumno1.agregar_nota(9.0)
alumno1.agregar_nota(5.5)

alumno2.agregar_nota(10.0)
alumno2.agregar_nota(9.5)

# 3. Resultados
# Le pedimos a cada objeto que nos muestre su reporte.

alumno1.mostrar_estado()
alumno2.mostrar_estado()


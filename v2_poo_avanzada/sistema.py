from abc import ABC, abstractmethod #Importamos herramientas para clases abstractas

# --- CLASE PADRE (ABSTRACTA) ---
# Esta clase es una plantilla. No se pueden crear "Personas" genéricas,
# solo tipos específicos como Estudiantes o Profesores.
class Persona(ABC):

    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    # Este decorador obliga a las clases hijas a tener este método sí o sí
    @abstractmethod
    def mostrar_info(self):
        pass

# --- CLASE HIJA (HERENCIA) ---
# Estudiante "es una" Persona, así que hereda nombre y edad.
class Estudiante(Persona):
    
    def __init__(self, nombre, edad, matricula):
        # Usamos super() para llamar al constructor de la clase padre (Persona)
        super().__init__(nombre, edad)
        self.matricula = matricula

        # ENCAPSULAMIENTO:
        # Al poner doble guion bajo (__), hacemos que este atributo sea privado.
        # Nadie puede hacer: alumno.__notas = [10, 10] desde fuera.
        self.__notas = []

    # Uso de *args (Tuplas como parámetros)
    # Ahora podemos recibir 1 nota o 20 notas a la vez.
    def agregar_notas(self, *calificaciones):
        for nota in calificaciones:
            # Validamos que la nota sea lógica antes de guardarla
            if 0 <= nota <= 10:
                self.__notas.append(nota)
                print(f"Nota {nota} agregada a {self.nombre}.")
            else:
                print(f"Error: La nota {nota} no es válida.")

    # Método propio de la lógica de negocio
    def calcular_promedio(self):
        if not self.__notas:
            return 0.0
        return sum(self.__notas) / len(self.__notas)
    
    # Implementación del método abstracto (Polimorfismo)
    def mostrar_info(self):
        promedio = self.calcular_promedio()
        estado = "Aprobado" if promedio >= 6.0 else "Reprobado"

        print(f"\n --- Expediente Estudiantil ---")
        print(f"Nombre: {self.nombre}")
        print(f"Edad: {self.edad} años")
        print(f"Matrícula: {self.matricula}")
        # Accedemos a __notas internamente, aquí sí está permitido
        print(f"Historial de Notas: {self.__notas}")
        print(f"Promedio Actual: {promedio: .2f} -> {estado}")
        print("----------------------------------------")

# --- PRUEBA DEL SISTEMA ---

# 1. Crear estudiante (Instancia)
alumno1 = Estudiante("Pedro Páramo", 19, "DATA-1-2025")
alumno2 = Estudiante("Cristiano Ronald", 20, "DATA-2-2025")

# 2. Probamos el método con *args (agregamos muchas notas juntas)
alumno1.agregar_notas(9.5, 8.0, 10.0, 7.5) # El 15 debería dar un error
alumno2.agregar_notas(9.0, 9.5, 7.6, 8.6)

# 3. Probamos el Encapsulamiento (Intentamos hackear las notas)
# Si intentas esto: print(alumno1.__notas), Python dará error.
# Esto protege la integridad de los datos.

# 4. Mostramos el reporte final
alumno1.mostrar_info()
alumno2.mostrar_info()
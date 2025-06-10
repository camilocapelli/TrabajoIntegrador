import random
from collections import deque

# Clase Partido (Nodo)
class Partido:
    def __init__(self, equipo1=None, equipo2=None):
        self.equipo1 = equipo1
        self.equipo2 = equipo2
        self.ganador = None
        self.izquierdo = None
        self.derecho = None

    def simular(self):
        if self.equipo1 and self.equipo2:
            self.ganador = random.choice([self.equipo1, self.equipo2])
        elif self.equipo1:
            self.ganador = self.equipo1
        elif self.equipo2:
            self.ganador = self.equipo2
        else:
            self.ganador = None
        return self.ganador

# Construcción del árbol
def construir_fixture(equipos):
    nodos = [Partido(e1, e2) for e1, e2 in zip(equipos[::2], equipos[1::2])]
    
    while len(nodos) > 1:
        siguiente_ronda = []
        for i in range(0, len(nodos), 2):
            padre = Partido()
            padre.izquierdo = nodos[i]
            padre.derecho = nodos[i+1] if i+1 < len(nodos) else None
            siguiente_ronda.append(padre)
        nodos = siguiente_ronda
    return nodos[0]

# Simulación del torneo
def simular_torneo(nodo):
    if nodo is None:
        return None
    if nodo.izquierdo is None and nodo.derecho is None:
        nodo.simular()
        return nodo.ganador
    nodo.equipo1 = simular_torneo(nodo.izquierdo)
    nodo.equipo2 = simular_torneo(nodo.derecho)
    nodo.simular()
    return nodo.ganador

# Validar cantidad de equipos
def es_potencia_de_dos(n):
    return n >= 2 and (n & (n - 1)) == 0

# Definir nombres de etapas según la cantidad de equipos (profundidad)
etapas_nombre = {
    1: "Final",
    2: "Semifinales",
    3: "Cuartos de final",
    4: "Octavos de final",
    5: "Dieciseisavos de final"
}

# Calcular profundidad máxima del árbol
def profundidad_arbol(nodo):
    if nodo is None:
        return 0
    izq = profundidad_arbol(nodo.izquierdo)
    der = profundidad_arbol(nodo.derecho)
    return max(izq, der) + 1

# Mostrar fixture nivel por nivel desde ronda inicial hasta final
def mostrar_fixture_por_niveles(raiz):
    if raiz is None:
        return
    
    profundidad_max = profundidad_arbol(raiz)
    cola = deque()
    cola.append((raiz, 1))  # nodo y nivel
    
    niveles = {}
    
    while cola:
        nodo, nivel = cola.popleft()
        if nivel not in niveles:
            niveles[nivel] = []
        niveles[nivel].append(nodo)
        
        if nodo.izquierdo:
            cola.append((nodo.izquierdo, nivel + 1))
        if nodo.derecho:
            cola.append((nodo.derecho, nivel + 1))
    
    # Imprimir desde nivel máximo (ronda inicial) hasta 1 (final)
    for nivel in range(profundidad_max, 0, -1):
        etapa = etapas_nombre.get(nivel, f"Ronda {nivel}")
        print(f"\n[{etapa}]")
        for partido in niveles.get(nivel, []):
            if partido.equipo1 and partido.equipo2:
                print(f"  {partido.equipo1} vs {partido.equipo2} → {partido.ganador}")

# Programa Principal
if __name__ == "__main__":
    print("SIMULADOR DE FIXTURE DE LIGA ARGENTINA")

    while True:
        try:
            cantidad = int(input("Ingrese la cantidad de equipos (potencia de 2, máximo 16): "))
            if not es_potencia_de_dos(cantidad):
                print("La cantidad debe ser una potencia de 2.")
            elif cantidad > 16:
                print("La cantidad máxima permitida es 16.")
            else:
                break
        except ValueError:
            print("Ingrese un número válido.")

    equipos = []
    print("\nIngrese los nombres de los equipos:")
    for i in range(cantidad):
        nombre = input(f"Equipo {i+1}: ")
        equipos.append(nombre.strip())

    print("\nEquipos cargados:")
    for e in equipos:
        print(f"- {e}")

    print("\nConstruyendo fixture...")
    raiz = construir_fixture(equipos)

    print("\nSimulando partidos...")
    campeon = simular_torneo(raiz)

    print("\nFixture completo:")
    mostrar_fixture_por_niveles(raiz)

    print(f"\n¡El campeón del torneo es: {campeon}!")
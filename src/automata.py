import graphviz
import json

class Estado:
    def __init__(self, nombre, es_final=False):
        self.nombre = nombre
        self.es_final = es_final
        self.transiciones = {}

    def agregar_transicion(self, simbolo, estado_destino):
        """Agrega una transición desde este estado a otro con un símbolo."""
        if simbolo in self.transiciones:
            self.transiciones[simbolo].append(estado_destino)
        else:
            self.transiciones[simbolo] = [estado_destino]

    def __repr__(self):
        return f"Estado({self.nombre}, Final={self.es_final})"


class Automata:
    def __init__(self, tipo='AFND'):
        self.tipo = tipo
        self.estados = {}
        self.estado_inicial = None

    def agregar_estado(self, nombre, es_final=False):
        """Agrega un estado al autómata."""
        nombre = nombre.lower()
        if nombre not in self.estados:
            self.estados[nombre] = Estado(nombre, es_final)
            print(f"✅ Estado agregado: {nombre} (Final: {es_final})")  # Debugging
        if self.estado_inicial is None:
            self.estado_inicial = self.estados[nombre]
            print(f"✅ Estado inicial establecido: {self.estado_inicial}")


    def agregar_transicion(self, origen, simbolo, destino):
        """Agrega una transición entre estados."""
        origen, destino = origen.lower(), destino.lower()
        if origen not in self.estados:
            raise ValueError(f"❌ Error: Estado origen '{origen}' no encontrado. Estados disponibles: {list(self.estados.keys())}")
        if destino not in self.estados:
            raise ValueError(f"❌ Error: Estado destino '{destino}' no encontrado. Estados disponibles: {list(self.estados.keys())}")

        self.estados[origen].agregar_transicion(simbolo, self.estados[destino])

    def fusionar(self, otro):
        """Fusiona los estados de otro autómata con el actual, manteniendo las referencias."""
        for nombre, estado in otro.estados.items():
            if nombre not in self.estados:
                self.estados[nombre] = estado

        # Mantener estado inicial si es un nuevo autómata fusionado
        if not self.estado_inicial:
            self.estado_inicial = otro.estado_inicial

    def mostrar_automata(self):
        """Muestra los estados y transiciones del autómata en consola."""
        print(f"\n🔷 Tipo: {self.tipo}")
        print(f"🔹 Estado inicial: {self.estado_inicial.nombre if self.estado_inicial else 'Ninguno'}")
        for estado in self.estados.values():
            transiciones_str = ", ".join(
                f"{simbolo} -> {', '.join(dest.nombre for dest in destinos)}"
                for simbolo, destinos in estado.transiciones.items()
            ) if estado.transiciones else "Sin transiciones"
            print(f"🔹 Estado {estado.nombre} {'(Final)' if estado.es_final else ''}: {transiciones_str}")

def establecer_estado_inicial(self, nombre):
    """Establece el estado inicial del autómata."""
    if self.estado_inicial is None:
        self.estado_inicial = self.estados.get(nombre.lower())
        print(f"✅ Estado inicial establecido: {self.estado_inicial}")
    else:
        print(f"⚠️ Advertencia: El estado inicial ya está definido como {self.estado_inicial}. Ignorando {nombre}.")

    return self
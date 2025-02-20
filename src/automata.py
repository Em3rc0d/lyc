### src/automata.py
import graphviz
import json

class Estado:
    def __init__(self, nombre, es_final=False):
        self.nombre = nombre
        self.es_final = es_final
        self.transiciones = {}

    def agregar_transicion(self, simbolo, estado_destino):
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
        if nombre in self.estados:
            raise ValueError(f"El estado '{nombre}' ya existe.")
        
        self.estados[nombre] = Estado(nombre, es_final)
        if not self.estado_inicial:
            self.estado_inicial = self.estados[nombre]


    def agregar_transicion(self, origen, simbolo, destino):
        if origen not in self.estados:
            raise ValueError(f"El estado origen '{origen}' no existe en el autómata.")
        if destino not in self.estados:
            raise ValueError(f"El estado destino '{destino}' no existe en el autómata.")
        
        self.estados[origen].agregar_transicion(simbolo, self.estados[destino])

        if self.estado_inicial == self.estados[origen]:
            self.estado_inicial = self.estados[destino]

        return self

    def mostrar_automata(self):
        print(f"Tipo: {self.tipo}")
        print(f"Estado inicial: {self.estado_inicial.nombre if self.estado_inicial else 'Ninguno'}")
        
        for estado in self.estados.values():
            transiciones_str = ", ".join(
                f"{simbolo} -> {', '.join(dest.nombre for dest in destinos)}"
                for simbolo, destinos in estado.transiciones.items()
            )
            print(f"Estado {estado.nombre} {'(Final)' if estado.es_final else ''}: {transiciones_str}")

        return self
    
    def obtener_transiciones(self):
        return {
            estado.nombre: {
                simbolo: [dest.nombre for dest in destinos]
                for simbolo, destinos in estado.transiciones.items()
            }
            for estado in self.estados.values()
        }

    def generar_grafico(self, filename="automata"):
        dot = graphviz.Digraph()
        for estado in self.estados.values():
            shape = "doublecircle" if estado.es_final else "circle"
            dot.node(estado.nombre, shape=shape)
        for estado in self.estados.values():
            for simbolo, destinos in estado.transiciones.items():
                for destino in destinos:
                    dot.edge(estado.nombre, destino.nombre, label=simbolo)
        dot.render(filename, format="png", cleanup=True)        
        return self
    
    def guardar_en_json(self, filepath):
        data = {
            "estados": [{"nombre": estado.nombre, "final": estado.es_final} for estado in self.estados.values()],
            "transiciones": [
                {"origen": estado.nombre, "simbolo": simbolo, "destino": destino.nombre}
                for estado in self.estados.values()
                for simbolo, destinos in estado.transiciones.items()
                for destino in destinos
            ]
        }
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"✅ Autómata guardado en '{filepath}'.")
        return self
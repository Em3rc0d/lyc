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

        #if self.estado_inicial == self.estados[origen]:
         #self.estado_inicial = self.estados[destino]

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
    
    def minimizar(self):
        if self.tipo != 'AFD':
            raise ValueError("Solo se puede minimizar un AFD.")
        
        estados = list(self.estados.values())
        simbolos = set()
        for estado in estados:
            simbolos.update(estado.transiciones.keys())
        
        finales = {estado.nombre for estado in estados if estado.es_final}
        no_finales = {estado.nombre for estado in estados if not estado.es_final}
        particiones = [finales, no_finales]
        
        while True:
            nuevas_particiones = []
            for grupo in particiones:
                subgrupos = {}
                for estado in grupo:
                    key = tuple(
                        next((i for i, g in enumerate(particiones) if self.estados[dest.nombre].nombre in g), -1)
                        for simbolo in simbolos
                        for dest in self.estados[estado].transiciones.get(simbolo, [])
                    )
                    if key in subgrupos:
                        subgrupos[key].add(estado)
                    else:
                        subgrupos[key] = {estado}
                nuevas_particiones.extend(subgrupos.values())
            if nuevas_particiones == particiones:
                break
            particiones = nuevas_particiones
        
        nuevo_automata = Automata(tipo='AFD')
        estado_mapeo = {}
        for i, grupo in enumerate(particiones):
            nombre_grupo = f"Q{i}"
            es_final = any(self.estados[nombre].es_final for nombre in grupo)
            nuevo_automata.agregar_estado(nombre_grupo, es_final)
            for nombre in grupo:
                estado_mapeo[nombre] = nombre_grupo
        
        for grupo in particiones:
            representante = next(iter(grupo))
            for simbolo, destinos in self.estados[representante].transiciones.items():
                if destinos:
                    nuevo_automata.agregar_transicion(estado_mapeo[representante], simbolo, estado_mapeo[destinos[0].nombre])
        
        return nuevo_automata


    def cerradura_epsilon(self, estados):
        """Calcula la cerradura épsilon de un conjunto de estados"""
        cerradura = set(estados)
        pila = list(estados)

        while pila:
            estado = pila.pop()
            if "" in estado.transiciones:  # Si hay transiciones épsilon
                for destino in estado.transiciones[""]:
                    if destino not in cerradura:
                        cerradura.add(destino)
                        pila.append(destino)

        return cerradura

import json
from automata import Automata
from visualizer import Visualizer
from validator import Validator

class AFND_to_AFD:
    def __init__(self):
        self.afnd = Automata(tipo='AFND')

    def cargar_desde_json(self, filepath):
        """Carga el autómata desde un archivo JSON con manejo de errores."""
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"❌ Error: Archivo '{filepath}' no encontrado")
            return self
        except json.JSONDecodeError:
            print(f"❌ Error: Archivo '{filepath}' no tiene un formato JSON válido.")
            return self

        for estado in data.get("estados", []):
            self.afnd.agregar_estado(estado["nombre"], estado.get("final", False))

        for transicion in data.get("transiciones", []):
            origen = transicion.get("origen")
            destino = transicion.get("destino")
            if origen in self.afnd.estados and destino in self.afnd.estados:
                self.afnd.agregar_transicion(origen, transicion.get("simbolo"), destino)
            else:
                print(f"⚠️ Advertencia: Estado no encontrado en transición {transicion}")
        
        self.afnd.estado_inicial = self.afnd.estados.get(data.get("estado_inicial"))
        return self

    def convertir(self):
        """Convierte el AFND a un AFD utilizando el algoritmo de construcción del subconjunto."""
        if not self.afnd.estado_inicial:
            print("❌ Error: No se ha definido un estado inicial en el AFND.")
            return None
        
        afd = Automata(tipo='AFD')
        procesados = {}  # Mapea frozenset de estados -> nombre
        cola = []
        contador = 0
        conjunto_inicial = frozenset([self.afnd.estado_inicial])
        cola.append(conjunto_inicial)
        procesados[conjunto_inicial] = f"Q{contador}"
        afd.agregar_estado(f"Q{contador}", any(e.es_final for e in conjunto_inicial))
        contador += 1

        while cola:
            conjunto_actual = cola.pop(0)
            nombre_actual = procesados[conjunto_actual]
            transiciones_nuevas = {}

            for estado in conjunto_actual:
                for simbolo, destinos in estado.transiciones.items():
                    transiciones_nuevas.setdefault(simbolo, set()).update(destinos)

            for simbolo, destinos in transiciones_nuevas.items():
                conjunto_destino = frozenset(destinos)
                if conjunto_destino in procesados:
                    nombre_destino = procesados[conjunto_destino]
                else:
                    nombre_destino = f"Q{contador}"
                    procesados[conjunto_destino] = nombre_destino
                    afd.agregar_estado(nombre_destino, any(e.es_final for e in conjunto_destino))
                    contador += 1
                    cola.append(conjunto_destino)
                afd.agregar_transicion(nombre_actual, simbolo, nombre_destino)
        
        return afd

    def guardar_en_json(self, filepath):
        data = {
            "estado_inicial": self.afnd.estado_inicial.nombre if self.afnd.estado_inicial else None,
            "estados": [{"nombre": estado.nombre, "final": estado.es_final} for estado in self.afnd.estados.values()],
            "transiciones": [
                {"origen": estado.nombre, "simbolo": simbolo, "destino": destino.nombre}
                for estado in self.afnd.estados.values()
                for simbolo, destinos in estado.transiciones.items()
                for destino in destinos
            ]
        }
        try:
            with open(filepath, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"✅ Autómata guardado en '{filepath}'.")
        except Exception as e:
            print(f"❌ Error al guardar el archivo: {e}")
        return self

    def mostrar_automatas(self):
        print("\n🔹 Autómata Finito No Determinista (AFND):")
        self.afnd.mostrar_automata()
        print("\n🔹 Autómata Finito Determinista (AFD):")
        afd = self.convertir()
        if afd:
            afd.mostrar_automata()
        return self

    def generar_grafico(self, filename="automata"):
        Visualizer.generar_grafico(self.afnd, filename)
        return self

    def validar_cadena(self, cadena):
        afd = self.convertir()
        if afd:
            return Validator.validar_cadena(afd, cadena)
        return False

    def agregar_estado(self, nombre, es_final=False):
        self.afnd.agregar_estado(nombre.lower(), es_final)
        return self

    def agregar_transicion(self, origen, simbolo, destino):
        """Agrega una transición al autómata."""
        origen = origen.lower()
        destino = destino.lower()

        if origen not in self.estados:
            raise ValueError(f"❌ Error: El estado origen '{origen}' no existe en el autómata.")
        if destino not in self.estados:
            raise ValueError(f"❌ Error: El estado destino '{destino}' no existe en el autómata.")

        # Agregar la transición correctamente
        self.estados[origen].agregar_transicion(simbolo, self.estados[destino])

        return self

import json
from automata import Automata

class AFND(Automata):
    def __init__(self):
        super().__init__(tipo='AFND')

    def cargar_desde_json(self, filepath):
        """Carga el autómata desde un archivo JSON."""
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)

            for estado in data.get("estados", []):
                self.agregar_estado(estado["nombre"], estado.get("final", False))

            for transicion in data.get("transiciones", []):
                if transicion["origen"] in self.estados and transicion["destino"] in self.estados:
                    self.agregar_transicion(transicion["origen"], transicion["simbolo"], transicion["destino"])
                else:
                    print(f"⚠️ Advertencia: Estado no encontrado en transición {transicion}")

        except FileNotFoundError:
            print(f"❌ Error: Archivo '{filepath}' no encontrado.2")
        except json.JSONDecodeError:
            print(f"❌ Error: Archivo '{filepath}' no tiene un formato JSON válido.")
        
        return self

    def guardar_en_json(self, filepath="../data/automata1.json"):
        """Guarda el autómata en un archivo JSON con formato corregido."""
        data = {
            "estados": [{"nombre": estado.nombre, "final": estado.es_final} for estado in self.estados.values()],
            "transiciones": [
                {"origen": estado.nombre, "simbolo": simbolo, "destino": destino}
                for estado in self.estados.values()
                for simbolo, destinos in estado.transiciones.items()
                for destino in destinos  # Corregido: solo almacena nombres de estados, no objetos
            ]
        }

        try:
            with open(filepath, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"✅ Autómata guardado en '{filepath}'.")
        except Exception as e:
            print(f"❌ Error al guardar el archivo: {e}")

        return self

    def agregar_transicion(self, origen, simbolo, destino):
        """Agrega una transición al autómata."""
        origen = origen.lower()
        destino = destino.lower()
        
        if origen not in self.estados:
            raise ValueError(f"El estado origen '{origen}' no existe en el autómata.")
        if destino not in self.estados:
            raise ValueError(f"El estado destino '{destino}' no existe en el autómata.")
        
        # Agregar la transición correctamente
        self.estados[origen].agregar_transicion(simbolo, self.estados[destino])

        return self

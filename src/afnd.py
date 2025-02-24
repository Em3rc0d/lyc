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

            # Verificar que el archivo tiene la estructura correcta
            if "estados" not in data or "transiciones" not in data:
                raise ValueError("❌ Error: El JSON no tiene la estructura esperada. Debe incluir 'estados' y 'transiciones'.")

            # Agregar todos los estados primero
            for estado in data["estados"]:
                nombre = estado.get("nombre")
                es_final = estado.get("final", False)
                if nombre:
                    self.agregar_estado(nombre, es_final)

            # 🔍 Depuración: Verificar estados cargados antes de agregar transiciones
            print(f"📌 Estados registrados antes de transiciones: {list(self.estados.keys())}")

            # Luego, agregar transiciones
            for transicion in data["transiciones"]:
                origen = transicion.get("origen")
                simbolo = transicion.get("simbolo")
                destino = transicion.get("destino")

                if origen in self.estados and destino in self.estados:
                    self.agregar_transicion(origen, simbolo, destino)
                else:
                    print(f"⚠️ Advertencia: Estado no encontrado en la transición {transicion}")

            # 🔍 Debug: Verificar transiciones cargadas
            for estado in self.estados.values():
                print(f"📌 Transiciones de {estado.nombre}: {estado.transiciones}")

        except FileNotFoundError:
            print(f"❌ Error: Archivo '{filepath}' no encontrado.")
        except json.JSONDecodeError:
            print(f"❌ Error: Archivo '{filepath}' no tiene un formato JSON válido.")
        except ValueError as ve:
            print(ve)

        return self


    def guardar_en_json(self, filepath="../data/automata1.json"):
        """Guarda el autómata en un archivo JSON con formato corregido."""
        data = {
            "estados": [{"nombre": estado.nombre, "final": estado.es_final} for estado in self.estados.values()],
            "transiciones": [
                {"origen": estado.nombre, "simbolo": simbolo, "destino": destino.nombre}  # Almacena solo nombres
                for estado in self.estados.values()
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

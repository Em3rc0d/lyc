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

            for estado in data.get("estados", []):
                self.afnd.agregar_estado(estado["nombre"], estado.get("final", False))

            for transicion in data.get("transiciones", []):
                if transicion["origen"] in self.afnd.estados and transicion["destino"] in self.afnd.estados:
                    self.afnd.agregar_transicion(transicion["origen"], transicion["simbolo"], transicion["destino"])
                else:
                    print(f"⚠️ Advertencia: Estado no encontrado en transición {transicion}")

        except FileNotFoundError:
            print(f"❌ Error: Archivo '{filepath}' no encontrado")
        except json.JSONDecodeError:
            print(f"❌ Error: Archivo '{filepath}' no tiene un formato JSON válido.")
        
        return self

    def guardar_en_json(self, filepath):
        data = {
            "estados": [{"nombre": estado.nombre, "final": estado.es_final} for estado in self.afnd.estados.values()],
            "transiciones": [
                {"origen": estado.nombre, "simbolo": simbolo, "destino": destino.nombre}
                for estado in self.afnd.estados.values()
                for simbolo, destinos in estado.transiciones.items()
                for destino in destinos
            ]
        }
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        return self

    def convertir(self):
        afd = Automata(tipo='AFD')
        estados_procesados = {}
        cola = [frozenset([self.afnd.estado_inicial])]
        contador = 0  # Para asignar nombres únicos

        while cola:
            conjunto_estados = cola.pop(0)
            
            # Si el conjunto ya tiene un nombre, reutilizarlo
            nombre_estado = None
            for key, value in estados_procesados.items():
                if value == conjunto_estados:
                    nombre_estado = key
                    break
            if not nombre_estado:
                nombre_estado = f"Q{contador}"
                contador += 1

            if nombre_estado not in estados_procesados:
                es_final = any(e.es_final for e in conjunto_estados)
                afd.agregar_estado(nombre_estado, es_final)
                estados_procesados[nombre_estado] = conjunto_estados

                transiciones_nuevas = {}
                for estado in conjunto_estados:
                    for simbolo, destinos in estado.transiciones.items():
                        transiciones_nuevas.setdefault(simbolo, set()).update(destinos)

                for simbolo, destinos in transiciones_nuevas.items():
                    if destinos:
                        # Buscar si el conjunto ya fue procesado
                        destino_nombre = None
                        for key, value in estados_procesados.items():
                            if value == destinos:
                                destino_nombre = key
                                break
                        if not destino_nombre:
                            destino_nombre = f"Q{contador}"
                            contador += 1
                            cola.append(frozenset(destinos))  # Solo encolar si es nuevo

                        afd.agregar_transicion(nombre_estado, simbolo, destino_nombre)

        return afd


    def mostrar_automatas(self):
        print("\n🔹 Autómata Finito No Determinista (AFND):")
        self.afnd.mostrar_automata()

        print("\n🔹 Autómata Finito Determinista (AFD):")
        afd = self.convertir()
        afd.mostrar_automata()
        return self


    def generar_grafico(self, filename="automata"):
        Visualizer.generar_grafico(self.afnd, filename)
        return self

    def validar_cadena(self, cadena):
        afd = self.convertir()  # Convertir el AFND a AFD antes de validar
        return Validator.validar_cadena(afd, cadena)

    def agregar_estado(self, nombre, es_final=False):
        nombre = nombre.lower()
        self.afnd.agregar_estado(nombre, es_final)
        return self

    def agregar_transicion(self, origen, simbolo, destino):
        origen = origen.lower()
        destino = destino.lower()
        self.afnd.agregar_transicion(origen, simbolo, destino)
        return self 
    

    
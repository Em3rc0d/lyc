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
        estados_procesados = {}  # Mapeo de nombres a conjuntos de estados
        cola = []  # Usamos una cola FIFO

        # Calcular cerradura épsilon del estado inicial
        estado_inicial = self.afnd.cerradura_epsilon({self.afnd.estado_inicial})
        estado_inicial = frozenset(estado_inicial)

        print(f"⚙️ Cerradura épsilon del estado inicial: {estado_inicial}")

        # Asignar el primer nombre "Q0"
        estados_procesados["Q0"] = estado_inicial
        afd.agregar_estado("Q0", any(e.es_final for e in estado_inicial))
        cola.append(("Q0", estado_inicial))  # Encolamos el estado inicial

        contador = 1  # Para nombres de estados nuevos

        while cola:
            nombre_actual, conjunto_actual = cola.pop(0)
            print(f"⚙️ Procesando estado: {nombre_actual} con conjunto {conjunto_actual}")

            transiciones_nuevas = {}
            for estado in conjunto_actual:
                for simbolo, destinos in estado.transiciones.items():
                    if simbolo:  # Ignorar transiciones épsilon
                        transiciones_nuevas.setdefault(simbolo, set()).update(destinos)

            for simbolo, destinos in transiciones_nuevas.items():
                print(f"🔍 Transición detectada: {nombre_actual} --({simbolo})--> {destinos}")
                destinos_frozen = frozenset(self.afnd.cerradura_epsilon(destinos))  # Aplicar cerradura épsilon

                destino_nombre = None
                # Buscar si el destino ya está registrado
                for key, value in estados_procesados.items():
                    if value == destinos_frozen:
                        destino_nombre = key
                        break

                if not destino_nombre:  # Si no existe, se crea
                    destino_nombre = f"Q{contador}"
                    contador += 1
                    estados_procesados[destino_nombre] = destinos_frozen
                    afd.agregar_estado(destino_nombre, any(e.es_final for e in destinos_frozen))
                    cola.append((destino_nombre, destinos_frozen))  # Se encola para su procesamiento

                # Agregar la transición en el AFD
                afd.agregar_transicion(nombre_actual, simbolo, destino_nombre)
                print(f"✅ Agregando transición: {nombre_actual} --({simbolo})--> {destino_nombre}")

        print(f"📌 Estados procesados: {estados_procesados}")
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
    

    
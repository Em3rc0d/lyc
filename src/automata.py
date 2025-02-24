import graphviz
import json
import logging

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
        """Agrega un estado al autómata si no existe. Si existe, lo marca como final si es necesario."""
        nombre = nombre.lower()

        # Establecer el estado inicial si aún no se ha definido
        if self.estado_inicial is None:
            self.establecer_estado_inicial(nombre)

        # Si el estado ya existe, solo actualizar si es final
        if nombre in self.estados:
            if es_final:
                self.estados[nombre].es_final = True
                logging.debug(f"✅ Estado actualizado: {nombre} (Final: {es_final})")
            else:
                logging.warning(f"⚠️ El estado '{nombre}' ya existe y no se actualizará.")
        else:
            # Agregar nuevo estado
            self.estados[nombre] = Estado(nombre, es_final)
            logging.debug(f"✅ Estado agregado correctamente: {nombre} (Final: {es_final})")

        # 🔍 Debug: Mostrar estados disponibles
        logging.debug(f"📌 Estados actuales: {list(self.estados.keys())}")

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


    def fusionar(self, otro):
        """Fusiona los estados de otro autómata con el actual, evitando duplicados."""
        for nombre, estado in otro.estados.items():
            if nombre not in self.estados:
                self.estados[nombre] = estado
            else:
                # Fusionar transiciones sin duplicar
                for simbolo, destinos in estado.transiciones.items():
                    for destino in destinos:
                        if destino not in self.estados[nombre].transiciones.get(simbolo, []):
                            self.estados[nombre].agregar_transicion(simbolo, destino)

        # Mantener estado inicial si aún no se ha definido
        if self.estado_inicial is None:
            self.estado_inicial = otro.estado_inicial

        return self

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
        """Establece el estado inicial solo si aún no se ha definido."""
        if self.estado_inicial is None:
            self.estado_inicial = self.estados.get(nombre.lower())
            print(f"✅ Estado inicial establecido: {self.estado_inicial}")
        else:
            print(f"⚠️ Advertencia: El estado inicial ya está definido como {self.estado_inicial}. Ignorando {nombre}.")

        return self


    def guardar_automata(self, archivo="automata.json"):
        """Guarda los estados y transiciones del autómata en un archivo JSON."""
        datos = {
            "tipo": self.tipo,
            "estado_inicial": self.estado_inicial.nombre if self.estado_inicial else None,
            "estados": {
                nombre: {
                    "es_final": estado.es_final,
                    "transiciones": {
                        simbolo: [dest.nombre for dest in destinos]
                        for simbolo, destinos in estado.transiciones.items()
                    }
                } for nombre, estado in self.estados.items()
            }
        }

        with open(archivo, "w") as f:
            json.dump(datos, f, indent=4)
        print(f"📁 Autómata guardado en {archivo}")

        return self


    def cargar_automata(archivo="automata.json"):
        """Carga un autómata desde un archivo JSON y lo reconstruye."""
        with open(archivo, "r") as f:
            datos = json.load(f)

        automata = Automata(datos["tipo"])

        # Crear diccionario de estados
        estados_dict = {estado["nombre"]: estado for estado in datos["estados"]}

        # Agregar estados
        for nombre, info in estados_dict.items():
            automata.agregar_estado(nombre, info["final"])

        # Agregar transiciones
        for transicion in datos["transiciones"]:
            origen = transicion["origen"]
            destino = transicion["destino"]

            if origen in estados_dict and destino in estados_dict:
                automata.agregar_transicion(origen, transicion["simbolo"], destino)
            else:
                print(f"⚠️ Advertencia: Estado en transición no encontrado: {origen} → {destino}")

        # Establecer estado inicial
        if "estado_inicial" in datos and datos["estado_inicial"] in estados_dict:
            automata.estado_inicial = automata.estados[datos["estado_inicial"]]
        else:
            print(f"⚠️ Advertencia: Estado inicial '{datos.get('estado_inicial')}' no encontrado")

        print(f"📂 Autómata cargado desde {archivo}")
        return automata

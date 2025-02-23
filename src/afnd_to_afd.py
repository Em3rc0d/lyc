from automata import Automata, Estado
from validator import Validator
from typing import Dict, Set, FrozenSet, Tuple
from collections import defaultdict

class AFND_to_AFD:
    def __init__(self):
        self.afnd = Automata(tipo='AFND')
        self._cache_cerradura: Dict[FrozenSet[Estado], Set[Estado]] = {}
        self._cache_transiciones: Dict[Tuple[FrozenSet[Estado], str], Set[Estado]] = {}

    def convertir(self) -> Automata:
        if not self.afnd.validar_estructura():
            raise ValueError("El AFND no es válido")

        afd = Automata(tipo='AFD')
        estados_procesados: Dict[str, FrozenSet[Estado]] = {}
        estados_por_procesar = [self._obtener_estado_inicial()]
        contador = 0

        while estados_por_procesar:
            conjunto_actual = estados_por_procesar.pop(0)
            nombre_estado = self._obtener_nombre_estado(conjunto_actual, estados_procesados)

            if nombre_estado not in estados_procesados:
                es_final = any(e.es_final for e in conjunto_actual)
                afd.agregar_estado(nombre_estado, es_final)
                estados_procesados[nombre_estado] = conjunto_actual

                for simbolo in self.afnd.alfabeto:
                    if simbolo == "ε":
                        continue
                        
                    nuevos_estados = self._calcular_transicion(conjunto_actual, simbolo)
                    if nuevos_estados:
                        nuevo_nombre = self._obtener_nombre_estado(nuevos_estados, estados_procesados)
                        if nuevo_nombre not in estados_procesados:
                            estados_por_procesar.append(nuevos_estados)
                        afd.agregar_transicion(nombre_estado, simbolo, nuevo_nombre)

        return afd

    def _obtener_estado_inicial(self) -> FrozenSet[Estado]:
        return frozenset(Validator._cerradura_epsilon({self.afnd.estado_inicial}))

    def _calcular_transicion(self, estados: FrozenSet[Estado], simbolo: str) -> FrozenSet[Estado]:
        cache_key = (estados, simbolo)
        if cache_key in self._cache_transiciones:
            return self._cache_transiciones[cache_key]

        destinos = set()
        for estado in estados:
            for destino in estado.transiciones.get(simbolo, []):
                destinos.update(Validator._cerradura_epsilon({destino}))

        resultado = frozenset(destinos)
        self._cache_transiciones[cache_key] = resultado
        return resultado

    @staticmethod
    def _obtener_nombre_estado(conjunto: FrozenSet[Estado], estados_procesados: Dict[str, FrozenSet[Estado]]) -> str:
        for nombre, conjunto_existente in estados_procesados.items():
            if conjunto == conjunto_existente:
                return nombre
        return f"q{len(estados_procesados)}"

    def mostrar_automatas(self):
        print("\n🔹 Autómata Finito No Determinista (AFND):")
        self.afnd.mostrar_automata()

        print("\n🔹 Autómata Finito Determinista (AFD):")
        afd = self.convertir()
        afd.mostrar_automata()
        return self

    def validar_cadena(self, cadena):
        afd = self.convertir()
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



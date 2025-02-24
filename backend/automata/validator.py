from .automata import Automata, Estado
from typing import Set, Dict, List, FrozenSet
from functools import lru_cache

class Validator:
    @staticmethod
    def validar_cadena(automata: Automata, cadena: str) -> bool:
        try:
            if not isinstance(automata, Automata) or not isinstance(cadena, str):
                raise ValueError("Tipos de datos inválidos")

            if not automata.estado_inicial:
                return False

            # Validar que exista al menos un estado final
            if not any(estado.es_final for estado in automata.estados.values()):
                return False

            # Conjunto inicial de estados
            estados_actuales = {automata.estado_inicial}
            
            # Para cada símbolo en la cadena
            for simbolo in cadena:
                print(f"Procesando símbolo: {simbolo}")
                if not estados_actuales:
                    return False
                    
                # Obtener próximos estados para el símbolo actual
                nuevos_estados = set()
                for estado in estados_actuales:
                    print(f"Evaluando estado: {estado.nombre}")
                    if simbolo in estado.transiciones:
                        nuevos_estados.update(estado.transiciones[simbolo])
                
                if nuevos_estados:
                    print(f"Nuevos estados para {simbolo}: {[e.nombre for e in nuevos_estados]}")
                else:
                    print(f"No hay transiciones válidas para {simbolo}")
                    
                estados_actuales = nuevos_estados

            # Verificar si llegamos a un estado final
            return any(estado.es_final for estado in estados_actuales)

        except Exception as e:
            print(f"Error en validación: {str(e)}")
            return False

    @staticmethod
    def _procesar_simbolo_afnd(estados: Set[Estado], simbolo: str) -> Set[Estado]:
        nuevos_estados = set()
        for estado in estados:
            if simbolo in estado.transiciones:
                nuevos_estados.update(estado.transiciones[simbolo])
        return nuevos_estados

    @staticmethod
    @lru_cache(maxsize=128)
    def _cerradura_epsilon(estados: FrozenSet[Estado]) -> FrozenSet[Estado]:
        if not estados:
            return frozenset()
            
        pila = list(estados)
        cerradura = set(estados)

        while pila:
            estado = pila.pop()
            if "ε" in estado.transiciones:
                for siguiente in estado.transiciones["ε"]:
                    if siguiente not in cerradura:
                        cerradura.add(siguiente)
                        pila.append(siguiente)

        return frozenset(cerradura)

    @staticmethod
    def _obtener_alfabeto(automata: Automata) -> Set[str]:
        alfabeto = set()
        for estado in automata.estados.values():
            alfabeto.update(estado.transiciones.keys())
        alfabeto.discard("ε")
        return alfabeto
from automata import Automata
from typing import Set, Dict, List
from functools import lru_cache

class Validator:
    @staticmethod
    def validar_cadena(automata: Automata, cadena: str) -> bool:
        try:
            if not isinstance(automata, Automata) or not isinstance(cadena, str):
                raise ValueError("Tipos de datos inválidos")

            if automata.estado_inicial is None:
                return False

            # Comenzamos con la cerradura-ε del estado inicial
            estados_actuales = Validator._cerradura_epsilon({automata.estado_inicial})

            # Para cada símbolo en la cadena
            for simbolo in cadena:
                estados_actuales = Validator._procesar_simbolo_afnd(estados_actuales, simbolo)
                if not estados_actuales:
                    return False

            # Verificamos si algún estado actual es final
            return any(estado.es_final for estado in estados_actuales)
        except Exception as e:
            print(f"Error en validación: {str(e)}")
            return False

    @staticmethod
    def _procesar_simbolo_afnd(estados: Set, simbolo: str) -> Set:
        nuevos_estados = set()
        # Procesamos cada estado actual
        for estado in estados:
            # Obtenemos todos los estados alcanzables con el símbolo
            if simbolo in estado.transiciones:
                for estado_destino in estado.transiciones[simbolo]:
                    # Agregamos el estado destino y su cerradura-ε
                    nuevos_estados.update(Validator._cerradura_epsilon({estado_destino}))
        return nuevos_estados

    @staticmethod
    @lru_cache(maxsize=128)
    def _cerradura_epsilon(estados: Set) -> Set:
        pila = list(estados)
        cerradura = set(estados)

        while pila:
            estado = pila.pop()
            # Procesamos transiciones épsilon
            if "ε" in estado.transiciones:
                for siguiente in estado.transiciones["ε"]:
                    if siguiente not in cerradura:
                        cerradura.add(siguiente)
                        pila.append(siguiente)

        return cerradura

    @staticmethod
    def _obtener_alfabeto(automata: Automata) -> Set[str]:
        alfabeto = set()
        for estado in automata.estados.values():
            alfabeto.update(estado.transiciones.keys())
        alfabeto.discard("ε")
        return alfabeto

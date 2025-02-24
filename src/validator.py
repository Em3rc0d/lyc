from collections import deque
from automata import Automata

class Validator:
    @staticmethod
    def validar_cadena(automata, cadena, debug=False):
        """
        Valida si una cadena es aceptada por el autómata.

        :param automata: Instancia del autómata.
        :param cadena: Cadena a evaluar.
        :param debug: Si es True, muestra el proceso paso a paso.
        :return: True si la cadena es aceptada, False en caso contrario.
        """
        # Validaciones iniciales
        if automata is None or not isinstance(automata, Automata):
            raise ValueError("❌ Error: Se debe proporcionar un autómata válido.")
        if not isinstance(cadena, str):
            raise ValueError("❌ Error: La cadena de entrada debe ser un string.")
        if automata.estado_inicial is None:
            return False  # No hay estado inicial definido
        
        estados_actuales = Validator._cerradura_epsilon({automata.estado_inicial})
        
        if debug:
            print(f"🔹 Estado inicial: {[e.nombre for e in estados_actuales]}")

        # Recorrer la cadena
        for simbolo in cadena:
            nuevos_estados = set()

            for estado in estados_actuales:
                if simbolo in estado.transiciones:
                    nuevos_estados.update(estado.transiciones[simbolo])

            estados_actuales = Validator._cerradura_epsilon(nuevos_estados)

            if debug:
                print(f"🔹 Procesando '{simbolo}': {[e.nombre for e in estados_actuales]}")

            if not estados_actuales:  # Si no hay estados alcanzables, la cadena es rechazada
                return False

        # Si al final hay al menos un estado final, la cadena es aceptada
        resultado = any(estado.es_final for estado in estados_actuales)

        if debug:
            print(f"✅ Resultado: {'Aceptada' if resultado else 'Rechazada'}")

        return resultado

    @staticmethod
    def _cerradura_epsilon(estados):
        """
        Calcula el cierre ε de un conjunto de estados.

        :param estados: Conjunto de estados a analizar.
        :return: Conjunto expandido con la cerradura ε.
        """
        pila = deque(estados)  # Se usa deque para optimizar pop()
        cerradura = set(estados)

        while pila:
            estado = pila.pop()
            if "ε" in estado.transiciones:  # Si hay transiciones ε
                for siguiente in estado.transiciones["ε"]:
                    if siguiente not in cerradura:
                        cerradura.add(siguiente)
                        pila.append(siguiente)

        return cerradura

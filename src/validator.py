from automata import Automata

class Validator:
    @staticmethod
    def validar_cadena(automata, cadena):
        if automata.estado_inicial is None:
            return False  # No hay estado inicial definido
        
        estados_actuales = Validator._cerradura_epsilon({automata.estado_inicial})

        for simbolo in cadena:
            nuevos_estados = set()
            for estado in estados_actuales:
                if simbolo in estado.transiciones:
                    nuevos_estados.update(estado.transiciones[simbolo])

            estados_actuales = Validator._cerradura_epsilon(nuevos_estados)

            if not estados_actuales:  # Si no hay estados a los que moverse, la cadena no es válida
                return False

        return any(estado.es_final for estado in estados_actuales)

    @staticmethod
    def _cerradura_epsilon(estados):
        """
        Calcula el cierre ε de un conjunto de estados.
        """
        pila = list(estados)
        cerradura = set(estados)

        while pila:
            estado = pila.pop()
            if "ε" in estado.transiciones:  # Verifica si hay transiciones vacías
                for siguiente in estado.transiciones["ε"]:
                    if siguiente not in cerradura:
                        cerradura.add(siguiente)
                        pila.append(siguiente)

        return cerradura

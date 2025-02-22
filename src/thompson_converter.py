import string
from automata import Automata

class ThompsonConverter:
    def __init__(self):
        self.state_counter = 0  # Contador para nombres únicos de estados
    
    def _new_state(self):
        """Genera un nuevo estado con un nombre único."""
        name = f"S{self.state_counter}"
        self.state_counter += 1
        return name

    def regex_to_afnd(self, regex):
        """Convierte una expresión regular en un AFND usando el algoritmo de Thompson.
           Añade concatenaciones implícitas cuando es necesario.
        """
        stack = []  
        prev_char = None  

        for char in regex:
            if char in string.ascii_letters or char.isdigit():
                if prev_char and (prev_char in string.ascii_letters or prev_char.isdigit()):
                    # Inserta concatenación implícita
                    stack.append(self._concatenation(stack.pop(), self._create_simple_automata(char)))
                else:
                    stack.append(self._create_simple_automata(char))
            elif char == "*":
                if stack:
                    stack.append(self._kleene_closure(stack.pop()))
            elif char == "|":
                if len(stack) >= 2:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(self._union(a, b))
            elif char == ".":
                if len(stack) >= 2:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(self._concatenation(a, b))
            prev_char = char  

        if len(stack) == 1:
            return stack[0]  
        else:
            raise ValueError("Expresión regular inválida")

    def _create_simple_automata(self, char):
        """Crea un AFND básico para un solo carácter."""
        start = self._new_state()
        end = self._new_state()

        automata = Automata(tipo="AFND")

        # Agregar estados antes de usarlos
        automata.agregar_estado(start)
        automata.agregar_estado(end, es_final=True)

        automata.agregar_transicion(start, char, end)

        # 🔹 Asegurar que el estado inicial se asigna correctamente
        automata.estado_inicial = automata.estados[start]

        return automata

    def _kleene_closure(self, automata):
        """Aplica la cerradura de Kleene (A*) a un AFND."""
        start = self._new_state()
        end = self._new_state()

        new_automata = Automata(tipo="AFND")

        new_automata.agregar_estado(start)
        new_automata.agregar_estado(end, es_final=True)

        new_automata.agregar_transicion(start, "ε", automata.estado_inicial.nombre)
        new_automata.agregar_transicion(start, "ε", end)

        for estado in automata.estados.values():
            if estado.es_final:
                estado.es_final = False
                new_automata.agregar_transicion(estado.nombre, "ε", end)
                new_automata.agregar_transicion(estado.nombre, "ε", automata.estado_inicial.nombre)

        for estado in automata.estados.values():
            new_automata.estados[estado.nombre] = estado

        new_automata.estado_inicial = new_automata.estados[start]  # Asegurar estado inicial

        return new_automata

    def _union(self, a, b):
        """Crea la unión (A | B) de dos AFNDs."""
        start = self._new_state()
        end = self._new_state()

        new_automata = Automata(tipo="AFND")
        new_automata.agregar_estado(start)
        new_automata.agregar_estado(end, es_final=True)

        new_automata.agregar_transicion(start, "ε", a.estado_inicial.nombre)
        new_automata.agregar_transicion(start, "ε", b.estado_inicial.nombre)

        for estado in a.estados.values():
            if estado.es_final:
                estado.es_final = False
                new_automata.agregar_transicion(estado.nombre, "ε", end)

        for estado in b.estados.values():
            if estado.es_final:
                estado.es_final = False
                new_automata.agregar_transicion(estado.nombre, "ε", end)

        for estado in a.estados.values():
            new_automata.estados[estado.nombre] = estado
        for estado in b.estados.values():
            new_automata.estados[estado.nombre] = estado

        new_automata.estado_inicial = new_automata.estados[start]  # Asegurar estado inicial

        return new_automata

    def _concatenation(self, a, b):
        """Concatena dos AFNDs asegurando que los estados finales de A se conecten con el inicio de B."""
        for estado in a.estados.values():
            if estado.es_final:
                estado.es_final = False
                for simbolo, destinos in b.estado_inicial.transiciones.items():
                    for destino in destinos:
                        estado.agregar_transicion(simbolo, destino)

        for estado in b.estados.values():
            a.estados[estado.nombre] = estado

        a.estado_inicial = a.estado_inicial if a.estado_inicial else b.estado_inicial  # Asegurar estado inicial

        return a
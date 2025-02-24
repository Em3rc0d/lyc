from automata import Automata

class RegexToAFND:
    def __init__(self, regex):
        self.regex = regex

    def _add_concat(self, regex):
        """
        Inserta explícitamente el operador de concatenación '.' donde sea necesario.
        Solo se inserta cuando:
         - El carácter actual es alfanumérico, '*' o ')'
         - Y el siguiente carácter es alfanumérico o '('
        Esto evita duplicar el operador cuando ya está explícito.
        """
        result = []
        for i, c in enumerate(regex):
            result.append(c)
            if i + 1 < len(regex):
                c1 = c
                c2 = regex[i + 1]
                if (c1.isalnum() or c1 in ['*', ')']) and (c2.isalnum() or c2 == '('):
                    result.append('.')
        return "".join(result)

    def _to_postfix(self, regex):
        """
        Convierte la expresión regular (con concatenación explícita) a notación postfija
        utilizando el algoritmo de Shunting-yard.
        """
        precedencia = {'*': 3, '.': 2, '|': 1}
        salida = []
        pila = []
        for c in regex:
            if c.isalnum():
                salida.append(c)
            elif c == '(':
                pila.append(c)
            elif c == ')':
                while pila and pila[-1] != '(':
                    salida.append(pila.pop())
                if pila:
                    pila.pop()  # descarta el '('
            else:
                while pila and pila[-1] != '(' and precedencia.get(pila[-1], 0) >= precedencia.get(c, 0):
                    salida.append(pila.pop())
                pila.append(c)
        while pila:
            salida.append(pila.pop())
        return "".join(salida)

    def convert(self):
        """
        Aplica el algoritmo de Thompson para construir un AFND a partir de la expresión regular.
        Se asume que los únicos operadores son:
            - Concatenación ('.')
            - Unión ('|')
            - Kleene star ('*')
        """
        regex_concatenada = self._add_concat(self.regex)
        postfix = self._to_postfix(regex_concatenada)
        stack = []
        for token in postfix:
            if token.isalnum():
                # Crear un AFND simple para el símbolo
                nfa = Automata(tipo="AFND")
                nfa.agregar_estado("s0")
                nfa.agregar_estado("s1", es_final=True)
                nfa.agregar_transicion("s0", token, "s1")
                fragmento = (nfa, "s0", "s1")
                stack.append(fragmento)
            elif token == '.':
                if len(stack) < 2:
                    raise ValueError("Expresión regular inválida: falta operandos para concatenación")
                nfa2, start2, end2 = stack.pop()
                nfa1, start1, end1 = stack.pop()
                # Conectar el final de nfa1 con el inicio de nfa2 mediante una transición epsilon
                nfa1.agregar_transicion(end1, "ε", start2)
                # Fusionar los estados de nfa2 en nfa1
                for estado in nfa2.estados.values():
                    if estado.nombre not in nfa1.estados:
                        nfa1.estados[estado.nombre] = estado
                fragmento = (nfa1, start1, end2)
                stack.append(fragmento)
            elif token == '|':
                if len(stack) < 2:
                    raise ValueError("Expresión regular inválida: falta operandos para unión")
                nfa2, start2, end2 = stack.pop()
                nfa1, start1, end1 = stack.pop()
                nfa = Automata(tipo="AFND")
                nfa.agregar_estado("s_new_start")
                nfa.agregar_estado("s_new_end", es_final=True)
                # Transiciones epsilon desde el nuevo estado inicial a los inicios de nfa1 y nfa2
                nfa.agregar_transicion("s_new_start", "ε", start1)
                nfa.agregar_transicion("s_new_start", "ε", start2)
                # Fusionar los estados de ambos autómatas
                for aut in [nfa1, nfa2]:
                    for estado in aut.estados.values():
                        if estado.nombre not in nfa.estados:
                            nfa.estados[estado.nombre] = estado
                # Transiciones epsilon desde los finales de nfa1 y nfa2 al nuevo estado final
                nfa.agregar_transicion(end1, "ε", "s_new_end")
                nfa.agregar_transicion(end2, "ε", "s_new_end")
                fragmento = (nfa, "s_new_start", "s_new_end")
                stack.append(fragmento)
            elif token == '*':
                if len(stack) < 1:
                    raise ValueError("Expresión regular inválida: falta operando para Kleene star")
                nfa1, start1, end1 = stack.pop()
                nfa = Automata(tipo="AFND")
                nfa.agregar_estado("s_new_start")
                nfa.agregar_estado("s_new_end", es_final=True)
                # Fusionar estados de nfa1 en nfa
                for estado in nfa1.estados.values():
                    if estado.nombre not in nfa.estados:
                        nfa.estados[estado.nombre] = estado
                # Agregar transiciones epsilon para la operación Kleene star
                nfa.agregar_transicion("s_new_start", "ε", start1)
                nfa.agregar_transicion("s_new_start", "ε", "s_new_end")
                nfa.agregar_transicion(end1, "ε", start1)
                nfa.agregar_transicion(end1, "ε", "s_new_end")
                fragmento = (nfa, "s_new_start", "s_new_end")
                stack.append(fragmento)
        if len(stack) != 1:
            raise ValueError("Expresión regular inválida: estructura incorrecta")
        afnd, start, end = stack.pop()
        # Definir el estado inicial y marcar únicamente el estado final correcto
        afnd.estado_inicial = afnd.estados[start]
        for estado in afnd.estados.values():
            estado.es_final = False
        afnd.estados[end].es_final = True
        return afnd

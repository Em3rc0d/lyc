from automata import Automata

class RegexToAFND:
    def __init__(self, regex):
        if not regex or not isinstance(regex, str):
            raise ValueError("❌ Error: La expresión regular debe ser un string válido.")
        self.regex = regex
        self.afnd = None
        self.estado_id = 0  # Contador de estados único

    def nuevo_estado(self):
        """Genera nombres únicos para los estados."""
        nombre = f"s{self.estado_id}"
        self.estado_id += 1
        return nombre

    def _add_concat(self, regex):
        """Inserta explícitamente el operador de concatenación '.' donde sea necesario."""
        resultado = []
        for i in range(len(regex) - 1):
            c1, c2 = regex[i], regex[i + 1]
            resultado.append(c1)
            if (c1.isalnum() or c1 in [')', '*']) and (c2.isalnum() or c2 == '('):
                resultado.append('.')
        resultado.append(regex[-1])
        return "".join(resultado)

    def _to_postfix(self, regex):
        """Convierte la expresión regular en notación postfija usando el algoritmo de Shunting-yard."""
        precedencia = {'*': 3, '.': 2, '|': 1}
        salida, pila = [], []
        for c in regex:
            if c.isalnum():
                salida.append(c)
            elif c == '(':
                pila.append(c)
            elif c == ')':
                while pila and pila[-1] != '(':
                    salida.append(pila.pop())
                pila.pop()  # Quitar '('
            else:
                while pila and pila[-1] != '(' and precedencia[pila[-1]] >= precedencia[c]:
                    salida.append(pila.pop())
                pila.append(c)
        while pila:
            salida.append(pila.pop())
        return "".join(salida)
    
    def convert(self):
        """Convierte la expresión regular a un AFND usando el algoritmo de Thompson."""
        regex_concatenada = self._add_concat(self.regex)
        postfix = self._to_postfix(regex_concatenada)
        stack = []
        estado_id = 0  # Contador para nombres únicos

        def nuevo_estado():
            nonlocal estado_id
            nombre = f"s{estado_id}"
            estado_id += 1
            return nombre

        for token in postfix:
            if token.isalnum():
                nfa = Automata(tipo="AFND")
                inicio, fin = nuevo_estado(), nuevo_estado()
                nfa.agregar_estado(inicio)
                nfa.agregar_estado(fin, es_final=True)
                nfa.agregar_transicion(inicio, token, fin)
                stack.append((nfa, inicio, fin))
            elif token == '.':
                nfa2, start2, end2 = stack.pop()
                nfa1, start1, end1 = stack.pop()

                # Aquí corregimos el problema de referencia a estados
                nfa1.agregar_transicion(end1, "ε", start2)
                nfa1.fusionar(nfa2)
                stack.append((nfa1, start1, end2))
            elif token == '|':
                nfa2, start2, end2 = stack.pop()
                nfa1, start1, end1 = stack.pop()
                nfa = Automata(tipo="AFND")
                nuevo_inicio, nuevo_fin = nuevo_estado(), nuevo_estado()
                nfa.agregar_estado(nuevo_inicio)
                nfa.agregar_estado(nuevo_fin, es_final=True)
                nfa.agregar_transicion(nuevo_inicio, "ε", start1)
                nfa.agregar_transicion(nuevo_inicio, "ε", start2)
                nfa.agregar_transicion(end1, "ε", nuevo_fin)
                nfa.agregar_transicion(end2, "ε", nuevo_fin)
                nfa.fusionar(nfa1)
                nfa.fusionar(nfa2)
                stack.append((nfa, nuevo_inicio, nuevo_fin))
            elif token == '*':
                nfa1, start1, end1 = stack.pop()
                nfa = Automata(tipo="AFND")
                nuevo_inicio, nuevo_fin = nuevo_estado(), nuevo_estado()
                nfa.agregar_estado(nuevo_inicio)
                nfa.agregar_estado(nuevo_fin, es_final=True)
                nfa.agregar_transicion(nuevo_inicio, "ε", start1)
                nfa.agregar_transicion(nuevo_inicio, "ε", nuevo_fin)
                nfa.agregar_transicion(end1, "ε", start1)
                nfa.agregar_transicion(end1, "ε", nuevo_fin)
                nfa.fusionar(nfa1)
                stack.append((nfa, nuevo_inicio, nuevo_fin))

        if len(stack) != 1:
            raise ValueError("❌ Error: La expresión regular es inválida.")

        afnd, start, end = stack.pop()
        afnd.estado_inicial = afnd.estados[start]
        for estado in afnd.estados.values():
            estado.es_final = False
        afnd.estados[end].es_final = True
        self.afnd = afnd
        return afnd


    def convertir(self):
        """Genera y guarda el AFND resultante en self.afnd."""
        return self.convert()

    def mostrar_automata(self):
        if self.afnd:
            self.afnd.mostrar_automata()
        else:
            print("⚠️ No se ha generado el AFND aún.")

    def generar_grafico(self, filename="automata"):
        if self.afnd:
            self.afnd.generar_grafico(filename)
        else:
            print("⚠️ No se ha generado el AFND aún.")

    def validar_cadena(self, cadena):
        if self.afnd and hasattr(self.afnd, "validar_cadena"):
            return self.afnd.validar_cadena(cadena)
        print("⚠️ No se ha generado el AFND o falta método de validación.")
        return False

    def guardar_en_json(self, filepath="automata.json"):
        if self.afnd:
            self.afnd.guardar_en_json(filepath) 
        else:
            print("⚠️ No se ha generado el AFND aun.")

    def cargar_desde_json(self, filepath="automata.json"):  
        self.afnd = AFND()
        self.afnd.cargar_desde_json(filepath)
        return self
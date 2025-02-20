import graphviz

class Visualizer:
    @staticmethod
    def generar_grafico(automata, filename="automata", output_format="png"):
        if not automata.estados:
            print("El autómata no tiene estados, no se generará el gráfico.")
            return
        
        dot = graphviz.Digraph()

        # Agregar un nodo de inicio ficticio para indicar el estado inicial
        dot.node("", shape="none")  
        dot.edge("", automata.estado_inicial.nombre)  

        for estado in automata.estados.values():
            shape = "doublecircle" if estado.es_final else "circle"
            dot.node(estado.nombre, shape=shape)

        for estado in automata.estados.values():
            for simbolo, destinos in estado.transiciones.items():
                for destino in destinos:
                    dot.edge(estado.nombre, destino.nombre, label=simbolo)

        dot.render(filename, format=output_format, cleanup=True)
        print(f"Gráfico guardado como {filename}.{output_format}")

import graphviz

class Visualizer:
    @staticmethod
    def generar_grafico(automata, filename="automata", output_format="png", output_dir="."):
        """
        Genera una representación gráfica del autómata y la guarda en el formato deseado.

        :param automata: Instancia del autómata a visualizar.
        :param filename: Nombre del archivo de salida sin extensión.
        :param output_format: Formato de salida (png, svg, pdf, etc.).
        :param output_dir: Directorio donde se guardará el gráfico.
        """
        # Validaciones iniciales
        if automata is None:
            raise ValueError("❌ Error: Se debe proporcionar un autómata válido.")
        if not automata.estados:
            print("⚠️ Advertencia: El autómata no tiene estados, no se generará el gráfico.")
            return
        if automata.estado_inicial is None:
            print("⚠️ Advertencia: El autómata no tiene un estado inicial definido.")
            return

        dot = graphviz.Digraph(format=output_format)

        # Nodo de inicio ficticio para representar el estado inicial
        dot.node("start", shape="none", label="")
        dot.edge("start", automata.estado_inicial.nombre, label="Inicio", color="blue")

        # Agregar estados con estilos personalizados
        for estado in automata.estados.values():
            shape = "doublecircle" if estado.es_final else "circle"
            color = "red" if estado == automata.estado_inicial else "black"
            dot.node(estado.nombre, shape=shape, color=color)

        # Agregar transiciones
        for estado in automata.estados.values():
            for simbolo, destinos in estado.transiciones.items():
                for destino in destinos:
                    dot.edge(estado.nombre, destino.nombre, label=simbolo)

        # Generar y guardar el archivo
        try:
            filepath = dot.render(directory=output_dir, filename=filename, cleanup=True)
            print(f"✅ Gráfico guardado en: {filepath}")
        except graphviz.ExecutableNotFound:
            print("❌ Error: No se encontró Graphviz. Asegúrate de que está instalado y en el PATH.")
        except Exception as e:
            print(f"❌ Error al generar el gráfico: {e}")

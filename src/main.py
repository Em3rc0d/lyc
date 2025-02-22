from thompson_converter import ThompsonConverter
from afnd_to_afd import AFND_to_AFD
from visualizer import Visualizer

def main():
    try:
        # 🔹 1. Expresión Regular 
        expresion_regular = "ab"  

        # 🔹 2. Convertir ER a AFND
        print(f"\n🔵 Generando AFND desde la expresión regular: '{expresion_regular}'")
        thompson = ThompsonConverter()
        afnd = thompson.regex_to_afnd(expresion_regular)

        # 🔎 Depuración: Imprimir estados del AFND antes de la conversión
        print("\n🔹 AFND Generado:")
        afnd.mostrar_automata()
        Visualizer.generar_grafico(afnd, "assets/automata_afnd_regex")

        print("\n🔎 Depuración: Estados y transiciones del AFND generado:")
        for estado_nombre, estado in afnd.estados.items():
            print(f"Estado: {estado_nombre} {'(Final)' if estado.es_final else ''}")
            for simbolo, destinos in estado.transiciones.items():
                print(f"  {simbolo} -> {[dest.nombre for dest in destinos]}")

        # 🔹 3. Convertir AFND a AFD
        print("\n🔵 Convirtiendo AFND a AFD...")
        conversor = AFND_to_AFD()
        afd = conversor.convertir()

        print("\n🔹 AFD Generado:")
        afd.mostrar_automata()
        Visualizer.generar_grafico(afd, "assets/automata_afd_regex")

        print("\n✅ Conversión de Expresión Regular a Autómata completada con éxito.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

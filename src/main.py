from afnd import AFND
from afnd_to_afd import AFND_to_AFD
from visualizer import Visualizer
import json 
def main():
    try:
        # Ejemplo: generar autómatas a partir de una expresión regular
        regex = input("Ingresa una expresión regular: ")
        
        # Convertir la expresión regular a AFND
        from regex_to_afnd import RegexToAFND
        conversor_regex = RegexToAFND(regex)
        afnd = conversor_regex.convert()
        print("AFND generado a partir de la expresión regular:")
        afnd.mostrar_automata()
        
        # Generar gráfico del AFND
        from visualizer import Visualizer
        Visualizer.generar_grafico(afnd, "assets/automata_afnd_regex")
        
        # Convertir el AFND a AFD
        from afnd_to_afd import AFND_to_AFD
        conversor_afnd = AFND_to_AFD()
        conversor_afnd.afnd = afnd  # Asignamos el AFND generado
        afd = conversor_afnd.convertir()
        afd.guardar_en_json("data/afd_regex.json")
        
        # Generar gráfico del AFD
        Visualizer.generar_grafico(afd, "assets/automata_afd_regex")
        
        print("✅ AFD generado a partir de la expresión regular con éxito.")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

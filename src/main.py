from afnd import AFND
from afnd_to_afd import AFND_to_AFD
from visualizer import Visualizer
import json 
def main():
    try:
        automata = AFND()
        
        # Cargar el autómata desde un archivo JSON
        automata.cargar_desde_json("data/afnd.json")
        automata.mostrar_automata()
        
        # Generar gráfico del AFND
        Visualizer.generar_grafico(automata, "assets/automata_afnd")
        
        # Convertir AFND a AFD
        conversor = AFND_to_AFD()
        conversor.cargar_desde_json("data/afnd.json")
        afd = conversor.convertir()
        afd.guardar_en_json("data/afd.json")
        
        # Generar gráfico del AFD
        Visualizer.generar_grafico(afd, "assets/automata_afd")
        
        print("✅ Autómatas generados y guardados con éxito.")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

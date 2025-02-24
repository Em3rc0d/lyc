from afnd import AFND
from afnd_to_afd import AFND_to_AFD
from regex_to_afnd import RegexToAFND
from visualizer import Visualizer
import json
import logging

# Configuración del logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        regex = input("Ingresa una expresión regular: ")
        logging.info(f"Expresión regular ingresada: {regex}")
        
        # Convertir la expresión regular a AFND
        logging.info("Generando AFND a partir de la expresión regular...")
        conversor_regex = RegexToAFND(regex)
        afnd = conversor_regex.convert()
        
        # Verificar estados generados
        estados_afnd = list(afnd.estados.keys())
        logging.debug(f"Estados generados en el AFND: {estados_afnd}")
        
        # Verificar transiciones
        logging.debug("Transiciones del AFND:")
        for estado, transiciones in afnd.transiciones.items():
            for simbolo, destinos in transiciones.items():
                for destino in destinos:
                    if destino not in afnd.estados:
                        logging.error(f"Error: Estado destino '{destino}' no encontrado. Estados disponibles: {list(afnd.estados.keys())}")
                        raise ValueError(f"Error: Estado destino '{destino}' no encontrado. Estados disponibles: {list(afnd.estados.keys())}")
                    logging.debug(f"  {estado} --{simbolo}--> {destino}")
        
        afnd.mostrar_automata()
        
        # Generar gráfico del AFND
        afnd_path = "assets/automata_afnd_regex"
        Visualizer.generar_grafico(afnd, afnd_path)
        logging.info(f"AFND generado y guardado en {afnd_path}.png")

        # Convertir el AFND a AFD
        logging.info("Convirtiendo AFND a AFD...")
        conversor_afnd = AFND_to_AFD()
        conversor_afnd.afnd = afnd  
        afd = conversor_afnd.convertir()
        
        # Verificar estados generados en el AFD
        estados_afd = list(afd.estados.keys())
        logging.debug(f"Estados generados en el AFD: {estados_afd}")
        
        # Verificar transiciones en el AFD
        logging.debug("Transiciones del AFD:")
        for estado, transiciones in afd.transiciones.items():
            for simbolo, destino in transiciones.items():
                if destino not in afd.estados:
                    logging.error(f"Error: Estado destino '{destino}' no encontrado en AFD. Estados disponibles: {list(afd.estados.keys())}")
                    raise ValueError(f"Error: Estado destino '{destino}' no encontrado en AFD. Estados disponibles: {list(afd.estados.keys())}")
                logging.debug(f"  {estado} --{simbolo}--> {destino}")
        
        # Guardar el AFD en JSON
        afd_json_path = "data/afd_regex.json"
        afd.guardar_en_json(afd_json_path)
        logging.info(f"AFD generado y guardado en {afd_json_path}.")

        # Generar gráfico del AFD
        afd_path = "assets/automata_afd_regex"
        Visualizer.generar_grafico(afd, afd_path)
        logging.info(f"AFD visualizado y guardado en {afd_path}.png")

    except ValueError as ve:
        logging.error(f"Error de validación: {ve}")
    except FileNotFoundError as fe:
        logging.error(f"Archivo no encontrado: {fe}")
    except Exception as e:
        logging.error(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()

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
        
        # Verificar transiciones del AFND
        logging.debug("Transiciones del AFND:")
        for estado_nombre, estado_obj in afnd.estados.items():
            for simbolo, destinos in estado_obj.transiciones.items():
                for destino in destinos:
                    if destino.nombre not in afnd.estados:
                        logging.error(f"Error: Estado destino '{destino.nombre}' no encontrado.")
                        raise ValueError(f"Error: Estado destino '{destino.nombre}' no encontrado.")
                    logging.debug(f"  {estado_nombre} --{simbolo}--> {destino.nombre}")
        
        afnd.mostrar_automata()
        if afnd.estado_inicial is None or afnd.estado_inicial not in afnd.estados:
            logging.error(f"Error: Estado inicial no definido correctamente. Estados actuales: {list(afnd.estados.keys())}")
            raise ValueError("El estado inicial del AFND no fue correctamente definido.")

        # Depuración antes de validar transiciones
        logging.debug(f"Estados en el AFND antes de verificar transiciones: {list(afnd.estados.keys())}")

        # Generar gráfico del AFND
        afnd_path = "assets/automata_afnd_regex"
        Visualizer.generar_grafico(afnd, afnd_path)
        logging.info(f"AFND generado y guardado en {afnd_path}.png")

        # Convertir el AFND a AFD
        logging.info("Convirtiendo AFND a AFD...")
        conversor_afnd = AFND_to_AFD(afnd)  # Pasar el AFND en el constructor
        afd = conversor_afnd.convertir()
        
        logging.debug(f"Estructura del AFND después de la conversión: {json.dumps({k: v.__dict__ for k, v in afnd.estados.items()}, indent=2)}")

        # Verificar transiciones del AFD
        logging.debug("Transiciones del AFD:")
        for estado_nombre, estado_obj in afd.estados.items():
            for simbolo, destino in estado_obj.transiciones.items():
                if destino.nombre not in afd.estados:
                    logging.error(f"Error: Estado destino '{destino.nombre}' no encontrado en AFD.")
                    raise ValueError(f"Error: Estado destino '{destino.nombre}' no encontrado en AFD.")
                logging.debug(f"  {estado_nombre} --{simbolo}--> {destino.nombre}")
                
        # Verificar estados generados en el AFD
        estados_afd = list(afd.estados.keys())
        logging.debug(f"Estados generados en el AFD: {estados_afd}")
        
        # Verificar transiciones en el AFD
        logging.debug("Transiciones del AFD:")
        for estado_nombre, estado_obj in afd.estados.items():
            for simbolo, destino in estado_obj.transiciones.items():
                if destino.nombre not in afd.estados:
                    logging.error(f"Error: Estado destino '{destino.nombre}' no encontrado en AFD.")
                    raise ValueError(f"Error: Estado destino '{destino.nombre}' no encontrado en AFD.")
                logging.debug(f"  {estado_nombre} --{simbolo}--> {destino.nombre}")
        
        # Guardar el AFD en JSON
        afd_json_path = "data/afd_regex.json"
        afd.guardar_automata(afd_json_path)  # Cambié a guardar_automata()
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

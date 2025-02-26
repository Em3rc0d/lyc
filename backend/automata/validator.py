"""
Validación de autómatas y cadenas.
"""
from typing import Set, Dict, List, Any
from .automata import Estado, Automata
from .utils import logger

class Validator:
    """Clase para validar autómatas y cadenas."""
    
    @staticmethod
    def validar_cadena(automata: Automata, cadena: str) -> bool:
        """Valida una cadena con un autómata."""
        return automata.validar_cadena(cadena)
    
    @staticmethod
    def _cerradura_epsilon(estados: Set[Estado]) -> Set[Estado]:
        """Calcula la cerradura epsilon de un conjunto de estados."""
        resultado = set(estados)
        procesados = set()
        por_procesar = list(estados)
        
        while por_procesar:
            actual = por_procesar.pop()
            if actual in procesados:
                continue
                
            procesados.add(actual)
            
            if 'ε' in actual.transiciones:
                for estado in actual.transiciones['ε']:
                    if estado not in procesados:
                        resultado.add(estado)
                        por_procesar.append(estado)
        
        return resultado
    
    @staticmethod
    def validate_automata_structure(automata_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida la estructura de un autómata desde datos JSON.
        Retorna un diccionario con el resultado de la validación.
        """
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Verificar si hay nodos y aristas
        if 'nodes' not in automata_data or not automata_data['nodes']:
            result['is_valid'] = False
            result['errors'].append('No hay nodos definidos en el autómata')
            return result
            
        if 'edges' not in automata_data or not automata_data['edges']:
            result['warnings'].append('No hay transiciones definidas en el autómata')
        
        # Verificar estado inicial
        initial_states = [n for n in automata_data['nodes'] if n.get('initial', False)]
        if not initial_states:
            result['warnings'].append('No hay un estado inicial definido')
        elif len(initial_states) > 1:
            result['warnings'].append(f'Hay múltiples estados iniciales: {", ".join([n["id"] for n in initial_states])}')
        
        # Verificar estados finales
        final_states = [n for n in automata_data['nodes'] if n.get('final', False)]
        if not final_states:
            result['warnings'].append('No hay estados finales definidos')
        
        # Todo parece estar bien
        return result
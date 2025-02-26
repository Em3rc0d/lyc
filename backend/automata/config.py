"""
Configuración centralizada para la aplicación de autómatas.
"""

# Constantes para la aplicación
DEFAULT_ALPHABET = ['a', 'b']
EPSILON = 'ε'

# Mensajes de error comunes
ERROR_MESSAGES = {
    'invalid_structure': 'La estructura del autómata no es válida',
    'no_initial_state': 'No se ha definido un estado inicial',
    'no_final_states': 'No se han definido estados finales',
    'invalid_transition': 'Transición inválida: {0}',
    'state_exists': 'El estado {0} ya existe',
    'state_not_exists': 'El estado {0} no existe',
    'invalid_automata_type': 'Tipo de autómata inválido: debe ser AFD o AFND',
}

# Configuración para serialización
SERIALIZATION_CONFIG = {
    'include_positions': True,
    'include_metadata': True,
}
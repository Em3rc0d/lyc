"""
Utilidades para la aplicación de autómatas.
"""
import logging
import time
from functools import wraps

# Configuración del logger
logger = logging.getLogger('automata')

def setup_logging():
    """Configura el logging para la aplicación de autómatas."""
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def log_execution_time(func):
    """Decorador para registrar el tiempo de ejecución de una función."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"Función {func.__name__} ejecutada en {end_time - start_time:.4f} segundos")
        return result
    return wrapper

# Inicializar logging
setup_logging()
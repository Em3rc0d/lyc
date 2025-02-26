"""
Módulo para gestionar caché en la aplicación.
"""
from functools import lru_cache
import time

class CacheManager:
    """Gestiona diferentes tipos de caché para la aplicación."""
    
    def __init__(self):
        self.transition_cache = {}
        self.validation_cache = {}
        self.last_cleanup = time.time()
    
    def get_transition(self, state, symbol):
        """Obtiene una transición de la caché."""
        key = (state, symbol)
        return self.transition_cache.get(key)
    
    def set_transition(self, state, symbol, target_states):
        """Guarda una transición en la caché."""
        key = (state, symbol)
        self.transition_cache[key] = target_states
    
    def get_validation_result(self, automata_id, input_string):
        """Obtiene un resultado de validación de la caché."""
        key = (automata_id, input_string)
        result, timestamp = self.validation_cache.get(key, (None, 0))
        
        # Invalidar si la caché es muy antigua (30 minutos)
        if time.time() - timestamp > 1800:
            return None
        return result
    
    def set_validation_result(self, automata_id, input_string, result):
        """Guarda un resultado de validación en la caché."""
        key = (automata_id, input_string)
        self.validation_cache[key] = (result, time.time())
    
    def cleanup(self, force=False):
        """Limpia entradas antiguas de la caché."""
        if force or (time.time() - self.last_cleanup > 3600):  # Limpiar cada hora
            now = time.time()
            
            # Limpiar caché de validación
            self.validation_cache = {
                k: v for k, v in self.validation_cache.items()
                if now - v[1] <= 1800  # Mantener solo entradas de los últimos 30 min
            }
            
            self.last_cleanup = now

# Crear una instancia global
cache_manager = CacheManager()
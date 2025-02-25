from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field

@dataclass
class Estado:
    nombre: str
    es_final: bool = False
    transiciones: Dict[str, List['Estado']] = field(default_factory=dict)

    def __str__(self):
        return f"Estado {self.nombre}"

    def __repr__(self):
        return f"Estado({self.nombre})"

    def __hash__(self):
        return hash(self.nombre)

    def __eq__(self, other):
        if not isinstance(other, Estado):
            return False
        return self.nombre == other.nombre

    def agregar_transicion(self, simbolo: str, estado_destino: 'Estado') -> None:
        if not isinstance(simbolo, str) or not isinstance(estado_destino, Estado):
            raise ValueError("Tipos de datos inválidos")

        if simbolo not in self.transiciones:
            self.transiciones[simbolo] = []
        if estado_destino not in self.transiciones[simbolo]:
            self.transiciones[simbolo].append(estado_destino)

class Automata:
    def __init__(self, tipo: str = 'AFND'):
        if tipo not in ['AFND', 'AFD']:
            raise ValueError("Tipo de autómata inválido")

        self.tipo = tipo
        self.estados: Dict[str, Estado] = {}
        self.estado_inicial: Optional[Estado] = None
        self.alfabeto: Set[str] = set()

    def agregar_estado(self, nombre: str, es_final: bool = False) -> None:
        if not isinstance(nombre, str):
            raise ValueError("El nombre del estado debe ser una cadena")

        if nombre in self.estados:
            raise ValueError(f"El estado '{nombre}' ya existe")

        nuevo_estado = Estado(nombre, es_final)
        self.estados[nombre] = nuevo_estado

        # Solo establecer como inicial si es el primer estado y no hay otro inicial
        if not self.estados or self.estado_inicial is None:
            self.estado_inicial = nuevo_estado

        return nuevo_estado

    def agregar_transicion(self, origen: str, simbolo: str, destino: str) -> 'Automata':
        if not all(isinstance(x, str) for x in [origen, simbolo, destino]):
            raise ValueError("Todos los argumentos deben ser cadenas")

        if origen not in self.estados or destino not in self.estados:
            raise ValueError("Estado origen o destino no existe")

        if self.tipo == 'AFD' and simbolo in self.estados[origen].transiciones:
            raise ValueError(f"El AFD ya tiene una transición para el símbolo {simbolo}")

        self.estados[origen].agregar_transicion(simbolo, self.estados[destino])
        self.alfabeto.add(simbolo)
        return self

    def es_deterministico(self) -> bool:
        for estado in self.estados.values():
            for transiciones in estado.transiciones.values():
                if len(transiciones) > 1:
                    return False
        return True

    def validar_estructura(self) -> bool:
        if not self.estado_inicial:
            return False

        if not any(estado.es_final for estado in self.estados.values()):
            return False

        for estado in self.estados.values():
            for destinos in estado.transiciones.values():
                if not all(destino in self.estados.values() for destino in destinos):
                    return False
        return True

    def mostrar_automata(self):
        print(f"Tipo: {self.tipo}")
        print(f"Estado inicial: {self.estado_inicial.nombre if self.estado_inicial else 'Ninguno'}")

        for estado in self.estados.values():
            transiciones_str = ", ".join(
                f"{simbolo} -> {', '.join(dest.nombre for dest in destinos)}"
                for simbolo, destinos in estado.transiciones.items()
            )
            print(f"Estado {estado.nombre} {'(Final)' if estado.es_final else ''}: {transiciones_str}")

        return self

    def obtener_transiciones(self):
        return {
            estado.nombre: {
                simbolo: [dest.nombre for dest in destinos]
                for simbolo, destinos in estado.transiciones.items()
            }
            for estado in self.estados.values()
        }

    def validar_cadena(self, cadena: str) -> bool:
        """Valida una cadena en el autómata."""
        if not self.estado_inicial:
            print("No hay estado inicial definido")
            return False

        if not any(estado.es_final for estado in self.estados.values()):
            print("No hay estados finales definidos")
            return False

        try:
            if self.tipo == 'AFD':
                return self._validar_cadena_afd(cadena)
            else:
                return self._validar_cadena_afnd(cadena)
        except Exception as e:
            print(f"Error al validar cadena: {e}")
            return False

    def _validar_cadena_afd(self, cadena: str) -> bool:
        estado_actual = self.estado_inicial
        
        for simbolo in cadena:
            if simbolo not in estado_actual.transiciones:
                return False
            estado_actual = estado_actual.transiciones[simbolo][0]
        
        return estado_actual.es_final

    def _validar_cadena_afnd(self, cadena: str) -> bool:
        estados_actuales = {self.estado_inicial}
        print(f"Estado inicial: {self.estado_inicial.nombre}")
        
        for simbolo in cadena:
            print(f"Procesando símbolo: {simbolo}")
            nuevos_estados = set()
            
            for estado in estados_actuales:
                print(f"Evaluando estado: {estado.nombre}")
                if simbolo in estado.transiciones:
                    nuevos_estados.update(estado.transiciones[simbolo])
                    print(f"Nuevos estados para {simbolo}: {[e.nombre for e in nuevos_estados]}")
            
            if not nuevos_estados:
                print(f"No hay transiciones válidas para {simbolo}")
                return False
                
            estados_actuales = nuevos_estados
        
        tiene_final = any(estado.es_final for estado in estados_actuales)
        print(f"Estados finales alcanzados: {tiene_final}")
        return tiene_final
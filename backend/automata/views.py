"""
Vistas para la API de autómatas.
"""
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .automata import Automata
from .afnd_to_afd import AFND_to_AFD
from .models import AutomataModel
from .utils import logger, log_execution_time
from .validator import Validator
from .cache import cache_manager


@api_view(['POST'])
@log_execution_time
def validate(request):
    """
    Valida una cadena de entrada con un autómata.
    Espera un JSON con:
    - input: Cadena a validar
    - automataType: Tipo de autómata (AFND o AFD)
    - automataData: Datos del autómata (nodos y aristas)
    """
    try:
        input_string = request.data.get('input', '')
        automata_type = request.data.get('automataType', 'AFND')
        automata_data = request.data.get('automataData', {})
        automata_id = request.data.get('automataId')
        
        # Intentar obtener resultado desde caché si es posible
        if automata_id:
            cached_result = cache_manager.get_validation_result(automata_id, input_string)
            if cached_result is not None:
                logger.info(f"Resultado obtenido desde caché para automata_id={automata_id}, input={input_string}")
                return Response({
                    'isValid': cached_result,
                    'fromCache': True
                })
        
        # Validar estructura del autómata
        validation_result = Validator.validate_automata_structure(automata_data)
        if not validation_result['is_valid']:
            return Response({
                'isValid': False,
                'errors': validation_result['errors']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Construir autómata
        automata = build_automata_from_data(automata_data, automata_type)
        
        # Validar cadena
        is_valid = automata.validar_cadena(input_string)
        
        # Guardar en caché
        if automata_id:
            cache_manager.set_validation_result(automata_id, input_string, is_valid)
        
        return Response({
            'isValid': is_valid,
            'warnings': validation_result.get('warnings', [])
        })
        
    except Exception as e:
        logger.error(f"Error validando cadena: {str(e)}")
        return Response({
            'isValid': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@log_execution_time
def convert_automata(request):
    """
    Convierte un AFND a AFD.
    Espera un JSON con nodos y aristas del AFND.
    """
    try:
        nodes = request.data.get('nodes', [])
        edges = request.data.get('edges', [])
        
        # Validar datos de entrada
        if not nodes or not edges:
            return Response({
                'error': 'Se requieren nodos y aristas para la conversión'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Construir AFND
        afnd = build_automata_from_data({'nodes': nodes, 'edges': edges}, 'AFND')
        
        # Convertir a AFD
        converter = AFND_to_AFD()
        converter.afnd = afnd
        afd = converter.convertir()
        
        # Convertir autómata a formato de respuesta
        result = automata_to_data(afd)
        
        return Response(result)
        
    except Exception as e:
        logger.error(f"Error convirtiendo autómata: {str(e)}")
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def save_automata(request):
    """
    Guarda un autómata en la base de datos.
    """
    try:
        name = request.data.get('name', 'Sin nombre')
        description = request.data.get('description', '')
        automata_type = request.data.get('automataType', 'AFND')
        nodes = request.data.get('nodes', [])
        edges = request.data.get('edges', [])
        
        # Validar datos
        if not nodes or not edges:
            return Response({
                'error': 'Se requieren nodos y aristas para guardar el autómata'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Si se proporciona un ID, actualizar en lugar de crear
        automata_id = request.data.get('id')
        if automata_id:
            automata = get_object_or_404(AutomataModel, id=automata_id)
            automata.name = name
            automata.description = description
            automata.automata_type = automata_type
            automata.nodes = nodes
            automata.edges = edges
            automata.save()
            msg = "Autómata actualizado correctamente"
        else:
            # Crear nuevo autómata
            automata = AutomataModel.objects.create(
                name=name,
                description=description,
                automata_type=automata_type,
                nodes=nodes,
                edges=edges
            )
            msg = "Autómata guardado correctamente"
        
        return Response({
            'success': True,
            'message': msg,
            'id': automata.id
        })
        
    except Exception as e:
        logger.error(f"Error guardando autómata: {str(e)}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def load_automata(request):
    """
    Carga autómatas de la base de datos.
    Si se proporciona un ID, carga un autómata específico.
    De lo contrario, devuelve una lista de todos los autómatas.
    """
    try:
        automata_id = request.query_params.get('id')
        
        if automata_id:
            # Cargar un autómata específico
            automata = get_object_or_404(AutomataModel, id=automata_id)
            return Response(automata.to_dict)
        else:
            # Listar todos los autómatas
            automatas = AutomataModel.objects.all().order_by('-updated_at')
            return Response([a.to_dict for a in automatas])
        
    except Exception as e:
        logger.error(f"Error cargando autómata(s): {str(e)}")
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


def build_automata_from_data(data, automata_type='AFND'):
    """
    Construye un objeto Automata a partir de datos de entrada.
    """
    automata = Automata(tipo=automata_type)
    
    # Primero, crear todos los estados
    for node in data['nodes']:
        automata.agregar_estado(node['id'], node.get('final', False))
    
    # Establecer el estado inicial
    for node in data['nodes']:
        if node.get('initial', False):
            automata.estado_inicial = automata.estados[node['id']]
            break
    
    # Agregar transiciones
    for edge in data['edges']:
        automata.agregar_transicion(edge['from'], edge.get('label', 'ε'), edge['to'])
    
    return automata


def automata_to_data(automata):
    """
    Convierte un objeto Automata a formato JSON para la API.
    """
    nodes = []
    edges = []
    
    # Crear nodos
    for nombre, estado in automata.estados.items():
        nodes.append({
            'id': nombre,
            'label': nombre,
            'initial': estado == automata.estado_inicial,
            'final': estado.es_final
        })
    
    # Crear aristas
    for nombre, estado in automata.estados.items():
        for simbolo, destinos in estado.transiciones.items():
            for destino in destinos:
                edges.append({
                    'from': nombre,
                    'to': destino.nombre,
                    'label': simbolo
                })
    
    return {
        'nodes': nodes,
        'edges': edges
    }
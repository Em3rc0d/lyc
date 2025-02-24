from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .automata import Automata
from .afnd_to_afd import AFND_to_AFD

@api_view(['POST'])
@csrf_exempt
def validate(request):
    try:
        # Logging detallado
        print("Received data:", request.data)
        
        data = request.data
        input_string = data.get('input', '')
        automata_type = data.get('automataType', 'AFND')
        automata_data = data.get('automataData', {})

        # Validación básica
        if not automata_data or 'nodes' not in automata_data or 'edges' not in automata_data:
            return Response({
                'error': 'Datos del autómata incompletos',
                'message': 'Se requieren nodos y aristas'
            }, status=400)

        # Crear el autómata
        automata = Automata(tipo=automata_type)
        initial_state = None
        final_states = []

        # Primero creamos todos los estados
        for node in automata_data['nodes']:
            estado_id = str(node['id'])
            es_final = node.get('final', False)
            es_inicial = node.get('initial', False)
            
            estado = automata.agregar_estado(estado_id, es_final=es_final)
            
            if es_inicial:
                initial_state = estado
                automata.estado_inicial = estado
            if es_final:
                final_states.append(estado)

        # Verificar estado inicial
        if not initial_state:
            return Response({
                'error': 'Estado inicial no definido',
                'message': 'El autómata debe tener un estado inicial'
            }, status=400)

        print(f"Estado inicial: {initial_state.nombre}")

        # Verificar estados finales
        if not final_states:
            if len(automata.estados) > 1:
                last_state_id = list(automata.estados.keys())[-1]
                estado_final_candidate = automata.estados[last_state_id]
                # Solo asignar si no es el estado inicial
                if estado_final_candidate != initial_state:
                    estado_final_candidate.es_final = True
                    final_states.append(estado_final_candidate)
                    print(f"No se definieron estados finales; se asigna el estado '{estado_final_candidate.nombre}' como final")
                else:
                    initial_state.es_final = True
                    final_states.append(initial_state)
                    print("No se definieron estados finales; se asigna el estado inicial como final")
            else:
                initial_state.es_final = True
                final_states.append(initial_state)
                print("No se definieron estados finales; se asigna el estado inicial como final")

        # Agregar transiciones
        for edge in automata_data['edges']:
            from_state = str(edge['from'])
            to_state = str(edge['to'])
            symbol = str(edge['label'])

            if not symbol:
                continue  # Ignorar transiciones vacías

            try:
                automata.agregar_transicion(from_state, symbol, to_state)
            except Exception as e:
                print(f"Error adding transition: {str(e)}")
                return Response({
                    'error': 'Error en transición',
                    'message': str(e)
                }, status=400)

        # Validar la cadena
        is_valid = automata.validar_cadena(input_string)
        print(f"Validation result for '{input_string}': {is_valid}")

        return Response({
            'isValid': is_valid,
            'message': '¡Cadena válida!' if is_valid else 'Cadena no válida'
        })

    except Exception as e:
        print(f"Error in validate view: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return Response({
            'error': 'Error interno del servidor',
            'message': str(e)
        }, status=500)

@api_view(['POST'])
def convert_automata(request):
    try:
        data = request.data
        afnd = Automata(tipo='AFND')

        for node in data['nodes']:
            afnd.agregar_estado(node['id'], node.get('shape') == 'doublecircle')

        for edge in data['edges']:
            afnd.agregar_transicion(edge['from'], edge['label'], edge['to'])

        converter = AFND_to_AFD()
        converter.afnd = afnd
        afd = converter.convertir()

        return Response({
            'nodes': [{'id': estado.nombre, 'label': estado.nombre,
                       'shape': 'doublecircle' if estado.es_final else 'circle'}
                      for estado in afd.estados.values()],
            'edges': [{'from': estado.nombre, 'to': destino.nombre, 'label': simbolo}
                      for estado in afd.estados.values()
                      for simbolo, destinos in estado.transiciones.items()
                      for destino in destinos]
        })

    except Exception as e:
        return Response({'error': str(e)}, status=400)
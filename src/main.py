from flask import Flask, request, jsonify
from flask_cors import CORS
from automata import Automata
from afnd_to_afd import AFND_to_AFD
from functools import lru_cache

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Caché para el AFND
_automata_cache = {}

@lru_cache(maxsize=128)
def get_or_create_automata(automata_type, cache_key=None):
    if automata_type == 'AFND':
        if cache_key and cache_key in _automata_cache:
            return _automata_cache[cache_key]
        automata = Automata(tipo='AFND')
        if cache_key:
            _automata_cache[cache_key] = automata
        return automata
    else:
        converter = AFND_to_AFD()
        return converter.convertir()

@app.route('/validate', methods=['OPTIONS', 'POST'])
def validate():
    # Manejo de CORS preflight
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Methods'] = 'POST'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    try:
        data = request.get_json(force=True)
        if not isinstance(data, dict):
            return jsonify({'error': 'Datos inválidos'}), 400

        input_string = data.get('input')
        automata_type = data.get('automataType')

        # Validaciones
        if not isinstance(input_string, str):
            return jsonify({'error': 'input debe ser una cadena'}), 400
            
        if not isinstance(automata_type, str):
            return jsonify({'error': 'automataType debe ser una cadena'}), 400

        if automata_type not in ['AFND', 'AFD']:
            return jsonify({'error': 'automataType debe ser AFND o AFD'}), 400

        if not all(c in ['a', 'b'] for c in input_string):
            return jsonify({
                'error': 'La cadena solo puede contener los símbolos "a" y "b"',
                'isValid': False
            }), 400

        # Crear el autómata correspondiente 
        automata = get_or_create_automata(automata_type)
        is_valid = automata.validar_cadena(input_string)
        
        return jsonify({
            'isValid': is_valid,
            'message': '¡Cadena válida!' if is_valid else 'Cadena no válida'
        })

    except Exception as e:
        print(f"Error en validate: {str(e)}")
        return jsonify({
            'error': str(e),
            'message': 'Error al procesar la solicitud',
            'isValid': False
        }), 400

@app.route('/automata/convert', methods=['POST'])
def convert_automata():
    try:
        data = request.json
        cache_key = str(sorted([(n['id'], n.get('shape', '')) for n in data['nodes']] +
                             [(e['from'], e['to'], e['label']) for e in data['edges']]))
        
        # Intentar obtener del caché
        if cache_key in _automata_cache:
            afd = _automata_cache[cache_key]
        else:
            afnd = get_or_create_automata('AFND')
            
            # Crear AFND desde los datos recibidos
            for node in data['nodes']:
                afnd.agregar_estado(node['id'], node.get('shape') == 'doublecircle')
                
            for edge in data['edges']:
                afnd.agregar_transicion(edge['from'], edge['label'], edge['to'])
                
            # Convertir a AFD y guardar en caché
            converter = AFND_to_AFD()
            converter.afnd = afnd
            afd = converter.convertir()
            _automata_cache[cache_key] = afd
        
        return jsonify({
            'nodes': [{'id': estado.nombre, 'label': estado.nombre, 
                      'shape': 'doublecircle' if estado.es_final else 'circle'}
                     for estado in afd.estados.values()],
            'edges': [{'from': estado.nombre, 'to': destino.nombre, 'label': simbolo}
                     for estado in afd.estados.values()
                     for simbolo, destinos in estado.transiciones.items()
                     for destino in destinos]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

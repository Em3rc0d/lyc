from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import json

from .automata import Automata, Estado
from .afnd_to_afd import AFND_to_AFD
from .models import AutomataModel

class AutomataTest(TestCase):
    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Crear un AFND que acepta cadenas que terminan en 'ab'
        self.afnd = Automata(tipo='AFND')
        self.afnd.agregar_estado('q0', es_final=False)
        self.afnd.agregar_estado('q1', es_final=False)
        self.afnd.agregar_estado('q2', es_final=True)
        
        self.afnd.agregar_transicion('q0', 'a', 'q0')
        self.afnd.agregar_transicion('q0', 'b', 'q0')
        self.afnd.agregar_transicion('q0', 'a', 'q1')
        self.afnd.agregar_transicion('q1', 'b', 'q2')
        
        # Crear un AFD simple que acepta cadenas con un número par de 'a's
        self.afd = Automata(tipo='AFD')
        self.afd.agregar_estado('p0', es_final=True)
        self.afd.agregar_estado('p1', es_final=False)
        
        self.afd.agregar_transicion('p0', 'a', 'p1')
        self.afd.agregar_transicion('p0', 'b', 'p0')
        self.afd.agregar_transicion('p1', 'a', 'p0')
        self.afd.agregar_transicion('p1', 'b', 'p1')
    
    def test_validar_cadena_afnd(self):
        """Prueba validación de cadenas con AFND."""
        self.assertTrue(self.afnd.validar_cadena('ab'))
        self.assertTrue(self.afnd.validar_cadena('aab'))
        self.assertTrue(self.afnd.validar_cadena('ababab'))
        self.assertFalse(self.afnd.validar_cadena('a'))
        self.assertFalse(self.afnd.validar_cadena('ba'))
        self.assertFalse(self.afnd.validar_cadena(''))
    
    def test_validar_cadena_afd(self):
        """Prueba validación de cadenas con AFD."""
        self.assertTrue(self.afd.validar_cadena(''))  # Cadena vacía (0 a's)
        self.assertFalse(self.afd.validar_cadena('a'))  # 1 'a'
        self.assertTrue(self.afd.validar_cadena('aa'))  # 2 'a's
        self.assertTrue(self.afd.validar_cadena('b'))  # 0 'a's
        self.assertTrue(self.afd.validar_cadena('baba'))  # 2 'a's
    
    def test_conversion_afnd_to_afd(self):
        """Prueba conversión de AFND a AFD."""
        converter = AFND_to_AFD()
        converter.afnd = self.afnd
        afd = converter.convertir()
        
        self.assertEqual(afd.tipo, 'AFD')
        self.assertTrue(afd.validar_cadena('ab'))
        self.assertTrue(afd.validar_cadena('aab'))
        self.assertFalse(afd.validar_cadena('a'))
    
    def test_minimizacion_afd(self):
        """Prueba minimización de un AFD."""
        # Creamos un AFD que puede ser minimizado
        afd = Automata(tipo='AFD')
        afd.agregar_estado('q0', es_final=False)
        afd.agregar_estado('q1', es_final=False)
        afd.agregar_estado('q2', es_final=True)
        afd.agregar_estado('q3', es_final=True)
        
        afd.agregar_transicion('q0', 'a', 'q1')
        afd.agregar_transicion('q0', 'b', 'q2')
        afd.agregar_transicion('q1', 'a', 'q1')
        afd.agregar_transicion('q1', 'b', 'q3')
        afd.agregar_transicion('q2', 'a', 'q1')
        afd.agregar_transicion('q2', 'b', 'q3')
        afd.agregar_transicion('q3', 'a', 'q1')
        afd.agregar_transicion('q3', 'b', 'q3')
        
        afd_min = afd.minimizar()
        
        # Verificar que el AFD minimizado conserva la funcionalidad
        self.assertTrue(afd_min.validar_cadena('b'))
        self.assertTrue(afd_min.validar_cadena('bb'))
        self.assertTrue(afd_min.validar_cadena('ab'))
        self.assertFalse(afd_min.validar_cadena('a'))
        self.assertFalse(afd_min.validar_cadena('aa'))
        
        # Y tiene menos estados
        self.assertLess(len(afd_min.estados), len(afd.estados))


class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_automata = {
            'name': 'Test Automaton',
            'description': 'Test description',
            'automataType': 'AFND',
            'nodes': [
                {'id': 'q0', 'label': 'q0', 'initial': True},
                {'id': 'q1', 'label': 'q1'},
                {'id': 'q2', 'label': 'q2', 'final': True}
            ],
            'edges': [
                {'from': 'q0', 'to': 'q0', 'label': 'a'},
                {'from': 'q0', 'to': 'q1', 'label': 'a'},
                {'from': 'q0', 'to': 'q0', 'label': 'b'},
                {'from': 'q1', 'to': 'q2', 'label': 'b'}
            ]
        }
        
    def test_validate_api(self):
        """Prueba el endpoint de validación de cadenas."""
        data = {
            'input': 'ab',
            'automataType': 'AFND',
            'automataData': {
                'nodes': self.test_automata['nodes'],
                'edges': self.test_automata['edges']
            }
        }
        
        response = self.client.post('/automata/validate/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['isValid'])
        
        # Cadena inválida
        data['input'] = 'a'
        response = self.client.post('/automata/validate/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['isValid'])
    
    def test_convert_api(self):
        """Prueba el endpoint de conversión AFND a AFD."""
        data = {
            'nodes': self.test_automata['nodes'],
            'edges': self.test_automata['edges']
        }
        
        response = self.client.post('/automata/convert/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('nodes', response.data)
        self.assertIn('edges', response.data)
    
    def test_save_load_api(self):
        """Prueba los endpoints de guardar y cargar autómatas."""
        # Guardar autómata
        response = self.client.post('/automata/save/', self.test_automata, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        automata_id = response.data['id']
        
        # Cargar autómata
        response = self.client.get(f'/automata/load/?id={automata_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.test_automata['name'])
        self.assertEqual(response.data['automataType'], self.test_automata['automataType'])
        
        # Listar autómatas
        response = self.client.get('/automata/load/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
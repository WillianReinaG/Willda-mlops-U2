"""
Pruebas unitarias para el módulo de diagnóstico médico
"""
import pytest
import sys
import os
import json
from datetime import datetime
from collections import Counter

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Diagnostico import diagnostico
from app import app, obtener_reporte


class TestDiagnostico:
    """Pruebas para la función de diagnóstico"""
    
    def test_no_enfermo(self):
        """Prueba que valores bajos retornen NO ENFERMO"""
        resultado = diagnostico(2, 3, 4)
        assert resultado == "NO ENFERMO"
    
    def test_enfermo_leve(self):
        """Prueba que valores medios bajos retornen ENFERMO LEVE"""
        resultado = diagnostico(5, 5, 5)
        assert resultado == "ENFERMO LEVE"
    
    def test_enfermo_agudo(self):
        """Prueba que valores medios retornen ENFERMO AGUDO"""
        resultado = diagnostico(8, 8, 8)
        assert resultado == "ENFERMO AGUDO"
    
    def test_enfermo_cronico(self):
        """Prueba que valores altos retornen ENFERMO CRONICO"""
        resultado = diagnostico(10, 11, 12)
        assert resultado == "ENFERMO CRONICO"
    
    def test_enfermedad_terminal(self):
        """Prueba que valores muy altos retornen ENFERMEDAD TERMINAL"""
        resultado = diagnostico(15, 15, 15)
        assert resultado == "ENFERMEDAD TERMINAL"


class TestAPI:
    """Pruebas para la API Flask"""
    
    @pytest.fixture
    def client(self):
        """Fixture para crear un cliente de prueba"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_health_endpoint(self, client):
        """Prueba que el endpoint de salud funcione"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_predict_post_endpoint(self, client):
        """Prueba el endpoint POST de predicción"""
        response = client.post('/api/predict',
                             json={'valor1': 5, 'valor2': 8, 'valor3': 12},
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'diagnostico' in data
        assert 'suma' in data
        assert data['suma'] == 25
    
    def test_predict_get_endpoint(self, client):
        """Prueba el endpoint GET de predicción"""
        response = client.get('/api/predict?valor1=3&valor2=4&valor3=5')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'diagnostico' in data
        assert data['suma'] == 12


class TestReporte:
    """Pruebas para el sistema de reportes - REQUERIDO"""
    
    @pytest.fixture
    def client(self):
        """Fixture para crear un cliente de prueba"""
        app.config['TESTING'] = True
        
        # Limpiar archivo de registro antes de cada prueba
        registro_file = "registro_predicciones.txt"
        if os.path.exists(registro_file):
            os.remove(registro_file)
        
        with app.test_client() as client:
            yield client
    
    def test_prediccion_registra_enfermedad(self, client):
        """PRUEBA 1: Realizar una predicción que arroje algún tipo de enfermedad
        y verificar que se registre correctamente"""
        
        # Realizar predicción que arroje enfermedad (ENFERMO LEVE: suma = 15)
        response = client.post('/api/predict',
                             json={'valor1': 5, 'valor2': 5, 'valor3': 5},
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['diagnostico'] == "ENFERMO LEVE"
        
        # Verificar que se registró en el archivo
        assert os.path.exists("registro_predicciones.txt")
        
        with open("registro_predicciones.txt", "r", encoding="utf-8") as f:
            line = f.readline().strip()
            registro = json.loads(line)
            assert registro['prediccion'] == "ENFERMO LEVE"
            assert registro['suma'] == 15
            assert 'fecha' in registro
    
    def test_estadisticas_ultimos_10_historicos(self, client):
        """PRUEBA 2: Generar 12 predicciones y chequear las estadísticas 
        de los últimos 10 datos históricos"""
        
        # Generar 12 predicciones con diferentes categorías
        predicciones = [
            (2, 3, 4),   # NO ENFERMO (9)
            (5, 5, 5),   # ENFERMO LEVE (15)
            (8, 8, 8),   # ENFERMO AGUDO (24)
            (10, 11, 9), # ENFERMO AGUDO (30)
            (11, 11, 11), # ENFERMO CRONICO (33)
            (15, 15, 15), # ENFERMEDAD TERMINAL (45)
            (3, 3, 3),   # NO ENFERMO (9)
            (6, 6, 6),   # ENFERMO LEVE (18)
            (7, 7, 7),   # ENFERMO AGUDO (21)
            (12, 12, 12), # ENFERMO CRONICO (36)
            (4, 4, 4),   # NO ENFERMO (12) - esta no debería estar en últimas 10
            (9, 9, 9),   # ENFERMO AGUDO (27) - esta tampoco
        ]
        
        for v1, v2, v3 in predicciones:
            client.post('/api/predict',
                       json={'valor1': v1, 'valor2': v2, 'valor3': v3},
                       content_type='application/json')
        
        # Obtener reporte
        response = client.get('/api/report')
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Verificar que tenemos estadísticas
        assert 'total_por_categoria' in data
        assert 'ultimas_5' in data  # API retorna últimas 5, pero verificamos que funcione
        
        # Verificar que las últimas 5 son las últimas realizadas
        ultimas = data['ultimas_5']
        assert len(ultimas) == 5
        
        # Verificar que la última predicción es la número 12 (9, 9, 9)
        assert ultimas[-1]['valor1'] == 9
        assert ultimas[-1]['valor2'] == 9
        assert ultimas[-1]['valor3'] == 9
        assert ultimas[-1]['prediccion'] == "ENFERMO AGUDO"
        
        # Verificar que tenemos conteo por categoría
        conteo = data['total_por_categoria']
        assert isinstance(conteo, dict)
        assert len(conteo) > 0
        
        # Verificar que tenemos fecha de última predicción
        assert 'fecha_ultima_prediccion' in data
        assert data['fecha_ultima_prediccion'] is not None
        
        # Verificar que la función obtener_reporte funciona correctamente
        conteo_directo, ultimas_directo, fecha_directa = obtener_reporte()
        
        # Debería haber 12 registros totales
        total_registros = sum(conteo_directo.values())
        assert total_registros == 12
        
        # Verificar que las últimas 5 son correctas
        assert len(ultimas_directo) == 5
        
        # Verificar que la última es la predicción 12
        assert ultimas_directo[-1]['valor1'] == 9


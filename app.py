from flask import Flask, render_template, request, jsonify
import sys
import os

# Agregar el directorio actual al path para importar Diagnostico
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Diagnostico import diagnostico

app = Flask(__name__)

@app.route('/')
def index():
    """Página principal con formulario para diagnóstico"""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """Endpoint API REST para predecir el estado de salud"""
    try:
        # Obtener datos del request
        data = request.get_json()
        
        # Validar que se proporcionen los cinco valores
        required_fields = ['edad', 'temperatura', 'frecuencia_cardiaca', 'glucosa', 'presion_arterial']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'error': f'Se requieren los valores: {", ".join(required_fields)}'
            }), 400
        
        # Extraer valores
        edad = float(data['edad'])
        temperatura = float(data['temperatura'])
        frecuencia_cardiaca = float(data['frecuencia_cardiaca'])
        glucosa = float(data['glucosa'])
        presion_arterial = float(data['presion_arterial'])
        
        # Validar que los valores sean números válidos
        if not all(isinstance(val, (int, float)) for val in [edad, temperatura, frecuencia_cardiaca, glucosa, presion_arterial]):
            return jsonify({
                'error': 'Todos los valores deben ser números'
            }), 400
        
        # Realizar diagnóstico
        resultado = diagnostico(edad, temperatura, frecuencia_cardiaca, glucosa, presion_arterial)
        
        return jsonify({
            'diagnostico': resultado,
            'edad': edad,
            'temperatura': temperatura,
            'frecuencia_cardiaca': frecuencia_cardiaca,
            'glucosa': glucosa,
            'presion_arterial': presion_arterial,
            'mensaje': 'Diagnóstico realizado con éxito'
        })
        
    except ValueError as e:
        return jsonify({
            'error': f'Error en los datos proporcionados: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'error': f'Error interno del servidor: {str(e)}'
        }), 500

@app.route('/api/predict', methods=['GET'])
def predict_get():
    """Endpoint GET para diagnóstico con parámetros de query"""
    try:
        # Obtener parámetros de la URL
        edad = request.args.get('edad', type=float)
        temperatura = request.args.get('temperatura', type=float)
        frecuencia_cardiaca = request.args.get('frecuencia_cardiaca', type=float)
        glucosa = request.args.get('glucosa', type=float)
        presion_arterial = request.args.get('presion_arterial', type=float)
        
        # Validar que se proporcionen los cinco valores
        if None in [edad, temperatura, frecuencia_cardiaca, glucosa, presion_arterial]:
            return jsonify({
                'error': 'Se requieren los parámetros: edad, temperatura, frecuencia_cardiaca, glucosa, presion_arterial en la URL'
            }), 400
        
        # Realizar diagnóstico
        resultado = diagnostico(edad, temperatura, frecuencia_cardiaca, glucosa, presion_arterial)
        
        return jsonify({
            'diagnostico': resultado,
            'edad': edad,
            'temperatura': temperatura,
            'frecuencia_cardiaca': frecuencia_cardiaca,
            'glucosa': glucosa,
            'presion_arterial': presion_arterial,
            'mensaje': 'Diagnóstico realizado con éxito'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error interno del servidor: {str(e)}'
        }), 500

@app.route('/health')
def health():
    """Endpoint de salud para verificar que la aplicación funciona"""
    return jsonify({
        'status': 'healthy',
        'message': 'La aplicación de diagnóstico médico está funcionando correctamente'
    })

if __name__ == '__main__':
    print("Iniciando aplicación de diagnóstico médico...")
    print("Página web disponible en: http://localhost:5000")
    print("API REST disponible en: http://localhost:5000/api/predict")
    print("Endpoint de salud en: http://localhost:5000/health")
    app.run(debug=True, host='0.0.0.0', port=5000)



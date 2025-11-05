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
        
        # Validar que se proporcionen los tres valores
        if not data or 'valor1' not in data or 'valor2' not in data or 'valor3' not in data:
            return jsonify({
                'error': 'Se requieren los valores valor1, valor2 y valor3'
            }), 400
        
        # Extraer valores
        valor1 = float(data['valor1'])
        valor2 = float(data['valor2'])
        valor3 = float(data['valor3'])
        
        # Validar que los valores sean números válidos
        if not all(isinstance(val, (int, float)) for val in [valor1, valor2, valor3]):
            return jsonify({
                'error': 'Todos los valores deben ser números'
            }), 400
        
        # Realizar diagnóstico
        resultado = diagnostico(valor1, valor2, valor3)
        
        # Calcular suma para información adicional
        suma = valor1 + valor2 + valor3
        
        return jsonify({
            'diagnostico': resultado,
            'categorias': [
                "NO ENFERMO",
                "ENFERMO LEVE",
                "ENFERMO AGUDO",
                "ENFERMO CRONICO",
                "ENFERMEDAD TERMINAL"
            ],
            'valor1': valor1,
            'valor2': valor2,
            'valor3': valor3,
            'suma': suma,
            'mensaje': f'Diagnóstico basado en la suma de valores: {suma}'
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
        valor1 = request.args.get('valor1', type=float)
        valor2 = request.args.get('valor2', type=float)
        valor3 = request.args.get('valor3', type=float)
        
        # Validar que se proporcionen los tres valores
        if valor1 is None or valor2 is None or valor3 is None:
            return jsonify({
                'error': 'Se requieren los parámetros valor1, valor2 y valor3 en la URL'
            }), 400
        
        # Realizar diagnóstico
        resultado = diagnostico(valor1, valor2, valor3)
        
        # Calcular suma para información adicional
        suma = valor1 + valor2 + valor3
        
        return jsonify({
            'diagnostico': resultado,
            'categorias': [
                "NO ENFERMO",
                "ENFERMO LEVE",
                "ENFERMO AGUDO",
                "ENFERMO CRONICO",
                "ENFERMEDAD TERMINAL"
            ],
            'valor1': valor1,
            'valor2': valor2,
            'valor3': valor3,
            'suma': suma,
            'mensaje': f'Diagnóstico basado en la suma de valores: {suma}'
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



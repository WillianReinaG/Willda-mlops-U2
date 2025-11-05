# Unidad 2 - Proyecto MLOps

## Sistema de Diagnóstico Médico - Aplicación Web

Esta aplicación web proporciona una interfaz para realizar diagnósticos médicos usando la función simulada del archivo `Diagnostico.py`.

## Características

- 🌐 **Interfaz Web**: Página web moderna y responsive para ingresar valores
- 🔌 **API REST**: Endpoints para integración con otros sistemas
- 📊 **Diagnóstico Automático**: Calcula el estado de salud basado en tres valores
- 🎨 **Diseño Moderno**: Interfaz atractiva con gradientes y animaciones

## Instalación

### Opción 1: Instalación Local

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la aplicación:
```bash
python app.py
```

3. Abrir el navegador en: `http://localhost:5000`

### Opción 2: Usando Docker (Recomendado)

#### Método Rápido con Docker Compose
```bash
# Ejecutar con docker-compose (recomendado)
docker-compose up --build

# O usar el script automatizado
./docker-script.sh compose    # Linux/Mac
.\docker-script.ps1 compose   # Windows PowerShell
```

#### Método Manual con Docker
```bash
# Construir la imagen
docker build -t diagnostico-app .

# Ejecutar el contenedor
docker run -d --name diagnostico-container -p 5000:5000 diagnostico-app
```

#### Scripts de Automatización
- **Linux/Mac**: `./docker-script.sh [build|run|stop|logs|clean|compose]`
- **Windows**: `.\docker-script.ps1 [build|run|stop|logs|clean|compose]`

Ejemplos:
```bash
# Construir imagen
./docker-script.sh build

# Ejecutar aplicación
./docker-script.sh run

# Ver logs
./docker-script.sh logs

# Detener aplicación
./docker-script.sh stop
```

## Uso

### Interfaz Web
- Ingrese tres valores numéricos en el formulario
- Haga clic en "Obtener Diagnóstico"
- Vea el resultado inmediatamente

### API REST

#### Endpoint POST `/api/predict`
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"valor1": 5, "valor2": 8, "valor3": 12}'
```

#### Endpoint GET `/api/predict`
```bash
curl "http://localhost:5000/api/predict?valor1=5&valor2=8&valor3=12"
```

#### Endpoint de Salud `/health`
```bash
curl http://localhost:5000/health
```

## Respuesta de la API

```json
{
  "diagnostico": "ENFERMO LEVE",
  "valor1": 5,
  "valor2": 8,
  "valor3": 12,
  "suma": 25,
  "mensaje": "Diagnóstico basado en la suma de valores: 25"
}
```

## Criterios de Diagnóstico

- **Suma < 10**: NO ENFERMO
- **Suma 10-19**: ENFERMO LEVE
- **Suma 20-29**: ENFERMO AGUDO
- **Suma ≥ 30**: ENFERMO CRÓNICO

## Estructura del Proyecto

```
Willda-mlops-U2/
├── app.py                  # Aplicación Flask principal
├── Diagnostico.py          # Función de diagnóstico
├── requirements.txt        # Dependencias
├── Dockerfile              # Configuración de Docker
├── docker-compose.yml      # Configuración de Docker Compose
├── .dockerignore           # Archivos a ignorar en Docker
├── docker-script.sh        # Script de automatización (Linux/Mac)
├── docker-script.ps1       # Script de automatización (Windows)
├── templates/
│   └── index.html          # Template HTML
└── README.md               # Este archivo
```

## Tecnologías Utilizadas

- **Flask**: Framework web de Python
- **HTML5/CSS3**: Interfaz moderna y responsive
- **JavaScript**: Interactividad del frontend
- **Python**: Lógica de negocio y API
- **Docker**: Containerización y despliegue
- **Docker Compose**: Orquestación de contenedores

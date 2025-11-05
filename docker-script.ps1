# Script PowerShell para construir y ejecutar la aplicación de diagnóstico médico con Docker

param(
    [Parameter(Position=0)]
    [ValidateSet("build", "run", "stop", "logs", "clean", "compose", "help")]
    [string]$Action = "help"
)

Write-Host "=== Aplicación de Diagnóstico Médico - Docker ===" -ForegroundColor Cyan
Write-Host ""

# Función para mostrar ayuda
function Show-Help {
    Write-Host "Uso: .\docker-script.ps1 [OPCIÓN]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Opciones:" -ForegroundColor Green
    Write-Host "  build     Construir la imagen Docker"
    Write-Host "  run       Ejecutar el contenedor"
    Write-Host "  stop      Detener el contenedor"
    Write-Host "  logs      Mostrar logs del contenedor"
    Write-Host "  clean     Limpiar imágenes y contenedores"
    Write-Host "  compose   Usar docker-compose (recomendado)"
    Write-Host "  help      Mostrar esta ayuda"
    Write-Host ""
    Write-Host "Ejemplos:" -ForegroundColor Green
    Write-Host "  .\docker-script.ps1 build"
    Write-Host "  .\docker-script.ps1 run"
    Write-Host "  .\docker-script.ps1 compose"
}

# Función para construir la imagen
function Build-Image {
    Write-Host "🔨 Construyendo imagen Docker..." -ForegroundColor Yellow
    docker build -t diagnostico-app .
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Imagen construida exitosamente" -ForegroundColor Green
    } else {
        Write-Host "❌ Error al construir la imagen" -ForegroundColor Red
        exit 1
    }
}

# Función para ejecutar el contenedor
function Run-Container {
    Write-Host "🚀 Ejecutando contenedor..." -ForegroundColor Yellow
    docker run -d --name diagnostico-container -p 5000:5000 diagnostico-app
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Contenedor ejecutándose en http://localhost:5000" -ForegroundColor Green
        Write-Host "📊 Health check: http://localhost:5000/health" -ForegroundColor Cyan
    } else {
        Write-Host "❌ Error al ejecutar el contenedor" -ForegroundColor Red
        exit 1
    }
}

# Función para detener el contenedor
function Stop-Container {
    Write-Host "🛑 Deteniendo contenedor..." -ForegroundColor Yellow
    docker stop diagnostico-container 2>$null
    docker rm diagnostico-container 2>$null
    Write-Host "✅ Contenedor detenido y eliminado" -ForegroundColor Green
}

# Función para mostrar logs
function Show-Logs {
    Write-Host "📋 Mostrando logs del contenedor..." -ForegroundColor Yellow
    docker logs diagnostico-container
}

# Función para limpiar
function Clean-Docker {
    Write-Host "🧹 Limpiando imágenes y contenedores..." -ForegroundColor Yellow
    docker stop diagnostico-container 2>$null
    docker rm diagnostico-container 2>$null
    docker rmi diagnostico-app 2>$null
    Write-Host "✅ Limpieza completada" -ForegroundColor Green
}

# Función para usar docker-compose
function Use-Compose {
    Write-Host "🐳 Usando docker-compose..." -ForegroundColor Yellow
    Write-Host "Construyendo y ejecutando con docker-compose..."
    docker-compose up --build -d
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Aplicación ejecutándose con docker-compose" -ForegroundColor Green
        Write-Host "🌐 Disponible en: http://localhost:5000" -ForegroundColor Cyan
        Write-Host "📊 Health check: http://localhost:5000/health" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Para ver logs: docker-compose logs -f" -ForegroundColor Yellow
        Write-Host "Para detener: docker-compose down" -ForegroundColor Yellow
    } else {
        Write-Host "❌ Error al ejecutar con docker-compose" -ForegroundColor Red
        exit 1
    }
}

# Procesar acción
switch ($Action) {
    "build" { Build-Image }
    "run" { Run-Container }
    "stop" { Stop-Container }
    "logs" { Show-Logs }
    "clean" { Clean-Docker }
    "compose" { Use-Compose }
    "help" { Show-Help }
    default {
        Write-Host "❌ Opción no válida: $Action" -ForegroundColor Red
        Write-Host ""
        Show-Help
        exit 1
    }
}



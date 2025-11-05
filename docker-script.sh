#!/bin/bash

# Script para construir y ejecutar la aplicación de diagnóstico médico con Docker

echo "=== Aplicación de Diagnóstico Médico - Docker ==="
echo ""

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 [OPCIÓN]"
    echo ""
    echo "Opciones:"
    echo "  build     Construir la imagen Docker"
    echo "  run       Ejecutar el contenedor"
    echo "  stop      Detener el contenedor"
    echo "  logs      Mostrar logs del contenedor"
    echo "  clean     Limpiar imágenes y contenedores"
    echo "  compose   Usar docker-compose (recomendado)"
    echo "  help      Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 build"
    echo "  $0 run"
    echo "  $0 compose"
}

# Función para construir la imagen
build_image() {
    echo "🔨 Construyendo imagen Docker..."
    docker build -t diagnostico-app .
    echo "✅ Imagen construida exitosamente"
}

# Función para ejecutar el contenedor
run_container() {
    echo "🚀 Ejecutando contenedor..."
    docker run -d --name diagnostico-container -p 5000:5000 diagnostico-app
    echo "✅ Contenedor ejecutándose en http://localhost:5000"
    echo "📊 Health check: http://localhost:5000/health"
}

# Función para detener el contenedor
stop_container() {
    echo "🛑 Deteniendo contenedor..."
    docker stop diagnostico-container
    docker rm diagnostico-container
    echo "✅ Contenedor detenido y eliminado"
}

# Función para mostrar logs
show_logs() {
    echo "📋 Mostrando logs del contenedor..."
    docker logs diagnostico-container
}

# Función para limpiar
clean_docker() {
    echo "🧹 Limpiando imágenes y contenedores..."
    docker stop diagnostico-container 2>/dev/null || true
    docker rm diagnostico-container 2>/dev/null || true
    docker rmi diagnostico-app 2>/dev/null || true
    echo "✅ Limpieza completada"
}

# Función para usar docker-compose
use_compose() {
    echo "🐳 Usando docker-compose..."
    echo "Construyendo y ejecutando con docker-compose..."
    docker-compose up --build -d
    echo "✅ Aplicación ejecutándose con docker-compose"
    echo "🌐 Disponible en: http://localhost:5000"
    echo "📊 Health check: http://localhost:5000/health"
    echo ""
    echo "Para ver logs: docker-compose logs -f"
    echo "Para detener: docker-compose down"
}

# Procesar argumentos
case "${1:-help}" in
    build)
        build_image
        ;;
    run)
        run_container
        ;;
    stop)
        stop_container
        ;;
    logs)
        show_logs
        ;;
    clean)
        clean_docker
        ;;
    compose)
        use_compose
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ Opción no válida: $1"
        echo ""
        show_help
        exit 1
        ;;
esac



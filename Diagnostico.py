# diagnostico.py

def diagnostico(edad, temperatura, frecuencia_cardiaca, glucosa, presion_arterial):
    """
    Evalúa el estado de salud basado en 5 parámetros vitales.
    
    Args:
        edad: 0-110 (óptimo: 30-40)
        temperatura: 30-50°C (óptimo: 37)
        frecuencia_cardiaca: 40-110 bpm (óptimo: 70)
        glucosa: 50-400 mg/dL (óptimo: 100)
        presion_arterial: 60-150 mmHg (óptimo: 105)
    
    Returns:
        Categoría de enfermedad
    """
    
    # Definir rangos óptimos (puntos medios)
    rangos_optimos = {
        'edad': (30, 40, 0, 110),  # (min_óptimo, max_óptimo, min_rango, max_rango)
        'temperatura': (36.5, 37.5, 30, 50),
        'frecuencia_cardiaca': (60, 80, 40, 110),
        'glucosa': (90, 110, 50, 400),
        'presion_arterial': (100, 110, 60, 150)
    }
    
    def calcular_desviacion(valor, parametro):
        """Calcula puntuación de desviación (0 = óptimo, mayor = peor)"""
        min_opt, max_opt, min_rango, max_rango = rangos_optimos[parametro]
        
        if min_opt <= valor <= max_opt:
            return 0
        elif valor < min_opt:
            desviacion = min_opt - valor
            rango_inf = min_opt - min_rango
            return (desviacion / rango_inf) * 10 if rango_inf > 0 else 10
        else:  # valor > max_opt
            desviacion = valor - max_opt
            rango_sup = max_rango - max_opt
            return (desviacion / rango_sup) * 10 if rango_sup > 0 else 10
    
    # Calcular puntuaciones individuales
    puntuaciones = {
        'edad': calcular_desviacion(edad, 'edad'),
        'temperatura': calcular_desviacion(temperatura, 'temperatura'),
        'frecuencia_cardiaca': calcular_desviacion(frecuencia_cardiaca, 'frecuencia_cardiaca'),
        'glucosa': calcular_desviacion(glucosa, 'glucosa'),
        'presion_arterial': calcular_desviacion(presion_arterial, 'presion_arterial')
    }
    
    # Suma ponderada (promedio de desviaciones)
    suma = sum(puntuaciones.values()) / len(puntuaciones)
    
    # Clasificación según puntuación total
    if suma < 10:
        return "NO ENFERMO"
    elif 10 <= suma < 20:
        return "ENFERMO LEVE"
    elif 20 <= suma < 30:
        return "ENFERMO AGUDO"
    elif 30 <= suma < 40:
        return "ENFERMO CRONICO"
    else:
        return "ENFERMEDAD TERMINAL"
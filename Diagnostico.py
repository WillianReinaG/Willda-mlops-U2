# diagnostico.py
# Sistema profesional de diagnóstico médico basado en múltiples parámetros

def diagnostico(edad, indice_muscular, presion, glucosa, oxigenacion, temperatura):
    """
    Determina el nivel de enfermedad basado en parámetros médicos.
    
    Parámetros:
        edad (float): Edad del paciente en años
        indice_muscular (float): Índice de masa muscular
        presion (float): Presión arterial sistólica (mmHg)
        glucosa (float): Nivel de glucosa en sangre (mg/dL)
        oxigenacion (float): Nivel de saturación de oxígeno (%)
        temperatura (float): Temperatura corporal (°C)
    
    Returns:
        str: Nivel de diagnóstico (NO ENFERMO, ENFERMO LEVE, ENFERMO AGUDO, 
             ENFERMO CRONICO, ENFERMEDAD TERMINAL)
    """
    
    # Normalizar valores para crear un índice de riesgo
    # Factores de riesgo ajustados según importancia clínica
    
    # Factor edad (mayor edad = mayor riesgo)
    factor_edad = edad / 10  # Normalizado
    
    # Factor índice muscular (menor índice = mayor riesgo)
    factor_muscular = max(0, (30 - indice_muscular) / 5)  # Invertido
    
    # Factor presión (valores normales 90-120, fuera de rango = riesgo)
    if presion < 90:
        factor_presion = (90 - presion) / 10  # Hipotensión
    elif presion > 120:
        factor_presion = (presion - 120) / 20  # Hipertensión
    else:
        factor_presion = 0  # Normal
    
    # Factor glucosa (valores normales 70-100, fuera de rango = riesgo)
    if glucosa < 70:
        factor_glucosa = (70 - glucosa) / 10  # Hipoglucemia
    elif glucosa > 100:
        factor_glucosa = (glucosa - 100) / 30  # Hiperglucemia
    else:
        factor_glucosa = 0  # Normal
    
    # Factor oxigenación (menor oxigenación = mayor riesgo crítico)
    factor_oxigenacion = max(0, (98 - oxigenacion) / 2)  # Invertido
    
    # Factor temperatura (valores normales 36-37.5, fuera = riesgo)
    if temperatura < 36:
        factor_temperatura = (36 - temperatura) / 2  # Hipotermia
    elif temperatura > 37.5:
        factor_temperatura = (temperatura - 37.5) / 1.5  # Fiebre
    else:
        factor_temperatura = 0  # Normal
    
    # Calcular índice de riesgo total (ponderado)
    indice_riesgo = (
        factor_edad * 0.8 +
        factor_muscular * 1.0 +
        factor_presion * 1.5 +
        factor_glucosa * 1.3 +
        factor_oxigenacion * 2.0 +  # Oxigenación es crítica
        factor_temperatura * 1.2
    )
    
    # Clasificación según índice de riesgo
    if indice_riesgo < 5:
        return "NO ENFERMO"
    elif 5 <= indice_riesgo < 12:
        return "ENFERMO LEVE"
    elif 12 <= indice_riesgo < 20:
        return "ENFERMO AGUDO"
    elif 20 <= indice_riesgo < 30:
        return "ENFERMO CRONICO"
    else:
        return "ENFERMEDAD TERMINAL"

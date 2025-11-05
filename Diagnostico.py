# diagnostico.py

def diagnostico(valor1, valor2, valor3):
    suma = valor1 + valor2 + valor3
    if suma < 10:
        return "NO ENFERMO"
    elif 10 <= suma < 20:
        return "ENFERMO LEVE"
    elif 20 <= suma < 30:
        return "ENFERMO AGUDO"
    else:
        return "ENFERMO CRONICO"
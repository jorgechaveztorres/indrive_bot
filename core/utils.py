# Utilidades genéricas sin evasión
def formatear_soles(monto):
    return f"S/ {monto:.2f}"

def validar_hora(hora_str):
    try:
        from datetime import datetime
        datetime.strptime(hora_str, "%H:%M")
        return True
    except:
        return False

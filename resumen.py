import os
from datetime import datetime
log_path = "logs/asistente_service.log"
if not os.path.exists(log_path):
    print("Aun no hay carreras")
    exit()
hoy = datetime.now().strftime("%Y-%m-%d")
total_neto = 0
total_comb = 0
conteo = 0
with open(log_path, "r", encoding="utf-8") as f:
    for line in f:
        if hoy in line:
            print(line.strip())
            conteo += 1
            try:
                neto = float(line.split("Neto:S/")[1].split(" ")[0])
                total_neto += neto
            except:
                pass
print(f"\nCarreras hoy: {conteo} | Neto total: S/ {total_neto:.2f}")

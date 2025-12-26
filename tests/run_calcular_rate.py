import sys
sys.path.append(r'c:\Users\edumi\Code\251225')
from app.utils import calcular_rate

valores = [0.3, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5]
for v in valores:
    print(f"vel={v} -> {calcular_rate(v)}")

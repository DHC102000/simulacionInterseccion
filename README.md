# simulacionInterseccion
Simulación de optimización de congestión en una intersección vial
Se puede cambiar la configuración de los semáforos en green_time_ns=60, green_time_ew=60. 
Se puede también cambiar los semáforos por signos PARE reemplazando return self.state == "NS"
a return False, sin embargo los semáforos presentan mejor eficiencia cuando hay más flujo de autos.

Este modelo está basado en problemas reales donde las intersecciones generan congestionamiento durante horas pico.

Cómo correr
```bash
git clone https://github.com/DHC102000/simulacionInterseccion.git
cd simulacionInterseccion
pip install -r requirements.txt
python Interss.py


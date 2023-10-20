from typing import Tuple

class DatosMeteorologicos:
    def __init__(self, nombre_archivo: str):
        self.nombre_archivo = nombre_archivo
        self.temperaturas = []
        self.humedades = []
        self.presiones = []
        self.velocidades_viento = []
        self.direcciones_viento = []

    def procesar_datos(self) -> Tuple[float, float, float, float, str]:
        try:
            with open(self.nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()

            for i in range(len(lineas)):
                if lineas[i].startswith("Temperatura: "):
                    temperatura = float(lineas[i].split(": ")[1])
                    self.temperaturas.append(temperatura)
                elif lineas[i].startswith("Humedad: "):
                    humedad = float(lineas[i].split(": ")[1])
                    self.humedades.append(humedad)
                elif lineas[i].startswith("Presión: "):
                    presion = float(lineas[i].split(": ")[1])
                    self.presiones.append(presion)
                elif lineas[i].startswith("Viento: "):
                    viento = lineas[i].split(": ")[1].split(",")
                    velocidad = float(viento[0])
                    direccion = viento[1]
                    self.velocidades_viento.append(velocidad)
                    self.direcciones_viento.append(direccion)

            if not self.temperaturas or not self.humedades or not self.presiones or not self.velocidades_viento:
                raise ValueError("No hay datos para calcular las estadísticas")

            temperatura_promedio = sum(self.temperaturas) / len(self.temperaturas)
            humedad_promedio = sum(self.humedades) / len(self.humedades)
            presion_promedio = sum(self.presiones) / len(self.presiones)
            velocidad_promedio = sum(self.velocidades_viento) / len(self.velocidades_viento)
            direccion_prominente = self.calcular_direccion_prominente()

            return (temperatura_promedio, humedad_promedio, presion_promedio, velocidad_promedio, direccion_prominente)

        except Exception as e:
            print(f"Error al procesar el archivo: {str(e)}")
            return (0, 0, 0, 0, "")

    def calcular_direccion_prominente(self) -> str:
        # Mapeo de direcciones a grados
        direccion_a_grados = {
            "N": 0,
            "NNE": 22.5,
            "NE": 45,
            "ENE": 67.5,
            "E": 90,
            "ESE": 112.5,
            "SE": 135,
            "SSE": 157.5,
            "S": 180,
            "SSW": 202.5,
            "SW": 225,
            "WSW": 247.5,
            "W": 270,
            "WNW": 292.5,
            "NW": 315,
            "NNW": 337.5
        }

        # Calcular el promedio en grados
        grados = sum(direccion_a_grados[d] for d in self.direcciones_viento) / len(self.direcciones_viento)

        # Encontrar la dirección más cercana en grados
        direcciones = list(direccion_a_grados.keys())
        direcciones.sort(key=lambda d: abs(direccion_a_grados[d] - grados))

        return direcciones[0]

# Ejemplo de uso:
nombre_archivo = "datos.txt"  # Reemplaza con el nombre de tu archivo
datos = DatosMeteorologicos(nombre_archivo)
temperatura_promedio, humedad_promedio, presion_promedio, velocidad_promedio, direccion_prominente = datos.procesar_datos()

print(f"Temperatura promedio: {temperatura_promedio}°C")
print(f"Humedad promedio: {humedad_promedio}%")
print(f"Presión promedio: {presion_promedio} hPa")
print(f"Velocidad promedio del viento: {velocidad_promedio} km/h")
print(f"Dirección predominante del viento: {direccion_prominente}")

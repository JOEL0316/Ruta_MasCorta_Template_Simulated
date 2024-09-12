from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import math
import random

app = Flask(__name__)
CORS(app)  # Permite CORS en la aplicación Flask

coord = {
    'Aguascalientes': [21.8853, -102.2916],
    'Baja California': [32.6246, -115.4523],
    'Baja California Sur': [24.1426, -110.3128],
    'Campeche': [19.8301, -90.5349],
    'Chiapas': [16.7539, -93.1131],
    'Chihuahua': [28.6329, -106.0691],
    'Ciudad de Mexico': [19.4326, -99.1332],
    'Coahuila': [25.4232, -101.0000],
    'Colima': [19.1223, -104.0072],
    'Durango': [24.0277, -104.6532],
    'Guanajuato': [21.0190, -101.2574],
    'Guerrero': [17.4392, -99.5451],
    'Hidalgo': [20.1011, -98.7302],
    'Jalisco': [20.6597, -103.3496],
    'Estado de Mexico': [19.4969, -99.7233],
    'Michoacan': [19.5665, -101.7068],
    'Morelos': [18.6813, -99.1013],
    'Nayarit': [21.7514, -104.8455],
    'Nuevo Leon': [25.6866, -100.3161],
    'Oaxaca': [17.0732, -96.7266],
    'Puebla': [19.0414, -98.2063],
    'Queretaro': [20.5888, -100.3899],
    'Quintana Roo': [19.1817, -88.4791],
    'San Luis Potosí': [22.1565, -100.9855],
    'Sinaloa': [24.8045, -107.4938],
    'Sonora': [29.0720, -110.9559],
    'Tabasco': [17.9869, -92.9303],
    'Tamaulipas': [23.7417, -99.1458],
    'Tlaxcala': [19.3139, -98.2404],
    'Veracruz': [19.1738, -96.1342],
    'Yucatan': [20.7099, -89.0943],
    'Zacatecas': [22.7709, -102.5832]
}

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Radio de la Tierra en km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = R * c
    return distancia

def evalua_ruta(ruta, coord):
    total = 0
    for i in range(len(ruta) - 1):
        ciudad1 = ruta[i]
        ciudad2 = ruta[i + 1]
        total += distancia(coord[ciudad1], coord[ciudad2])
    ciudad1 = ruta[-1]
    ciudad2 = ruta[0]
    total += distancia(coord[ciudad1], coord[ciudad2])
    return total

def simulated_annealing(ruta, coord):
    T = 20
    T_MIN = 0
    V_enfriamiento = 100

    while T > T_MIN:
        dist_actual = evalua_ruta(ruta, coord)
        for _ in range(V_enfriamiento):
            i = random.randint(0, len(ruta) - 1)
            j = random.randint(0, len(ruta) - 1)

            # Asegurar que i y j sean diferentes
            while i == j:
                j = random.randint(0, len(ruta) - 1)

            ruta_tmp = ruta[:]
            ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
            dist = evalua_ruta(ruta_tmp, coord)
            delta = dist_actual - dist
            if dist < dist_actual:
                ruta = ruta_tmp
                break
            elif random.random() < math.exp(delta / T):
                ruta = ruta_tmp
                break
        T -= 0.005

    return ruta

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shortest_route', methods=['POST'])
def shortest_route():
    try:
        data = request.get_json()
        start = data['start']
        end = data['end']
        
        # Crear una lista de ciudades en orden
        ruta = [start, end]
        mejor_ruta = simulated_annealing(ruta, coord)
        distancia_total = evalua_ruta(mejor_ruta, coord)

        return jsonify({
            'mejor_ruta': mejor_ruta,
            'distancia_total': distancia_total
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

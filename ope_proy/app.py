from flask import Flask, request, render_template, jsonify
from scipy.optimize import linprog

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/resolver', methods=['POST'])
def resolver():
    try:
        # Leer datos del formulario
        funcion_objetivo = list(map(float, request.form['objetivo'].split(',')))
        restricciones = request.form['restricciones'].split(';')
        lados_derechos = list(map(float, request.form['lados'].split(',')))

        # Procesar restricciones
        A = [list(map(float, r.split(','))) for r in restricciones]

        # Resolver problema de programación lineal
        resultado = linprog(c=funcion_objetivo, A_ub=A, b_ub=lados_derechos, method='highs')

        if resultado.success:
            solucion = {
                'variables': [f"x{i+1} = {valor:.2f}" for i, valor in enumerate(resultado.x)],
                'funcion_objetivo': f"Z = {-resultado.fun:.2f}"
            }
        else:
            solucion = {'error': 'No se pudo encontrar una solución óptima.'}

        return jsonify(solucion)

    except Exception as e:
        return jsonify({'error': f"Error en el procesamiento de datos: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)

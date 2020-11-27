#!/usr/bin/env python
'''
Mapa interactivo
---------------------------
Ejecución: Lanzar el programa y abrir en un navegador la siguiente dirección URL
http://127.0.0.1:5000/

Requisitos de instalacion:

- Python 3.x
- Libreriras (incluye los comandos de instalacion)
    pip install numpy
    pip install pandas
    pip install -U Flask
'''

__author__ = "Hernan Contigiani"
__version__ = "1.0"


import pandas as pd
import numpy as np
import traceback
import io

from flask import Flask, request, jsonify, render_template, Response, redirect
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from sklearn import linear_model

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

 
@app.route('/mapa') # Your API endpoint URL would consist /predict
def propiedades():
    try:
        marker = {'red': 'http://www.openstreetmap.org/openlayers/img/marker.png',
                  'blue': 'http://www.openstreetmap.org/openlayers/img/marker-blue.png',
                  'gold': 'http://www.openstreetmap.org/openlayers/img/marker-gold.png',
                  'green': 'http://www.openstreetmap.org/openlayers/img/marker-green.png'
                    }


        # # Marco que bandera o marca mostrar en cada caso
        # df['marca'] = df.apply(lambda x: blue_marker if x['moneda'] == 'USD' else gold_marker if x['precio'] < q_low else red_marker if x['precio'] > q_hi else green_marker, axis=1 )

        df = pd.read_csv("campo.csv")
        df['marca'] = 'http://www.openstreetmap.org/openlayers/img/marker.png'

        print(df['marca'].head())

        if "color" in df:
            df['marca'] = df.apply(lambda x: marker.get(x['color'], 'http://www.openstreetmap.org/openlayers/img/marker.png'), axis=1 )

        result = df.to_json()
        return(result)
    except:
        return jsonify({'trace': traceback.format_exc()})

@app.route('/alquileres/reporte') # Your API endpoint URL would consist /predict
def reporte():
    try:
        # Utilizo el programa de reporte para generar el gráfico y mostrarlo en la web
        fig = rp.generar_reporte(reporte=0, silent_mode=True)
        
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
    except:
        return jsonify({'trace': traceback.format_exc()})

if __name__ == '__main__':
    try:
        port = int(sys.argv[1]) # This is for a command-line argument
    except:
        port = 5000 # Puerto default
        
    app.run(host='0.0.0.0', port=port, debug=True)
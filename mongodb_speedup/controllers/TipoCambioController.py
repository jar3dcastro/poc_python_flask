from config import db as mongo
from flask import request, jsonify, abort
from datetime import datetime

class TipoCambioController :
    def get_tipo_cambio (fecha) :
        try :
            # validacion de entrada
            try :
                fecha = datetime.strptime(fecha, '%Y%m%d').strftime('%d/%m/%Y')
            except :
                raise Exception('La fecha debe tener el siguiente formato: yyyymmdd')
            # obtener cambio
            result = mongo.db.coleccion_tipo_cambio.find_one({'fecha':str(fecha)})
            if result is None :
                raise Exception('Sin resultados')
            # limpiar datos
            tipo_cambio = result['tipo_cambio']
            if ',' in tipo_cambio :
                tipo_cambio = tipo_cambio.replace(',', '.')
            tipo_cambio = float(tipo_cambio)
            return jsonify({'tipo_cambio':tipo_cambio})
        except Exception as error :
            abort(404, description=str(error))

from config import app, db
from flask import request, jsonify, abort
from models.venta import Venta
from models.producto import Producto
from models.moneda import Moneda

def obtener_de_api_masivo (paths, mode = 'parallel') :
    if mode == 'sync' :

        import requests
        respuestas = [
            requests.get('http://nosql-benchmark:5001/' + path).json()
            for path in paths
        ]
        return respuestas

    elif mode == 'async' :

        import aiohttp
        import asyncio
        async def get (url) :
            async with aiohttp.ClientSession() as session :
                async with session.get(url) as response:
                    return await response.json()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        corrutinas = [
            get('http://nosql-benchmark:5001/' + path)
            for path in paths
        ]
        respuestas = loop.run_until_complete(asyncio.gather(*corrutinas))
        return respuestas

    elif mode == 'parallel' :

        from concurrent import futures
        import requests
        with futures.ThreadPoolExecutor(max_workers=365) as executor :
            futures = [
                [executor.submit(lambda : requests.get('http://nosql-benchmark:5001/tipocambio/' + path).json()), path]
                for path in paths
            ]
        respuestas = [
            [future[0].result(), future[1]]
            for future in futures
        ]
        return respuestas

class VentaController :
    def get_resumen_ventas () :
        try :
            # entrada
            app.logger.info(f'REQUEST={request.json}')
            id_producto = request.json['id_producto']
            anio = request.json['anio']
            mes = request.json['mes']
            moneda = request.json['moneda']
            usuario_consulta = request.json['usuario_consulta']
            modo_ejecucion_request = 'parallel'#request.args.get('modo')
            # contantes
            PEN = 1
            USD = 2
            # validacion de entrada
            if type(id_producto) is not int :
                raise Exception('id_producto must be integer')
            if type(anio) is not int :
                raise Exception('anio must be integer')
            if type(mes) is not int :
                raise Exception('mes must be integer')
            if type(moneda) is not str or moneda not in ['PEN', 'USD'] :
                raise Exception('moneda must be PEN or USD')
            if type(usuario_consulta) is not str :
                raise Exception('usuario_consulta must be string')
            # obtener ventas
            query = Venta.query.filter(Venta.id_producto == id_producto)
            if anio != 0 :
                query = query.filter(db.extract('year', Venta.fecha) == anio)
            if mes != 0 :
                query = query.filter(db.extract('month', Venta.fecha) == mes)
            ventas = query.all()
            if len(ventas) == 0 :
                return jsonify([])
            # obtener listado de fechas necesarias a ser procesadas
            id_moneda = PEN if moneda == 'PEN' else USD
            cambios_moneda = {}
            for venta in ventas :
                anio = venta.fecha.year
                mes = venta.fecha.month
                dia = venta.fecha.day
                venta.aniomes = f'{anio}{"0" if mes < 10 else ""}{mes}'
                venta.aniomesdia = f'{venta.aniomes}{"0" if dia < 10 else ""}{dia}'
                # iniciar con el cambio por defecto
                cambios_moneda[venta.aniomesdia] = 3
                '''# hacer consulta al api de cambios
                respuesta_api = obtener_de_api(f'tipocambio/{venta.aniomesdia}')
                if 'error' not in respuesta_api :
                    cambios_moneda[venta.aniomesdia] = respuesta_api['tipo_cambio']'''
            # obtener cambios de moneda para cada fecha
            paths = [
                aniomesdia for aniomesdia in cambios_moneda.keys()
            ]
            respuestas_api = obtener_de_api_masivo(paths, mode=modo_ejecucion_request)
            for _respuesta_api in respuestas_api :
                respuesta_api = _respuesta_api[0]
                aniomesdia = _respuesta_api[1]
                if 'error' not in respuesta_api :
                    cambios_moneda[aniomesdia] = respuesta_api['tipo_cambio']
            # procesar resumen
            resumen_ventas = {}
            for venta in ventas :
                aniomes = venta.aniomes
                aniomesdia = venta.aniomesdia
                if aniomes not in resumen_ventas :
                    resumen_ventas[aniomes] = 0
                monto = venta.monto
                if id_moneda == PEN and venta.id_moneda == USD :
                    monto = monto * cambios_moneda[aniomesdia]
                elif id_moneda == USD and venta.id_moneda == PEN :
                    monto = monto / cambios_moneda[aniomesdia]
                resumen_ventas[aniomes] += monto
            # crear respuesta
            producto = Producto.query.get(id_producto)
            moneda = Moneda.query.get(id_moneda)
            resultado = [
                {
                    'nombre_producto':producto.descripcion_producto,
                    'descripcion_moneda':moneda.descripcion_moneda,
                    'aniomes':int(aniomes),
                    'monto_total':round(monto_total, 2)
                }
                for aniomes, monto_total in resumen_ventas.items()
            ]
            resultado = sorted(resultado, key=lambda fila:fila['aniomes'], reverse=True)
            # hacer log del resultado
            for fila in resultado :
                producto, aniomes, monto, moneda = fila.values()
                app.logger.info(f'{producto}, {aniomes}: {monto}, {moneda}')
            # salida
            app.logger.info(f'RESULTADO={resultado}')
            return jsonify(resultado)
        except Exception as error :
            abort(404, description=str(error))

import json
from odoo.tools import date_utils
from odoo import http
import base64
import os

from random import randrange



def clear_console(self):
    os.system('clear')


class OdooController(http.Controller):

    @http.route(
        "/barriotec/skus/<categoria_id>",
        auth="public",
    )
    
    def index(self, db, **kw):
        desloguear = self.auth(db=db)


        categoriaId = kw.get('categoria_id')

        productos = http.request.env['product.template'].search([
            ["is_booking_type", "=", True],
            ["categ_id.id", "=", categoriaId],
        ])

        self.auth(login=False, desloguear=desloguear)

        datos = json.dumps(self.skusGenerarDiccionario(productos))
        return http.Response(
            datos,
            status=200,
            content_type="application/json"
        )


    def auth(self, login=True, desloguear=False, db="test"):

        # Comprobamos que no haya ningún usuario autenticado.
        uid = http.request.session.uid
        es_usuario_de_sistema = uid != None and login

        if es_usuario_de_sistema and not desloguear:
            return False

        if login:

            http.request.session.authenticate(db, "web", "12345")

            return True

        if desloguear:
            http.request.session.logout(keep_db=False)
            return False

    def skusGenerarDiccionario(self, productos):

        productos_dict = {
            'skus': []
        }
        for producto in productos:

            d = {
                "name": producto.name,
                "categ_id": [x.name for x in producto.categ_id],
                "booking_rom_num": producto.booking_rom_num,
                "booking_floor": producto.booking_floor,
                "booking_area": producto.booking_area,
                "booking_lookout_area": producto.booking_lookout_area,
                "is_booking_type": producto.is_booking_type,
                "website_url": producto.website_url,
                "booking_plan_ids": [x.id for x in producto.booking_plan_ids],
                "product_template_image_ids": [
                    x.id for x in producto.product_template_image_ids],

                "image_1024":
                'web/image/product.template/' +
                    str(producto.id)+'/image_1024/?unique=d' +
                str(randrange(9999)),
                "description": producto.description_sale,
                "list_price": producto.list_price,
                "booking_area": producto.booking_area,
                "booking_lookout_area": producto.booking_lookout_area,
                "booking_rom_num": producto.booking_rom_num,

                # Este es el campo para el plano

                "extra_image_data_uri": producto.extra_image_data_uri,
                "website_url": producto.website_url
            }

            productos_dict['skus'].append(d)

        return productos_dict

    def imagen_procesar(self, imagen_bytes):

        return base64.b64encode(imagen_bytes).decode('ascii')


    def dump(self, obj, buscar=False):
        clear_console(self)

        print(obj._model_fields)
        print("===========================")
        print("===========================")
        print("===========================")
        for attr in dir(obj):

            if buscar:
                if buscar in attr:
                    print("obj.%s = %r" % (attr, getattr(obj, attr)))
            else:
                if not '__' in attr:
                    print("obj.%s = %r" % (attr, getattr(obj, attr)))

        print("===========================")
        print("===========================")
        print("===========================")

    @http.route(
        "/barriotec/plans/<ids>",
        auth="public",
    )

    def planes(self, db, **kw):
        desloguear = self.auth(db=db)

        ids = kw.get('ids').split('-')
        datos = http.request.env['pgmx.booking.product.plans'].search(
            [["id", "in", ids]])

        self.auth(login=False, desloguear=desloguear)

        datos = json.dumps(self.planDiccionarios(datos))
        return http.Response(
            datos,
            status=200,
            content_type="application/json"
        )

    def planDiccionarios(self, planes):

        dic = {
            'plans': []
        }
        for plan in planes:

            d = {
                'id': plan.id,
                'name': plan.plan_id.name,
                'price': plan.price,
                'description': plan.plan_id.discription,

            }

            dic['plans'].append(d)

        return dic

    @http.route(
        "/barriotec/imagenes/<ids>",
        auth="public",
    )
    def imagenes(self, db, **kw):
        desloguear = self.auth(db=db)


        ids = kw.get('ids').split('-')
        datos = http.request.env['product.image'].search(
            [["id", "in", ids]])

        self.auth(login=False, desloguear=desloguear)

        datos = json.dumps(self.imagenesDiccionario(datos))
        return http.Response(
            datos,
            status=200,
            content_type="application/json"
        )

    def imagenesDiccionario(self, imagenes):

        dic = {
            'imagenes': []
        }
        for imagen in imagenes:

            d = {
                'id': imagen.id,
                'video': imagen.embed_code,
                'image_1024': 'web/image/product.image/'+str(imagen.id)+'/image_1024/?'+str(randrange(9999))

            }

            dic['imagenes'].append(d)

        return dic

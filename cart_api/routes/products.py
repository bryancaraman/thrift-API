import falcon
from playhouse.shortcuts import model_to_dict
from cart_api.database import DatabaseProducts
from peewee import DoesNotExist

class Product:
    def on_get(self, req, resp, product_id):
        try:
            product = DatabaseProducts.get(id=product_id)
            resp.media = model_to_dict(product)
            resp.status = falcon.HTTP_200
        except DoesNotExist:
            resp.status = falcon.HTTP_404
            resp.media = {
                "message": "404_NOT_FOUND"
            }

    def on_delete(self, req, resp, product_id):
        DatabaseProducts.delete_by_id(product_id)
        resp.status = falcon.HTTP_204


# Excercise 2:
# Products route should respond to GET and POST requests
# GET products returns a list of every product in the database
# POST products creates a product and returns the data it created


class Products:
    def on_get(self, req, resp):
        list = []
        for product in DatabaseProducts.select():
            list.append(model_to_dict(product))
        resp.media = list
        resp.status = falcon.HTTP_200
        
    def on_post(self, req, resp):
        obj = req.get_media()
        for product in DatabaseProducts.select():
            if (obj["name"] == product.name):
                resp.media = {"message": "Product already in database"}
                resp.status = falcon.HTTP_400
                return
        product = DatabaseProducts(
            name=obj["name"], 
            description=obj["description"], 
            size=obj["size"], 
            color=obj["color"], 
            condition=obj["condition"], 
            material=obj["material"], 
            image_url=obj["image_url"], 
            price=obj["price"], 
            is_on_sale=obj["is_on_sale"], 
            sale_price=obj["sale_price"]
        )
        product.save()
        resp.media = model_to_dict(product)
        resp.status = falcon.HTTP_201
        
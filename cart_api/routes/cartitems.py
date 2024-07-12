import falcon
from playhouse.shortcuts import model_to_dict
from cart_api.database import DatabaseCartItem
from peewee import DoesNotExist

# Exercise 3:
# Using the database model you created in Exercise 1 create a cartitems route
# CartItems should have a responder for POST and GET
# CartItem should have responders for GET DELETE PATCH
# Your API response statuses and bodies should conform to your OpenAPI spec


class CartItems:
    def on_get(self, req, resp):
        list = []
        for cart_item in DatabaseCartItem.select():
            list.append(model_to_dict(cart_item))
        resp.media = list
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        obj = req.get_media()
        for cart_item in DatabaseCartItem.select():
            if (obj["name"] == cart_item.name):
                resp.media = {"message": "Cart item already in database"}
                resp.status = falcon.HTTP_400
                return
        cart_item = DatabaseCartItem(
            name=obj["name"],
            image_url=obj["image_url"],
            price=obj["price"], 
            quantity=obj["quantity"]
        )
        cart_item.save()
        resp.media = model_to_dict(cart_item)
        resp.status = falcon.HTTP_201

class CartItem:
    def on_get(self, req, resp, cart_item_id):
        try: 
            cart_item = DatabaseCartItem.get(id=cart_item_id)
            resp.media = model_to_dict(cart_item)
            resp.status = falcon.HTTP_200
        except DoesNotExist:
            resp.status = falcon.HTTP_404  
            resp.media = {
                "message": "404_NOT_FOUND"
            }

    def on_delete(self, req, resp, cart_item_id):
        DatabaseCartItem.delete_by_id(cart_item_id)
        resp.status = falcon.HTTP_204

    def on_patch(self, req, resp, cart_item_id):
        obj = req.get_media()
        cart_item = DatabaseCartItem.get(id=cart_item_id)
        if "quantity" in obj:
            cart_item.quantity = obj["quantity"]
            cart_item.save()
        resp.status = falcon.HTTP_204


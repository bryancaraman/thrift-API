import falcon
from playhouse.shortcuts import model_to_dict
from cart_api.database import DatabaseSellItems
from peewee import DoesNotExist

class SellItem:
    def on_get(self, req, resp, sell_item_id):
        try:
            sell_item = DatabaseSellItems.get(id=sell_item_id)
            resp.media = model_to_dict(sell_item)
            resp.status = falcon.HTTP_200
        except DoesNotExist:
            resp.status = falcon.HTTP_404
            resp.media = {
                "message": "404_NOT_FOUND"
            }

    def on_delete(self, req, resp, sell_item_id):
        DatabaseSellItems.delete_by_id(sell_item_id)
        resp.status = falcon.HTTP_204

class SellItems:
    def on_get(self, req, resp):
        list = []
        for sell_item in DatabaseSellItems.select():
            list.append(model_to_dict(sell_item))
        resp.media = list
        resp.status = falcon.HTTP_200
        
    def on_post(self, req, resp):
        obj = req.get_media()
        for sell_item in DatabaseSellItems.select():
            if (obj["name"] == sell_item.name):
                resp.media = {"message": "Product for sale already in database"}
                resp.status = falcon.HTTP_400
                return
        sell_item = DatabaseSellItems(
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
        sell_item.save()
        resp.media = model_to_dict(sell_item)
        resp.status = falcon.HTTP_201
        


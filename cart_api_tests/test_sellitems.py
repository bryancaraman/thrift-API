import time
from .test_heartbeat import TestClient

SELLITEMS_PATH = "/v1/sellitems"
SELLITEM_PATH = "/v1/sellitems/{id}"

# Dummy sell item data
body = dict(
    name=f"TestProduct-{int(time.time())} ",
    description="Really awesome stuff",
    size="Large",
    color="Blue",
    condition="Used",
    material="Cotton",
    image_url="http://pictureofcats.com",
    price=14.99,
    is_on_sale=True,
    sale_price=3.99,
)

class SellItemsTest(TestClient):
    def test_post_sellitems(self):
        # Post the item for sale
        response = self.simulate_post(SELLITEMS_PATH, json=body)
        self.assertEqual(response.status_code, 201)
        
        # Test that the posted sell item is accurate
        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, dict)
        new_sell_item_id = response.json["id"]
        self.assertIsInstance(new_sell_item_id, int)
        response_minus_id = response.json
        del response_minus_id["id"]
        self.assertEqual(body, response_minus_id)

        # Test the posting of a duplicate item for sale
        response_duplicate = self.simulate_post(SELLITEMS_PATH, json=response.json)
        self.assertEqual(response_duplicate.status_code, 400)
        self.assertEqual(response_duplicate.json["message"], "Product for sale already in database")

        # Clean up and delete posted item for sale
        del_response = self.simulate_delete(SELLITEM_PATH.format(id=new_sell_item_id))
        self.assertEqual(del_response.status_code, 204)

    def test_get_all_sellitems(self):
        response = self.simulate_get(SELLITEMS_PATH)
        self.assertEqual(response.status_code, 200)

        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, list)

    def test_get_sellitem(self):
        response = self.simulate_post(SELLITEMS_PATH, json=body)
        self.assertEqual(response.status_code, 201, "Requires working POST")

        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, dict)
        new_sell_item_id = response.json["id"]
        self.assertIsInstance(new_sell_item_id, int)

        # Test getting posted sellitem
        response = self.simulate_get(SELLITEM_PATH.format(id=new_sell_item_id))
        self.assertEqual(response.status_code, 200)

        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, dict)

        del_response = self.simulate_delete(SELLITEM_PATH.format(id=new_sell_item_id))
        self.assertEqual(del_response.status_code, 204)

    def test_get_non_existing_sellitem(self):
        response = self.simulate_get(SELLITEM_PATH.format(id=9999999))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["message"], "404_NOT_FOUND")
        
    def test_delete_sellitem(self):
        response = self.simulate_post(SELLITEMS_PATH, json=body)
        self.assertEqual(response.status_code, 201, "Requires working POST")
        
        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, dict)
        new_sell_item_id = response.json["id"]
        self.assertIsInstance(new_sell_item_id, int)

        response = self.simulate_delete(SELLITEM_PATH.format(id=new_sell_item_id))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.text, "")

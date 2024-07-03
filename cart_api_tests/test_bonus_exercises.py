import time
from .test_heartbeat import TestClient

PRODUCTS_PATH = "/v1/products"
PRODUCT_PATH = "/v1/products/{id}"

body = dict(
    name=f"TestProduct-{int(time.time())} ",
    description="Woah this is like a pretty cool description yo",
    image_url="http://pictureofcats.com",
    price=4.99,
    is_on_sale=True,
    sale_price=3.99,
)

class ProductTest(TestClient):
    def test_get_product(self):
        response = self.simulate_post(PRODUCTS_PATH, json=body)
        self.assertEqual(response.status_code, 201, "Requires working POST")
        self.aitem = response.json

        response = self.simulate_get(PRODUCT_PATH.format(item_id=self.aitem["id"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], self.aitem["name"])
        
    def test_delete_item(self):
        response = self.simulate_post(PRODUCTS_PATH, json=body)
        self.assertEqual(response.status_code, 201, "Requires working POST")
        self.aitem = response.json

        response = self.simulate_delete(PRODUCT_PATH.format(item_id=self.aitem["id"]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.text, "")
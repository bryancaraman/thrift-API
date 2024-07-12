import time
from .test_heartbeat import TestClient

PRODUCTS_PATH = "/v1/products"
PRODUCT_PATH = "/v1/products/{id}"

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

class ProductTest(TestClient):
    def test_get_product(self):
        response = self.simulate_post(PRODUCTS_PATH, json=body)
        self.assertEqual(response.status_code, 201, "Requires working POST")

        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, dict)
        new_product_id = response.json["id"]
        self.assertIsInstance(new_product_id, int)

        response = self.simulate_get(PRODUCT_PATH.format(id=new_product_id))
        self.assertEqual(response.status_code, 200)

        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, dict)

        del_response = self.simulate_delete(PRODUCT_PATH.format(id=new_product_id))
        self.assertEqual(del_response.status_code, 204)
        
    def test_delete_product(self):
        response = self.simulate_post(PRODUCTS_PATH, json=body)
        self.assertEqual(response.status_code, 201, "Requires working POST")
        
        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, dict)
        new_product_id = response.json["id"]
        self.assertIsInstance(new_product_id, int)

        response = self.simulate_delete(PRODUCT_PATH.format(id=new_product_id))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.text, "")

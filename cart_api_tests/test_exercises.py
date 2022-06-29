import time
from .test_heartbeat import TestClient

PRODUCTS_PATH = "/v1/products"
PRODUCT_PATH = "/v1/products/{id}"
EXAMPLE_CART_ITEM = dict(
    name="Cool Test Item",
    price=4.99,
    quantity=1
)


class Exercise1(TestClient):
    def test_import_model(self):
        """Verifies CartItem model exists"""
        from cart_api.database import DatabaseCartItem
        DatabaseCartItem.select()

    def test_example_data_matches_model(self):
        from cart_api.database import DatabaseCartItem
        DatabaseCartItem(**EXAMPLE_CART_ITEM)


class Exercise2(TestClient):

    def test_post_products(self):
        body = dict(
            name=f"TestProduct-{int(time.time())} ",
            description="Woah this is like a pretty cool description yo",
            image_url="http://pictureofcats.com",
            price=4.99,
            is_on_sale=True,
            sale_price=3.99,
        )

        response = self.simulate_post(PRODUCTS_PATH, json=body)
        self.assertEqual(response.status_code, 201)
        r_json = response.json

        self.assertIsNotNone(r_json)
        self.assertIsInstance(r_json, dict)
        new_product_id = r_json["id"]
        self.assertIsInstance(new_product_id, int)
        del r_json["id"]
        self.assertEqual(body, r_json)

        del_response = self.simulate_delete(
            PRODUCT_PATH.format(id=new_product_id)
        )
        self.assertEqual(del_response.status_code, 204)

    def test_get_all_products(self):
        response = self.simulate_get(PRODUCTS_PATH)
        self.assertEqual(response.status_code, 200)
        r_json = response.json

        self.assertIsNotNone(r_json)
        self.assertIsInstance(r_json, list)

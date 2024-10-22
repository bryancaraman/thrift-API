import time
from .test_heartbeat import TestClient
from playhouse.postgres_ext import IntegerField


PRODUCTS_PATH = "/v1/products"
PRODUCT_PATH = "/v1/products/{id}"
EXAMPLE_CART_ITEM = dict(name="Cool Test Item", image_url="ajbaiofnao", price=4.99, quantity=1)


class Exercise1(TestClient):
    def test_import_model(self):
        """Verifies CartItem model exists"""
        from cart_api.database import DatabaseCartItem

        DatabaseCartItem.select()

    def test_example_data_matches_model(self):
        from cart_api.database import DatabaseCartItem
        isinstance(DatabaseCartItem.quantity,IntegerField)
        DatabaseCartItem(**EXAMPLE_CART_ITEM)


class Exercise2(TestClient):
    def test_post_products(self):
        # Dummy product data
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

        # Post the product
        response = self.simulate_post(PRODUCTS_PATH, json=body)
        self.assertEqual(response.status_code, 201)
        
        # Test that the posted product is accurate
        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, dict)
        new_product_id = response.json["id"]
        self.assertIsInstance(new_product_id, int)
        response_minus_id = response.json
        del response_minus_id["id"]
        self.assertEqual(body, response_minus_id)

        # Test the posting of a duplicate product
        response_duplicate = self.simulate_post(PRODUCTS_PATH, json=response.json)
        self.assertEqual(response_duplicate.status_code, 400)
        self.assertEqual(response_duplicate.json["message"], "Product already in database")

        # Clean up and delete posted product
        del_response = self.simulate_delete(PRODUCT_PATH.format(id=new_product_id))
        self.assertEqual(del_response.status_code, 204)

    def test_get_all_products(self):
        response = self.simulate_get(PRODUCTS_PATH)
        self.assertEqual(response.status_code, 200)

        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, list)

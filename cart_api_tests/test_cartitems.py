from .test_heartbeat import TestClient
from .test_exercises import EXAMPLE_CART_ITEM

CARTITEMS_PATH = "/v1/cartitems"
CARTITEM_PATH = "/v1/cartitems/{id}"


class Exercise3(TestClient):
    def test_get_cartitems(self):
        response = self.simulate_get(CARTITEMS_PATH)
        self.assertEqual(response.status_code, 200)

        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, list)

    def test_get_cartitem(self):
        body = EXAMPLE_CART_ITEM
        response = self.simulate_post(CARTITEMS_PATH, json=body)
        self.assertEqual(response.status_code, 201, "Requires working POST")
        self.aitem = response.json

        self.assertIsNotNone(self.aitem)
        self.assertIsInstance(self.aitem, dict)
        self.assertIsInstance(self.aitem["id"], int)

        response = self.simulate_get(CARTITEM_PATH.format(id=self.aitem["id"]))
        self.assertEqual(response.status_code, 200)

        # Test the response of the get
        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, dict)
        self.assertEqual(response.json["name"], self.aitem["name"])

        # Delete the test cart item
        item_uri = CARTITEM_PATH.format(id=self.aitem["id"])
        del_response = self.simulate_delete(item_uri)
        self.assertEqual(del_response.status_code, 204)

    def test_get_non_existing_cartitem(self):
        response = self.simulate_get(CARTITEM_PATH.format(id=9999999))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["message"], "404_NOT_FOUND")

    def test_post_cartitems(self):
        body = EXAMPLE_CART_ITEM
        response = self.simulate_post(CARTITEMS_PATH, json=body)

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, dict)

        generated_id = response.json["id"]
        self.assertIsInstance(generated_id, int)
        self.assertEqual(body["name"], response.json["name"])

        # Test the posting of a duplicate cartitem
        response_duplicate = self.simulate_post(CARTITEMS_PATH, json=response.json)
        self.assertEqual(response_duplicate.status_code, 400)
        self.assertEqual(response_duplicate.json["message"], "Cart item already in database")

        # Delete the test cart item
        item_uri = CARTITEM_PATH.format(id=generated_id)
        del_response = self.simulate_delete(item_uri)
        self.assertEqual(del_response.status_code, 204)

    def test_delete_cartitem(self):
        body = EXAMPLE_CART_ITEM
        response = self.simulate_post(CARTITEMS_PATH, json=body)
        self.assertEqual(response.status_code, 201, "Requires working POST")
        self.aitem = response.json

        self.assertIsNotNone(response.json)
        self.assertIsInstance(response.json, dict)
        new_product_id = response.json["id"]
        self.assertIsInstance(new_product_id, int)

        response = self.simulate_delete(CARTITEM_PATH.format(id=self.aitem["id"]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.text, "")

    def test_patch_cartitem(self):
        body = EXAMPLE_CART_ITEM
        response = self.simulate_post(CARTITEMS_PATH, json=body)
        self.assertEqual(response.status_code, 201, "Requires working POST")
        self.aitem = response.json
        changes = {"quantity": 5}
        response = self.simulate_patch(
            CARTITEM_PATH.format(id=self.aitem["id"]),
            json=changes,
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.text, "")

        # Verify change
        response = self.simulate_get(CARTITEM_PATH.format(id=self.aitem["id"]))
        self.assertEqual(response.status_code, 200, "Requires working GET")
        self.assertEqual(response.json["quantity"], 5)

        # Delete the test cart item
        item_uri = CARTITEM_PATH.format(id=self.aitem["id"])
        del_response = self.simulate_delete(item_uri)
        self.assertEqual(del_response.status_code, 204)
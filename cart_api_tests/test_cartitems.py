from .test_heartbeat import TestClient
from .test_exercises import EXAMPLE_CART_ITEM

CARTITEMS_PATH = "/v1/cartitems"
CARTITEM_PATH = "/v1/cartitems/{item_id}"


class Exercise3(TestClient):

    def test_get_items(self):
        response = self.simulate_get(CARTITEMS_PATH)
        self.assertEqual(response.status_code, 200)
        body = response.json
        self.assertIsInstance(body, list)

    def test_get_item(self):
        body = EXAMPLE_CART_ITEM
        response = self.simulate_post(CARTITEMS_PATH, json=body)
        self.assertEqual(response.status_code, 201, "Requires working POST")
        self.aitem = response.json

        response = self.simulate_get(
            CARTITEM_PATH.format(item_id=self.aitem["id"])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], self.aitem["name"])

    def test_post_cartitems(self):
        body = EXAMPLE_CART_ITEM

        response = self.simulate_post(CARTITEMS_PATH, json=body)
        r_json = response.json

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(r_json)
        self.assertIsInstance(r_json, dict)

        generated_id = r_json["id"]
        self.assertIsInstance(generated_id, int)
        self.assertEqual(body["name"], r_json["name"])

        # Delete the new item
        item_uri = CARTITEM_PATH.format(item_id=generated_id)
        self.simulate_delete(item_uri)

    def test_delete_item(self):
        body = EXAMPLE_CART_ITEM
        response = self.simulate_post(CARTITEMS_PATH, json=body)
        self.assertEqual(response.status_code, 201, "Requires working POST")
        self.aitem = response.json

        response = self.simulate_delete(
            CARTITEM_PATH.format(item_id=self.aitem["id"])
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.text, "")

    def test_patch_item(self):
        body = EXAMPLE_CART_ITEM
        response = self.simulate_post(CARTITEMS_PATH, json=body)
        self.assertEqual(response.status_code, 201, "Requires working POST")
        self.aitem = response.json
        changes = {"quantity": 5}
        response = self.simulate_patch(
            CARTITEM_PATH.format(item_id=self.aitem["id"]),
            json=changes,
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.text, "")

        # Verify change
        response = self.simulate_get(
            CARTITEM_PATH.format(item_id=self.aitem["id"])
        )
        self.assertEqual(response.status_code, 200, "Requires working GET")
        self.assertEqual(response.json["quantity"], 5)

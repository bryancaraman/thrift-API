from falcon import testing
from cart_api.api import api
from cart_api.api import Heartbeat


class TestClient(testing.TestCase):
    def setUp(self):
        # Init falcon testing harness
        super(TestClient, self).setUp()
        self.app = api


class HeartBeatTest(TestClient):
    def test_root(self):
        response = self.simulate_get("/heartbeat")
        self.assertEqual(response.text, Heartbeat.DEFAULT_BODY)

    def test_405_method_not_allowed(self):
        response = self.simulate_post("/heartbeat")
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json["code"], "405_METHOD_NOT_ALLOWED")

import falcon


class Heartbeat:
    DEFAULT_BODY = "Hello World! You did it!"

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.text = Heartbeat.DEFAULT_BODY
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT

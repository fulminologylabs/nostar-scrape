import tornado.ioloop
from pynostr.relay import Relay
from pynostr.base_relay import RelayPolicy
from pynostr.message_pool import MessagePool

class RelayGenerator:
    def __init__(self, relay_id: int):
        # TODO perform relay lookup
        self.timeout = 5
        self.url = "wss://relay.damus.io"
        self.message_pool = MessagePool(first_response_only=False)
        self.policy = RelayPolicy()
        self.io_loop = tornado.ioloop.IOLoop.current() 

    def _lookup_relay_url(self):
        # TODO function that looks up relay url by ID in DB
        self.url = ""

    def build(self) -> Relay:
        return Relay(
            self.url,
            self.message_pool,
            self.io_loop,
            self.policy,
            self.timeout
        )
    
    def create_subscription(self):
        pass

    def close_subscription(self):
        pass

    def _mark_subscription_closed(self):
        pass
    

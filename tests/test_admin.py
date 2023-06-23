from app.services.admin import Admin
from app.repository.models import Relay, RelayConfig
# Fixtures
from tests.fixtures import db_session, relay_name, relay_url, \
    dt_epoch_start, admin

class TestAdmin:
    def test_add_relay_w_config(
        self,
        admin: Admin, 
        relay_url: str,
        relay_name: str,
        dt_epoch_start: str,
    ):
        # relay = admin.add_relay_w_config(
        #     url=relay_url,
        #     name=relay_name,
        # )
        # Assert
        #assert type(relay.id) == int
        pass

    def test_get_relay_w_config_by_id(
        self, 
        admin: Admin,
    ):
        pass

    def get_all_relay_w_config(
        self, 
        admin: Admin
    ):
        pass

    def test_update_relay(
        self, 
        admin: Admin
    ):
        pass

    def test_update_relay_config(
        self, 
        admin: Admin
    ):
        pass


"""
        relay = Relay(
            url=relay_url, 
            name=relay_name
        )
        self.db_session.add(relay)
        self.db_session.flush()
        # Refresh instance
        self.db_session.refresh(relay)
        assert type(relay.id) == int # The first is inserted via alembic migrations
        # Attempt RelayConfig insert
        config = RelayConfig(
            relay_id=relay.id,
            epoch_start=dt_epoch_start
        )
        self.db_session.add(config)
        self.db_session.flush()
        # Refresh again
        assert config.relay_id == relay.id
"""
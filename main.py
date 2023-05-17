from services.examples.walk_known_relays import trial
from services.examples.walk_single_relay import start
from utils import generate_date_range_from_dts
from datetime import datetime, timedelta

if __name__ == "__main__":
    #trial()
    start()
    #today = datetime.today()
    #stop = today - timedelta(days=7)
    #print(generate_date_range_from_dts(old_point=stop, new_point=today))
    
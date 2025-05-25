from datetime import datetime
import os

rp = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + '/../')
dp = os.path.join(rp, 'history')
if not os.path.exists(dp):
    os.makedirs(dp)

# Global variables
websocket_is_connected = False
# try fix ssl.SSLEOFError: EOF occurred in violation of protocol (_ssl.c:2361)
ssl_Mutual_exclusion = False  # mutex read write
# if false websocket can sent self.websocket.send(data)
# else can not sent self.websocket.send(data)
ssl_Mutual_exclusion_write = False  # if thread write

SSID = None
DEMO = None

check_websocket_if_error = False
websocket_error_reason = None

balance_id = None
balance = None
balance_type = None
balance_updated = None
result = None
order_data = {}
order_open = []
order_closed = []
closed_deals = []
#open_orders = []
#closed_orders = []
trades = {}
stat = []
pairs = {}

loglevel = 'INFO'

# To get the payment details for the different pairs
PayoutData = None

def logger(message, lvl):
    if loglevel == 'DEBUG':
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        print('%s :[DEBUG]: %s' %(str(dt), str(message)))
    elif loglevel == lvl:
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        print('%s :[%s]: %s' %(str(dt), str(lvl), str(message)))
    elif lvl == 'ERROR':
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        print('%s :[ERROR]: %s' %(str(dt), str(message)))
    return


def set_cache(key, value, path=None):
    #data={"timestamp": int(time.time()), "value": value}
    data={"value": value}
    file = os.path.join(rp, str(key))
    if os.path.exists(file+".json"):
        os.remove(file+".json")
    with open(file+".json", "w") as k:
        json.dump(data, k, indent=4)


def check_cache(key, path=None):
    try:
        if path: file = os.path.join(dp, path, str(key))
        else: file = os.path.join(rp, str(key))
        if os.path.exists(file+".json"):
            return True
        return False
    except:
        return None


def get_cache(key, path=None):
    try:
        if path: file = os.path.join(dp, path, str(key))
        else: file = os.path.join(rp, str(key))
        with open(file+".json") as k:
            r = json.load(k)
        value = r.get('value')
        return value
    except:
        return None


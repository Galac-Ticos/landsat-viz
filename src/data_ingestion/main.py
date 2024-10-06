import os
from dotenv import load_dotenv
from proxy import Proxy

load_dotenv()

NASA_PASSWORD = os.getenv('NASA_PASSWORD')
NASA_USERNAME = os.getenv('NASA_USERNAME')

def main():
    p = Proxy(NASA_USERNAME, NASA_PASSWORD)
    p.fetch_scenes(9.9281,-84.0907,'2024-08-01','2024-10-05',0,datasets=['landsat_ot_c2_l2'])

if __name__ == "__main__":
    main()
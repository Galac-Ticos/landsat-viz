import os
from dotenv import load_dotenv
from proxy import Proxy
import utils

load_dotenv()

NASA_PASSWORD = os.getenv('NASA_PASSWORD')
NASA_USERNAME = os.getenv('NASA_USERNAME')


def main():
    p = Proxy(NASA_USERNAME, NASA_PASSWORD)

    p.fetch_scenes(latitude=9.9281, longitude=-84.0907, start_date='2024-08-01', end_date='2024-08-02',
                   max_cloud_cover=0, datasets=['landsat_ot_c2_l2'])

    utils.extract_tar_files('../data')


if __name__ == "__main__":
    main()

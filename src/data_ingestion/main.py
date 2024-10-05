from proxy import Proxy
def main():
    print("Running data ingestion pipeline...")
    username = "galac-ticos-api"
    password = "Galacticos123!"

    proxy = Proxy(username, password)

    scenes = proxy.search_scenes(
        dataset='landsat_tm_c2_l1',
        latitude=50.85,
        longitude=-4.35,
        start_date='1995-01-01',
        end_date='1995-10-01',
        max_cloud_cover=10
    )

    proxy.download_scene(scenes[0])

if __name__ == "__main__":
    main()
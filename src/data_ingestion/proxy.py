import json
from landsatxplore.api import API

class Proxy:
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

        self.api = API(username, password)

    def search_scenes(self, dataset, latitude, longitude, start_date, end_date, max_cloud_cover):
        scenes = self.api.search(
            dataset=dataset,
            latitude=latitude,
            longitude=longitude,
            start_date=start_date,
            end_date=end_date,
            max_cloud_cover=max_cloud_cover
        )
        return scenes
    
    def download_scene(self, scene):
        scene_id = scene['landsat_product_id']
        print(f"Downloading scene {scene_id}...")
<<<<<<< HEAD
from landsatxplore.api import API
from landsatxplore.earthexplorer import EarthExplorer

class Proxy:
    def __init__(self, username, password) -> None:
        self.__username = username
        self.__password = password
        self.__ee = EarthExplorer(self.__username, self.__password)
        self.__api = API(self.__username, self.__password)

    def search_scenes(self, datasets: list[str], latitude, longitude, start_date, end_date, max_cloud_cover):
        scenes = []
        for ds in datasets:
            scenes += self.__api.search(
                dataset=ds,
                latitude=latitude,
                longitude=longitude,
                start_date=start_date,
                end_date=end_date,
                max_cloud_cover=max_cloud_cover
            )
        print(scenes)
        return scenes

    def download_scene(self, scene) -> int:
        scene_id = scene['landsat_product_id']
        print(f"Downloading scene {scene_id}...")
        self.__ee.download(scene_id, output_dir='./data', overwrite=True)
        return 0

    def download_scenes(self, scenes: list):
        status = 0
        for scene in scenes:
            status |= self.download_scene(scene)
        return status
    
    def fetch_scenes(self, latitude, longitude, start_date, end_date, max_cloud_cover, datasets = ['landsat_ot_c2_l1', 'landsat_ot_c2_l2']):
        scenes = self.search_scenes(datasets,latitude,longitude,start_date,end_date,max_cloud_cover)
        status = self.download_scenes(scenes)
        return status
=======
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
>>>>>>> data_ingestion

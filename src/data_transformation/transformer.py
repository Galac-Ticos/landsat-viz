import utils


class Transformer:
    def __init__(self) -> None:
        self.user_form = None

    def get_scene_metadata(self, data_path='../data'):
        metadata_json = utils.find_metadata_json_files(data_path)[0]

        metadata_user = {
            "satellite": metadata_json["LANDSAT_METADATA_FILE"]["IMAGE_ATTRIBUTES"]["SPACECRAFT_ID"],
            "sensor": metadata_json["LANDSAT_METADATA_FILE"]["IMAGE_ATTRIBUTES"]["SENSOR_ID"],
            "date": metadata_json["LANDSAT_METADATA_FILE"]["IMAGE_ATTRIBUTES"]["DATE_ACQUIRED"],
            "cloud_cover": metadata_json["LANDSAT_METADATA_FILE"]["IMAGE_ATTRIBUTES"]["CLOUD_COVER"],
            "cloud_cover_land": metadata_json["LANDSAT_METADATA_FILE"]["IMAGE_ATTRIBUTES"]["CLOUD_COVER_LAND"],
            "image_quality": metadata_json["LANDSAT_METADATA_FILE"]["IMAGE_ATTRIBUTES"]["IMAGE_QUALITY_OLI"],
            "sun_elevation": metadata_json["LANDSAT_METADATA_FILE"]["IMAGE_ATTRIBUTES"]["SUN_ELEVATION"],
            "earth_sun_distance": metadata_json["LANDSAT_METADATA_FILE"]["IMAGE_ATTRIBUTES"]["EARTH_SUN_DISTANCE"],
        }

        return metadata_user

    def get_rgb_matrix(self, image_path=None):
        matrix = [[150, 150, 150], [150, 150, 150], [150, 150, 150]]
        return matrix

    def make_json_to_user(self, data_path='../data', image_path=None):
        metadata_user = self.get_scene_metadata(data_path)
        rgb_matrix = self.get_rgb_matrix(image_path)

        self.user_form = {
            "metadata": metadata_user,
            "rgb_matrix": rgb_matrix
        }

        return self.user_form

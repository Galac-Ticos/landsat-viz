from landsatxplore.earthexplorer import EarthExplorer

username = "galac-ticos-api"
password = "Galacticos123!"

ee = EarthExplorer(username, password)

ee.download('LC90150532022272LGN01', output_dir='./data')


ee.logout()
from landsatxplore.earthexplorer import EarthExplorer
ID = 'LC90150532024214LGN00'
username='galac-ticos-api'
password='Galacticos123!'
ee = EarthExplorer(username, password)
ee.download(ID, output_dir='./data', overwrite=True)

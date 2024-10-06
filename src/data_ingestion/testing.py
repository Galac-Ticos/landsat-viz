import sys
import os

# Add the directory containing earthexplorer.py to sys.path
module_path = os.path.join('landsat-module', 'landsatxplore-master', 'landsatxplore')
sys.path.append(module_path)

# Now you can import from earthexplorer
from earthexplorer import EarthExplorer 

ID = 'LC90150532024214LGN00'
username='galac-ticos-api'
password='Galacticos123!'
ee = EarthExplorer(username, password)
ee.download(ID, output_dir='./data', overwrite=True)

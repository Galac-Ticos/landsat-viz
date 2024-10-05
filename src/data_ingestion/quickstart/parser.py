from datetime import datetime

def convert_to_julian(year, month, day):
    """Convert a date to its Julian day."""
    date = datetime(year, month, day)
    return date.timetuple().tm_yday

def parse_landsat_scene(scene_identifier):
    """Parse the Landsat scene identifier and convert it to a standard Scene ID."""
    # Split the input scene identifier
    parts = scene_identifier.split('_')
    
    # Extract components
    satellite = parts[0][:3]  # LT5 -> LT5
    path_row = parts[2]        # 203025
    acquisition_date = parts[3]  # 19950815
    last_process_date = parts[4]  # 20200912 (not used in Scene ID)
    
    # Extract year, month, and day from acquisition date
    year = int(acquisition_date[:4])
    month = int(acquisition_date[4:6])
    day = int(acquisition_date[6:])
    
    # Convert acquisition date to Julian day
    julian_day = convert_to_julian(year, month, day)
    
    # Construct the final Scene ID
    ground_station_id = 'LGN'  # Example ground station identifier
    version_number = '00'       # Example version number
    
    scene_id = f"{satellite}{path_row}{year}{julian_day:03d}{ground_station_id}{version_number}"
    
    return scene_id

# Example usage
scene_identifier = "LC09_L1TP_015053_20220929_20230327_02_T1"
scene_id = parse_landsat_scene(scene_identifier)
print("Constructed Scene ID:", scene_id)
## Landsat Visualization Project

### Overview

The **Landsat Visualization Project** aims to leverage satellite imagery for comprehensive environmental monitoring and analysis. By utilizing data from NASA's Landsat program, we provide insights into land use changes, urban development, and ecological transformations over time. This project employs advanced visualization technologies to interpret and present Landsat data effectively.

### NASA Resources

Our project extensively utilizes resources from NASA, particularly the **Landsat API**, which provides access to a vast archive of satellite imagery collected since 1972. The Landsat program, jointly managed by NASA and the U.S. Geological Survey (USGS), offers invaluable data for understanding various environmental phenomena, including:

- Urban growth
- Deforestation
- Agricultural changes
- Climate change impacts

The Landsat data is freely available, significantly enhancing its use in research and application development. We access this data through platforms such as EarthExplorer and Google Earth Engine, enabling effective analysis and visualization of land cover changes.

### Technical Implementation

The project is structured into three main modules, each serving a specific purpose:

#### **1. Transformation Module**

- **Purpose**: Responsible for processing raw Landsat images.
- **Technologies Used**:
  - **OpenCV**: Employed for various image transformation techniques to enhance visual quality.
- **Key Functions**:
  - Image filtering
  - Edge detection
  - Color adjustments

#### **2. Front End Module**

- **Purpose**: Provides an interactive user interface for exploring visualized data.
- **Technologies Used**:
  - **React**: Utilized to build a responsive and user-friendly interface.
- **Key Features**:
  - Seamless navigation through datasets
  - Interactive visualizations of transformed images

#### **3. Data Ingestion Module**

- **Purpose**: Handles the retrieval of Landsat data from the API.
- **Technologies Used**:
  - **Python**: Implemented for robust data handling capabilities.
- **Key Functions**:
  - Fetching the latest satellite imagery
  - Preparing data for processing and visualization

### API Integration

For our data ingestion, we utilize the **landsatxplore** API, which has been installed as a wheel file. This package facilitates easy access to Landsat imagery through its command-line interface and Python API, allowing us to search for and download scenes efficiently. You can find the repository for this API [here](https://github.com/yannforget/landsatxplore).

### Collaborators

This project was developed collaboratively by:

- Alex Brenes
- Marco Ferraro
- Giancarlo Solorzano
- David Villalobos

### Use of AI in Our Project

We employed several AI tools to enhance data processing and image transformation:

- **Perplexity**: Instrumental in refining our data analysis process, allowing efficient filtering and extraction of relevant information.
- **OpenCV**: Utilized for image transformation tasks, enhancing visual representations of satellite imagery through various image processing techniques.

These AI tools have improved the quality of our visualizations and facilitated a more robust analysis of Landsat data.

### Conclusion

The Landsat Visualization Project exemplifies the integration of advanced technology with valuable scientific data. By leveraging NASA's resources and employing AI tools for processing, we aim to contribute meaningful insights into environmental monitoring and land use analysis. This project stands as a testament to the potential of open data and innovative technology in addressing global challenges.

### Repository Information

For further details and access to the codebase, please visit our GitHub repository: [Landsat Visualization Project Repository](https://github.com/Galac-Ticos/landsat-viz).

#### Resources

[1] <https://www.usgs.gov/landsat-missions/landsat-satellite-missions>
[2] <https://svs.gsfc.nasa.gov/11433/>
[3] <https://landsat.gsfc.nasa.gov/data/>
[4] <https://www.nv5geospatialsoftware.com/docs/TimeSeriesTutorial.html>
[5] <https://landsat.gsfc.nasa.gov/satellites/landsat-next/>
[6] <https://earth.esa.int/eogateway/missions/landsat>
[7] <https://github.com/mapbox/landsat-tiler/blob/master/README.md>
[8] <https://pypi.org/project/landsatxplore/>

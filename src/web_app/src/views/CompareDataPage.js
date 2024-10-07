import React, { useState, useEffect} from "react";
import {
  Container,
  Table,
  Button,
  Form,
  FormGroup,
  Label,
  Input,
} from "reactstrap";
import Navbar from "components/Navbar.js";
import Footer from "components/Footer.js";
import { Grid, Paper } from "@mui/material";
import { Row, Col } from "react-bootstrap";

function CompareDataPage() {
  const BASE_HOST = "https://landsat-viz-7c4bd6683246.herokuapp.com";

  const metadata_user = {
    metadata: {
      satellite: "LANDSAT_9",
      sensor: "OLI_TIRS",
      date: "2024-08-01",
      cloud_cover: "75.58",
      cloud_cover_land: "82.98",
      image_quality: "9",
      sun_elevation: "62.58520182",
      earth_sun_distance: "1.0149148",
    },
    rgb_matrix: [
      [
        [34, 139, 34],
        [139, 69, 19],
        [0, 128, 128],
      ],
      [
        [160, 82, 45],
        [0, 100, 0],
        [70, 130, 180],
      ],
      [
        [139, 69, 19],
        [34, 139, 34],
        [0, 128, 128],
      ],
    ],
  };

  const [locations, setLocations] = useState([]);

  const fetchLocations = async () => {
    const token = localStorage.getItem("authToken");

    try {
      const response = await fetch(BASE_HOST + "/locations", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Error fetching locations");
      }

      const data = await response.json();
      setLocations(data.map(location => `${location.latitude}, ${location.longitude}`));
    } catch (err) {
    }
  };

  useEffect(() => {
    fetchLocations();
  }, []);

  const [data, setData] = useState(metadata_user);
  const [selectCollection, setselectCollection] = useState("");
  const [selectedDate, setSelectedDate] = useState("");
  const [selectLocation, setselectLocation] = useState(locations);
  const [threshold, setThreshold] = useState(0.70);

  const collections = [
    "Landsat 8 Collection 2 Level 1    landsat_ot_c2_l1",
    "Landsat 8 Collection 2 Level 2    landsat_ot_c2_l2",
    "Landsat 9 Collection 2 Level 1    landsat_ot_c2_l1",
    "Landsat 9 Collection 2 Level 2    landsat_ot_c2_l2"
  ];

  const rgbToCss = (rgbObj) => {
    return `rgb(${rgbObj[0]}, ${rgbObj[1]}, ${rgbObj[2]})`;
  };

  const handleSubmit = () => {
    console.log("Selected collection:", selectCollection);
    console.log("Selected Date:", selectedDate);
    console.log("Selected location:", selectLocation);
  };

  return (
    <>
      <Navbar />
      <div className="page-header clear-filter" filter-color="blue">
        <div
          className="page-header-image"
          style={{
            backgroundImage: "url(" + require("assets/img/login.jpg") + ")",
          }}
        ></div>
        <div className="content" style={{ marginTop: "80px" }}>
          <Container style={{ maxWidth: "400px", marginTop: "10px" }}>
            <Form>
              <FormGroup >
                <Label for="collection">Collection</Label>
                <Input
                  type="select"
                  id="collection"
                  value={selectCollection}
                  onChange={(e) => setselectCollection(e.target.value)}
                >
                  <option value="" disabled>
                    Select a collection
                  </option>
                  {collections.map((name, index) => (
                    <option key={index} value={name}>
                      {name}
                    </option>
                  ))}
                </Input>

                <Label for="datePicker">Select Date</Label>
                <Input
                  type="date"
                  id="datePicker"
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                  max={new Date().toISOString().split("T")[0]}
                />

                <Label for="locations">Locations</Label>
                <Input
                  type="select"
                  id="locations"
                  value={selectLocation}
                  onChange={(e) => setselectLocation(e.target.value)}
                >
                  <option value="" disabled>
                    Select a location
                  </option>
                  {locations.map((value, index) => (
                    <option key={index} value={value}>
                      {value}
                    </option>
                  ))}
                </Input>

                <Label for="threshold">Threshold</Label>
                <Input
                  type="float"
                  id="threshold"
                  value={threshold}
                  onChange={(e) => setThreshold(e.target.value)}
                  max={1}
                  min={0}
                />
              </FormGroup>

              <Button color="primary" onClick={handleSubmit}>
                Submit
              </Button>
            </Form>
          </Container>
          <Row>
            <Col>
              <Grid
                container
                spacing={0.1}
                style={{ width: "300px", margin: "auto" }}
              >
                {data.rgb_matrix.map((row, rowIndex) => (
                  <Grid container item xs={12} key={rowIndex} spacing={0.1}>
                    {row.map((cell, cellIndex) => (
                      <Grid item xs={4} key={cellIndex}>
                        <Paper
                          style={{
                            backgroundColor: rgbToCss(cell),
                            height: "100px",
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            color: "#fff",
                            fontWeight: "bold",
                          }}
                          square
                        ></Paper>
                      </Grid>
                    ))}
                  </Grid>
                ))}
              </Grid>
            </Col>

            <Col style={{ maxWidth: "400px", marginRight: "300px" }}>
              <Table bordered size="sm" style={{ backgroundColor: "white" }}>
                <thead>
                  <tr>
                    <th>Variable</th>
                    <th>Value</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(data.metadata).map(([key, value], index) => (
                    <tr key={index}>
                      <td>{key}</td>
                      <td>{value}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
            </Col>
          </Row>
        </div>
        <Footer />
      </div>
    </>
  );
}

export default CompareDataPage;

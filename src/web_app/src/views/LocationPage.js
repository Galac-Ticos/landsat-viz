import React, { useState, useEffect } from 'react';
import { Container, Table, Spinner } from 'reactstrap';
import Navbar from "components/Navbar.js";
import Footer from "components/Footer.js";

function LocationsPage() {
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const BASE_HOST = "https://landsat-viz-7c4bd6683246.herokuapp.com"

  const fetchLocations = async () => {
    const token = localStorage.getItem("authToken");
  
    try {
      const response = await fetch(BASE_HOST + '/locations', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
  
      if (!response.ok) {
        throw new Error('Error fetching locations');
      }
  
      const data = await response.json();
      setLocations(data);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };
  

  useEffect(() => {
    // Obtener las ubicaciones al montar el componente
    fetchLocations();
  }, []);

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
        <div className="content">
          <Container className="mt-5" style={{ maxWidth: "600px" }}>
            <h3>Locations</h3>

            {loading && <Spinner color="primary" />}

            {error && <p style={{ color: 'red' }}>{error}</p>}

            {!loading && !error && (
              <Table bordered size="sm" style={{ background: "white"}}>
                <thead>
                  <tr>
                    <th>Latitude</th>
                    <th>Longitude</th>
                    <th>Description</th>
                  </tr>
                </thead>
                <tbody>
                  {locations.length > 0 ? (
                    locations.map((location, index) => (
                      <tr key={index}>
                        <td>{location.latitude}</td>
                        <td>{location.longitude}</td>
                        <td>{location.description}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="3" className="text-center">
                        No locations found
                      </td>
                    </tr>
                  )}
                </tbody>
              </Table>
            )}
          </Container>
        </div>
        <Footer />
      </div>
    </>
  );
}

export default LocationsPage;

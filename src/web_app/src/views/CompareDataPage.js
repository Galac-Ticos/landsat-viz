import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, CardBody } from 'reactstrap';

function CompareDataPage() {
    const VAR_TO_REMOVE = [
        [{"color": "#ff0000"}, {"color": "#00ff00"}, {"color": "#0000ff"}],
        [{"color": "#0000ff"}, {"color": "#0000ff"}, {"color": "#0000ff"}], 
        [{"color": "#0000ff"}, {"color": "#0000ff"}, {"color": "#0000ff"}],
    ] 
    const [data, setData] = useState(VAR_TO_REMOVE);

  return (
    <Container className="mt-5">
      <Row>
        {data.map((item, index) => (
          <Col key={index} md="4" className="mb-4">
            <Card style={{ backgroundColor: item.color }}>
              <CardBody>
                <h5 className="text-white">Card {index + 1}</h5>
              </CardBody>
            </Card>
          </Col>
        ))}
      </Row>
    </Container>
  );
}

export default CompareDataPage;

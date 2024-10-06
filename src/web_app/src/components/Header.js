import React from "react";
import { Container } from "reactstrap";

function Header() {
  return (
    <>
      <div className="page-header clear-filter" filter-color="blue">
        <div
          className="page-header-image"
          style={{
            backgroundImage: "url(" + require("assets/img/header.png") + ")"
          }}
          
        ></div>
        <Container>
          <div className="content-center brand">
            <i className="h1-seo now-ui-icons objects_spaceship"> <p>Landsat viz</p> </i>
            <h3>Visualize and compare Landsat satellite </h3>
          </div>
        </Container>
      </div>
    </>
  );
}

export default Header;

import React from "react";

import Navbar from "components/Navbar.js";
import Footer from "components/Footer.js";
import {
  Container
} from "reactstrap";

function HomePage() {
  let pageHeader = React.createRef();

  React.useEffect(() => {
    if (window.innerWidth > 991) {
      const updateScroll = () => {
        let windowScrollTop = window.pageYOffset / 3;
        pageHeader.current.style.transform =
          "translate3d(0," + windowScrollTop + "px,0)";
      };
      window.addEventListener("scroll", updateScroll);
      return function cleanup() {
        window.removeEventListener("scroll", updateScroll);
      };
    }
  });

  React.useEffect(() => {
    document.body.classList.add("index-page");
    document.body.classList.add("sidebar-collapse");
    document.documentElement.classList.remove("nav-open");
    window.scrollTo(0, 0);
    document.body.scrollTop = 0;
    return function cleanup() {
      document.body.classList.remove("index-page");
      document.body.classList.remove("sidebar-collapse");
    };
  });
  return (
    <>
      <Navbar />
      <div className="wrapper">
      <div className="page-header clear-filter" filter-color="blue">
          <div
            className="page-header-image"
            style={{
              backgroundImage: "url(" + require("assets/img/header.png") + ")"
            }}
            ref={pageHeader}
          ></div>
          <Container>
            <div className="content-center brand">
              <i className="h1-seo now-ui-icons objects_spaceship"> <p data-testid="landsat-viz-text">Landsat viz</p> </i>
              <h3>Visualize and compare Landsat data </h3>
            </div>
          </Container>
        </div>
        <Footer />
      </div>
    </>
  );
}

export default HomePage;

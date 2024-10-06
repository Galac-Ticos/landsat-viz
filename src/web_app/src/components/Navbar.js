import React from "react";
import { Link } from "react-router-dom";
import CRImage from 'assets/img/flags/CR.jpg';
import {
  Collapse,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  UncontrolledDropdown,
  NavbarBrand,
  Navbar as ReactNavbar,
  NavItem,
  NavLink,
  Nav,
  Container,
} from "reactstrap";

function Navbar() {
  const [navbarColor, setNavbarColor] = React.useState("navbar-transparent");
  const [collapseOpen, setCollapseOpen] = React.useState(false);
  React.useEffect(() => {
    const updateNavbarColor = () => {
      if (
        document.documentElement.scrollTop > 399 ||
        document.body.scrollTop > 399
      ) {
        setNavbarColor("");
      } else if (
        document.documentElement.scrollTop < 400 ||
        document.body.scrollTop < 400
      ) {
        setNavbarColor("navbar-transparent");
      }
    };
    window.addEventListener("scroll", updateNavbarColor);
    return function cleanup() {
      window.removeEventListener("scroll", updateNavbarColor);
    };
  });
  return (
    <>
      {collapseOpen ? (
        <div
          id="bodyClick"
          onClick={() => {
            document.documentElement.classList.toggle("nav-open");
            setCollapseOpen(false);
          }}
        />
      ) : null}
      <ReactNavbar className={"fixed-top " + navbarColor} expand="lg" color="info">
        <Container>
          <div className="navbar-translate">
            <NavbarBrand href="/" target="_blank" id="navbar-brand" >
             <img
                src={CRImage}
                alt="Landsat Icon"
                style={{ width: "auto", height: "24px", marginRight: "10px" }}
              />
              <p>Landsat viz</p>
            </NavbarBrand>   
          </div>
          <Collapse
            className="justify-content-end"
            isOpen={collapseOpen}
            navbar
          >
            <Nav navbar>
              <NavItem>
                <NavLink href="/login">
                  <i className="now-ui-icons users_single-02"></i>
                  <p>Login</p>
                </NavLink>
              </NavItem>
              <NavItem>
                <NavLink href="/notifications">
                  <i className="now-ui-icons ui-1_bell-53"></i>
                  <p>Notifications</p>
                </NavLink>
              </NavItem>
              <NavItem>
                <NavLink href="/compare-data">
                  <i className="now-ui-icons objects_spaceship"></i>
                  <p>Compare Data</p>
                </NavLink>
              </NavItem>
              <NavItem>
                <NavLink href="/locations">
                  <i className="now-ui-icons location_pin"></i>
                  <p>Locations</p>
                </NavLink>
              </NavItem>
              <UncontrolledDropdown nav>
                <DropdownToggle
                  caret
                  color="default"
                  href="/profile"
                  nav
                  onClick={(e) => e.preventDefault()}
                >
                  <i className="now-ui-icons users_single-02 mr-1"></i>
                  <p>Profile</p>
                </DropdownToggle>
                <DropdownMenu>
                  <DropdownItem to="/settings" tag={Link}>
                    <i className="now-ui-icons ui-1_settings-gear-63 mr-1"></i>
                    Settings
                  </DropdownItem>
                  <DropdownItem href="/login" tag={Link}>
                    <i className="now-ui-icons ui-1_simple-remove mr-1"></i>
                    Logout
                  </DropdownItem>
                </DropdownMenu>
              </UncontrolledDropdown>
            </Nav>
          </Collapse>
        </Container>
      </ReactNavbar>
    </>
  );
}

export default Navbar;

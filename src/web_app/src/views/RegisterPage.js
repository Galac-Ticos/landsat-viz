import React, { useState, useEffect } from "react";
import {
  Button,
  Card,
  CardBody,
  CardFooter,
  Form,
  Input,
  InputGroupAddon,
  InputGroupText,
  InputGroup,
  Container,
  Col,
} from "reactstrap";
import { useNavigate } from "react-router-dom";
import Navbar from "components/Navbar.js";
import Footer from "components/Footer.js";

function RegisterPage() {
  const [firstFocus, setFirstFocus] = useState(false);
  const [lastFocus, setLastFocus] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isValid, setIsValid] = useState(false);
  const navigate = useNavigate();
  const BASE_HOST = "https://landsat-viz-7c4bd6683246.herokuapp.com";

  useEffect(() => {
    document.body.classList.add("login-page");
    document.body.classList.add("sidebar-collapse");
    document.documentElement.classList.remove("nav-open");
    window.scrollTo(0, 0);
    document.body.scrollTop = 0;

    return function cleanup() {
      document.body.classList.remove("login-page");
      document.body.classList.remove("sidebar-collapse");
    };
  }, []);

  useEffect(() => {
    setIsValid(email !== "" && password !== "");
  }, [email, password]);

  const createCRLocation = async () => {
    const token = localStorage.getItem("authToken");
  
    try {
      const response = await fetch(`${BASE_HOST}/auth`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });
      if (!response.ok) {
        throw new Error('Error to create CR location');
      }
      const data = await response.json();
      if (response.ok && data.token) {
        const response2 = await fetch(BASE_HOST + '/locations', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${data.token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            latitude:9.9281, 
            longitude:-84.0907,
            description:"Costa Rica"
          }),
        });
        if (!response2.ok) {
          throw new Error('Error to create CR location');
        }
      }
  
    } catch (err) {
      console.log(err.message);
    }
  };

  const handleRegister = async () => {
    try {
      const response = await fetch(`${BASE_HOST}/users`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        await createCRLocation()
        navigate("/login");
        alert("Registration successful!");
      } else {
        alert(data.error || "Registration failed");
      }
    } catch (error) {
      console.error("Error during registration:", error);
      alert("Something went wrong. Please try again.");
    }
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
        <div className="content">
          <Container>
            <Col className="ml-auto mr-auto" md="4">
              <Card className="card-login card-plain">
                <Form action="" className="form" method="">
                  <CardBody>
                    <h3 className="h1-seo mb-4"> Register </h3>
                    <InputGroup
                      className={
                        "no-border input-lg" +
                        (firstFocus ? " input-group-focus" : "")
                      }
                    >
                      <InputGroupAddon addonType="prepend">
                        <InputGroupText>
                          <i className="now-ui-icons ui-1_email-85"></i>
                        </InputGroupText>
                      </InputGroupAddon>
                      <Input
                        placeholder="Email..."
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        onFocus={() => setFirstFocus(true)}
                        onBlur={() => setFirstFocus(false)}
                      />
                    </InputGroup>
                    <InputGroup
                      className={
                        "no-border input-lg" +
                        (lastFocus ? " input-group-focus" : "")
                      }
                    >
                      <InputGroupAddon addonType="prepend">
                        <InputGroupText>
                          <i className="now-ui-icons ui-1_lock-circle-open"></i>
                        </InputGroupText>
                      </InputGroupAddon>
                      <Input
                        placeholder="Password..."
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        onFocus={() => setLastFocus(true)}
                        onBlur={() => setLastFocus(false)}
                      />
                    </InputGroup>
                  </CardBody>
                  <CardFooter className="text-center">
                    <Button
                      block
                      className="btn-round"
                      color="info"
                      size="lg"
                      onClick={handleRegister}
                      disabled={!isValid}
                    >
                      Register
                    </Button>
                  </CardFooter>
                </Form>
              </Card>
            </Col>
          </Container>
        </div>
        <Footer />
      </div>
    </>
  );
}

export default RegisterPage;

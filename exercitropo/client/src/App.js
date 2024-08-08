import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from "./pages/Home";
import Instructions from "./pages/Instructions";
import ExerciTropo from "./pages/ExerciTropo";
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';

function App() {
  const MyNavbar = () => {
    return (
      <Navbar bg="light" expand="lg">
        <Navbar.Brand href="https://rice.dibris.unige.it/about-us/">Lorenza Saettone Unige, Dip Dibris, Lab Rice - Automazione del training ExerciTropo</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link as={Link} to="/">Home</Nav.Link>
            <Nav.Link as={Link} to="/instructions/1">DebugInstr</Nav.Link>
            <Nav.Link as={Link} to="/ExerciTropo/1">DebugExerciTropo</Nav.Link>
            
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    );
  };

  return (
    <Router>
      <div>
        <MyNavbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/instructions/:index" element={<Instructions />} />
          <Route path="/ExerciTropo/:index" element={<ExerciTropo />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

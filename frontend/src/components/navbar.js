import React from 'react'
import {Navbar, Nav, NavDropdown} from 'react-bootstrap'

const navbar = () => {
    return (
  <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
  <Navbar.Brand href="#home">RecomMedia</Navbar.Brand>
  <Navbar.Toggle aria-controls="responsive-navbar-nav" />
  <Navbar.Collapse id="responsive-navbar-nav">
    <Nav className="mr-auto">
      <Nav.Link href="#features">Features</Nav.Link>
      <Nav.Link href="#pricing">Pricing</Nav.Link>
      <NavDropdown title="Dropdown" id="collasible-nav-dropdown">
        <NavDropdown.Item href="#action/3.1">Movie List</NavDropdown.Item>
        <NavDropdown.Item href="#action/3.2">Login</NavDropdown.Item>
        <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
        <NavDropdown.Divider />
        <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
      </NavDropdown>
    </Nav>
    <Nav>
      <Nav.Link href="#details">Details</Nav.Link>
      <Nav.Link eventKey={2} href="#OtherThing">
        Other Thing
      </Nav.Link>
    </Nav>
  </Navbar.Collapse>
</Navbar>
    );
}

export default navbar;
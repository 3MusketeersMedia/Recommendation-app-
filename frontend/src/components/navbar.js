import React from 'react'
import {Navbar, Nav, NavDropdown} from 'react-bootstrap'
import {AppContext} from '../AppContext';

const MyNav = () => {
    return <AppContext.Consumer>
      {context => <div>
        <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
        <Navbar.Brand href="/">RecomMedia</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link href="/list">Movie List</Nav.Link>
            <Nav.Link href="/login">Login</Nav.Link>
            <NavDropdown title="Dropdown" id="collasible-nav-dropdown">
              <NavDropdown.Item href="#action/3.1">Item 1</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.2">Item 2</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.3">Item 3</NavDropdown.Item>
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
      </div>}
    </AppContext.Consumer>;
}

export default MyNav;

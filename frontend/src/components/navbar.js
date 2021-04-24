import React from 'react'
import {Navbar, Nav, NavDropdown, Form, FormControl, Button} from 'react-bootstrap'
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
            <Nav.Link href="#" onClick={context.openLoginModal}>Login</Nav.Link>
            <NavDropdown title="Dropdown" id="collasible-nav-dropdown">
              <NavDropdown.Item href="#action/3.1">Item 1</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.2">Item 2</NavDropdown.Item>
              <NavDropdown.Item href="#action/3.3">Item 3</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
            </NavDropdown>
          </Nav>
          <Nav>
            <Form inline>
      <FormControl type="text" placeholder="Search" className="mr-sm-2" />
      <Button variant="outline-light">Search</Button>
    </Form>
          </Nav>
          </Navbar.Collapse>
        </Navbar>
      </div>}
    </AppContext.Consumer>;
}

export default MyNav;

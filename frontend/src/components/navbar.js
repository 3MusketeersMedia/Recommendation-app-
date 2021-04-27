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
            <Nav.Link href="/login">Login</Nav.Link>
          </Nav>
          <Nav>
            <NavDropdown title="Advanced Search" id="collasible-nav-dropdown">
              <div>
                <div>Genre:<input></input></div>
                <div>Year:<input></input></div>
              </div>
              <NavDropdown.Divider />
              <Button variant = "outline-dark">Search</Button>
            </NavDropdown>
          </Nav>
          <Nav>
            <Form inline>
              <FormControl type="text" placeholder="Search by title" className="mr-sm-2" />
              <Button variant="outline-light">Search</Button>
            </Form>
          </Nav>
          </Navbar.Collapse>
        </Navbar>
      </div>}
    </AppContext.Consumer>;
}

export default MyNav;

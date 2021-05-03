import React, { useState } from 'react'
import {Navbar, Nav, NavDropdown, Form, FormControl, Button} from 'react-bootstrap'
import {AppContext} from '../AppContext';
import './navbar.css';

const MyNav = () => {
    const [searchContents, changeSC] = useState(null);
    const [genre, changeGenre] = useState(null);
    const [minYear, changeMinYear] = useState(null);
    const [maxYear, changeMaxYear] = useState(null);
    const [minRate, changeMinRate] = useState(null);
    const [maxRate, changeMaxRate] = useState(null);
    
    function getSearchConts(val)
    {
      changeSC(val.target.value);
      console.warn(val.target.value);
    }
    function getGenre(val)
    {
      changeGenre(val.target.value);
      console.warn(val.target.value);
    }
    function getMinYear(val)
    {
      changeMinYear(val.target.value);
      console.warn(val.target.value);
    }
    function getMaxYear(val)
    {
      changeMaxYear(val.target.value);
      console.warn(val.target.value);
    }
    function getMinRate(val)
    {
      changeMinRate(val.target.value);
      console.warn(val.target.value);
    }
    function getMaxRate(val)
    {
      changeMaxRate(val.target.value);
      console.warn(val.target.value);
    }

    // Performs normal, not advanced search (by name)
    async function normalSearch()
    {
      const response = await fetch('http://localhost:5000/search', {
        method: 'GET',
        headers: {
          'content-type': 'application/json',
        },
        body: JSON.stringify({searchContents}),
      });
      console.log(response);
      const data = await response.json();
      console.log(data);
    }

    // Performs advanced search
    async function advancedSearch()
    {
      const response = await fetch('http://localhost:5000/advSearch', {
        method: 'GET',
        headers: {
          'content-type': 'application/json',
        },
        body: JSON.stringify({genre, minYear, maxYear, minRate, maxRate}),
      });
      console.log(response);
      const data = await response.json();
      console.log(data);
    }
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
                <div>Genre:
                  <div className = "searchTab">
                    <input className = "fullSizeInput" onChange = {getGenre}/>
                  </div>
                </div>
                <div>Year (From, To):
                  <div className = "searchTab"> 
                    <input className = "halfSizeInput" onChange = {getMinYear}/>
                    <input className = "halfSizeInput" onChange = {getMaxYear}/>
                  </div>
                </div>
                <div>Rating (From, To):
                  <div className = "searchTab"> 
                    <input className = "halfSizeInput" onChange = {getMinRate}/>
                    <input className = "halfSizeInput" onChange = {getMaxYear}/>
                  </div>
                </div>
              </div>
              <NavDropdown.Divider />
              <Button variant = "outline-dark" onClick = {advancedSearch}>Search</Button>
            </NavDropdown>
          </Nav>
          <Nav>
            <Form inline>
              <FormControl type="text" placeholder="Search by title" className="mr-sm-2" onChange = {getSearchConts}/>
              <Button variant="outline-light" onClick = {normalSearch}>Search</Button>
            </Form>
          </Nav>
          </Navbar.Collapse>
        </Navbar>
      </div>}
    </AppContext.Consumer>;
}

export default MyNav;

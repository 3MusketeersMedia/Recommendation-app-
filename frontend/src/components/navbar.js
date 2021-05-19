import React, { useState, useContext } from 'react'
import {Navbar, Nav, NavDropdown, FormGroup, FormControl, Button} from 'react-bootstrap'
import {AppContext} from '../AppContext';
import './navbar.css';

const MyNav = () => {
    const [searchContents, changeSC] = useState(null);
    const [name, changeName] = useState(null);
    const [mediaType, changeMediaType] = useState(null);
    const [genre, changeGenre] = useState(null);
    const [minYear, changeMinYear] = useState(null);
    const [maxYear, changeMaxYear] = useState(null);
    const [minRate, changeMinRate] = useState(null);
    const [maxRate, changeMaxRate] = useState(null);
    const context = useContext(AppContext);

    function getSearchConts(val)
    {
      changeSC(val.target.value);
      console.warn(val.target.value);
    }
    function getName(val)
    {
      changeName(val.target.value);
      console.warn(val.target.value);
    }
    function getMediaType(val)
    {
      changeMediaType(val.target.value);
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
      context.actions.search(searchContents);
    }

    // Performs advanced search
    async function advancedSearch()
    {
      context.actions.advancedSearch(name, mediaType, genre, minYear, minRate, maxYear, maxRate);
    }
    return <AppContext.Consumer>
      {context => <div>
        <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
        <Navbar.Brand href="/">RecomMedia</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link href="/list">Media List</Nav.Link>
          </Nav>
          <Nav>
            {context.store.token && context.store.token !== "" && context.store.token !== undefined ?
              <> <Nav.Link onClick={() => context.actions.logout()}>Signout</Nav.Link>
              <Nav.Link href="/user/profile"> Profile </Nav.Link></>:
              <><Nav.Link href="/login">Login</Nav.Link>
              <Nav.Link href="/login"> Profile </Nav.Link> </>
            }
            <NavDropdown title="Advanced Search" id="collasible-nav-dropdown">
              <div>
              <div>Name:
                  <div className = "searchTab">
                    <input className = "fullSizeInput" onChange = {getName}/>
                  </div>
              </div>
              <div>Media Type:
                <div className = "searchTab">
                  <input className = "fullSizeInput" onChange = {getMediaType}/>
                </div>
              </div>
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
                    <input className = "halfSizeInput" onChange = {getMaxRate}/>
                  </div>
                </div>
              </div>
              <NavDropdown.Divider />
              <Button variant = "outline-dark" onClick = {advancedSearch}>Search</Button>
            </NavDropdown>
          </Nav>
          <Nav>
            <div className = "searchBar">
              <FormControl
              type="text"
              placeholder="Search by title"
              className="mr-sm-2"
              onKeyPress={event => {
                if (event.key === "Enter") {
                  normalSearch();
                }
              }}
              onChange = {getSearchConts}/>
            </div>
            <Button variant="outline-light" onClick = {normalSearch}>Search</Button>
          </Nav>
          </Navbar.Collapse>
        </Navbar>
      </div>}
    </AppContext.Consumer>;
}

export default MyNav;

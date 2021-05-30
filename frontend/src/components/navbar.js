import React, { useState, useContext } from 'react'
import {Navbar, Nav, NavDropdown,  FormControl, Button} from 'react-bootstrap'
import {AppContext} from '../AppContext';
import LoginPage from '../pages/LoginPage'
import './navbar.css';
import logo from '../pics/logo.png';

const MyNav = () => {
    // The following hooks are used to edit variables involved with searching
    const [searchContents, changeSC] = useState(null);
    const [name, changeName] = useState(null);
    const [mediaType, changeMediaType] = useState(null);
    const [genre, changeGenre] = useState(null);
    const [minYear, changeMinYear] = useState(null);
    const [maxYear, changeMaxYear] = useState(null);
    const [minRate, changeMinRate] = useState(null);
    const [maxRate, changeMaxRate] = useState(null);
    const context = useContext(AppContext);

    // These functions edit the react hooks
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
        <Navbar className = "bar py-0" expand="lg"  bg="dark" variant="dark">
        <Navbar.Brand href="/">
        <img className="logo" src={logo} alt="Logo Img"/>
        RecomMedia
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse className = "collapse" id="responsive-navbar-nav">
          <Nav className="mr-auto">
            {context.store.token && context.store.token !== "" && context.store.token !== undefined ?
            <> <Nav.Link onClick = {context.actions.getUserRecs}>Recommendations</Nav.Link></>:null}
          </Nav>
          <Nav>
            {context.store.token && context.store.token !== "" && context.store.token !== undefined ?
              <> <Nav.Link onClick={() => context.actions.logout()}>Signout</Nav.Link>
              <Nav.Link href="/user/profile"> Profile </Nav.Link></>:
              <><Nav.Link href="#" onClick={context.actions.openLoginModal}>Login</Nav.Link>
              <Nav.Link href="#" onClick={context.actions.openLoginModal}> Profile </Nav.Link> </>
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
        <LoginPage show={context.store.loginModalShown} close={context.actions.closeLoginModal}/>
      </div>}
    </AppContext.Consumer>;
}

export default MyNav;

import React from 'react';
import {BrowserRouter, Route} from 'react-router-dom';
import ContextWrapper from './AppContext';
import MovieList from './pages/MovieList';
import ZoomedPage from './pages/zoomedpage';
import HomePage from './pages/HomePage.js';
import ProfilePage from './pages/ProfilePage.js';
import LoginPage from './pages/LoginPage.js';

export default class App extends React.Component {

  render() {
    return (
      <BrowserRouter>
        <ContextWrapper>
          <Route exact path='/' component={HomePage}/>
          <Route exact path='/list' component={MovieList}/>
          <Route exact path='/movie' component={ZoomedPage}/>
          <Route exact path='/user/profile' component={ProfilePage}/>
          <Route exact path='/login' component={LoginPage}/>
        </ContextWrapper>
      </BrowserRouter>
    );
  }
}

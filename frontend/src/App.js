import React from 'react';
import {BrowserRouter, Route, Redirect} from 'react-router-dom';
import {AppContext} from './AppContext'
import MovieList from './pages/MovieList';
import ZoomedPage from './zoomedpage';
import HomePage from './HomePage.js';

export default class App extends React.Component {
  constructor() {
    super();
    this.state = {
      movie: null,
    };
  }
  render() {
    const context = {
      movie: this.state.movie,
      setMovie: async (movie) => await this.setState({movie}),
    };
    return (
      <BrowserRouter>
        <AppContext.Provider value={context}>
          <Route exact path='/' component={HomePage}/>
          <Route exact path='/list' component={MovieList}/>
          <Route exact path='/movie' component={ZoomedPage}/>
        </AppContext.Provider>
      </BrowserRouter>
    );
  }
}

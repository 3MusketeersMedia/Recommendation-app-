import React from 'react';
import {BrowserRouter, Route, Redirect} from 'react-router-dom';
import {AppContext} from './AppContext'
import MovieList from './pages/MovieList';
import ZoomedPage from './pages/zoomedpage';
import HomePage from './pages/HomePage.js';

export default class App extends React.Component {
  constructor() {
    super();
    this.state = {
      movie: {},
    };
  }
  async componentDidMount() {
    const movie = JSON.parse(localStorage.getItem('movie'));
    await this.setState({movie});
  }
  setMovie = async(movie) => {
    localStorage.setItem('movie', JSON.stringify(movie));
    await this.setState({movie});
  }
  render() {
    const context = {
      movie: this.state.movie,
      setMovie: this.setMovie,
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

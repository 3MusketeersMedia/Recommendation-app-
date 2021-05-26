import React from 'react';
import {Container, Row, Col, ListGroup, Image} from 'react-bootstrap';
import {AppContext} from '../AppContext';
import MyNav from '../components/navbar';
import PageBar from '../components/PageBar';
import './MovieList.css';
import { withRouter, useHistory  } from "react-router-dom"

class MovieList extends React.Component {
  static contextType = AppContext;
  constructor() {
    super();
    this.state = {
      loading: false,
      movies: [],
      limit: 100,
      page: 1,
      count: 0
    };
  }
  componentDidMount() {
    this.loadMovies()
  }
  loadMovies = async () => {
    await this.setState({loading: true});
    const limit = this.state.limit;
    const offset = limit * (this.state.page - 1);
    const {movies, count} = await this.context.actions.loadMovies(limit, offset);
    await this.setState({movies, count, loading: false})
  }
  pageBack = async () => {
    await this.setState({page: this.state.page - 1});
    await this.loadMovies();
  }
  pageForward = async () => {
    await this.setState({page: this.state.page + 1});
    await this.loadMovies();
  }
  selectMovie = (movie) => {
    this.context.actions.setMovie(movie);
    this.props.history.push("/movie")
  }
  render() {
    console.log(this.state.movies);
    return <>
      {window.location.pathname != "/" ? <MyNav /> : null}
      <Container fluid className='p-3'>
        <PageBar forward={this.pageForward} back={this.pageBack} page={this.state.page}
          limit={this.state.limit} count={this.state.count}/>
        {this.state.movies.length === 0 && !this.state.loading ? (
          <p>No results</p>
        ) : ''}
        {this.state.loading ? (
          <p>Loading...</p>
        ) : ''}
        <Row>
          {this.state.movies.map(movie => (
            <Col xs={12} sm={6} md={4} lg={3} className='p-3 border' onClick={() => this.selectMovie(movie)}>
              <Row>
                <Image src={movie.link} className='movieImage mx-auto' style={{width: 'auto'}}/>
              </Row>
              <Row className='text-center'>
                <h5 className='w-100 mt-3 mb-0'>{movie.name}</h5>
              </Row>
            </Col>
          ))}
        </Row>
        {this.state.movies.length > 0 ? (
          <PageBar forward={this.pageForward} back={this.pageBack} page={this.state.page}
            limit={this.state.limit} count={this.state.count}/>
        ) : ''}
      </Container>
    </>;
  }
}

export default withRouter(MovieList);

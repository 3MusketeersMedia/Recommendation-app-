import React from 'react';
import {Container, Row, Col, ListGroup, Image} from 'react-bootstrap';
import {AppContext} from '../AppContext';

export default class MovieList extends React.Component {
  static contextType = AppContext;
  constructor() {
    super();
    this.state = {
      movies: [],
    };
  }
  async componentDidMount() {
    const response = await fetch('http://localhost:4000/movies');
    const movies = await response.json();
    console.log(movies);
    await this.setState({movies});
  }
  selectMovie(movie) {
    this.context.setMovie(movie);
    this.props.history.push('/movie');
  }
  render() {
    return (
      <Container fluid className='p-3'>
        <ListGroup>
          {this.state.movies.map(movie => (
            <ListGroup.Item key={movie.id} onClick={() => this.selectMovie(movie)}>
              <Row>
                <Col>
                  <Image src={movie.picture}/>
                </Col>
                <Col>
                  <h3>
                    {movie.title}
                  </h3>
                  <p>
                    {movie.Rating}/10
                  </p>
                  <p>
                    {movie.text}
                  </p>
                </Col>
              </Row>
            </ListGroup.Item>
          ))}
        </ListGroup>
      </Container>
    );
  }
}

import React from 'react';
import {Container, Row, Col, ListGroup, Image} from 'react-bootstrap';
import {AppContext} from '../AppContext';
import MyNav from '../components/navbar';

export default class MovieList extends React.Component {
  static contextType = AppContext;
  constructor() {
    super();
    this.state = {
      movies: [],
    };
  }
  async componentDidMount() {
    const response = await fetch('http://localhost:5000/movies');
    const movies = await response.json();
    console.log(movies);
    await this.setState({movies});
  }
  selectMovie(movie) {
    this.context.setMovie(movie);
    this.props.history.push('/movie');
  }
  render() {
    return <>
      <MyNav/>
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
    </>;
  }
}

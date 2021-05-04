import {useState, useContext} from 'react';
import Movies from "../components/moviePic"
import Header from "../components/header"
import Summary from "../components/summary"
import SimilarMovies from "../components/similarMovies"
import Rating from "../components/review"
import MyNav from '../components/navbar'
import Footer from '../components/Footer';
import {AppContext} from '../AppContext';
import {Container, Row, Col} from 'react-bootstrap'
import './zoomed-paged-grid.css';

function ZoomedPage() {
  const database_address = "http://localhost:4000/movies";
  const [simShowMovies, setSimMovies] = useState ([
      {
        "id": 1,
        "title": "Harry Potter and the Half-Blood Prince",
        "picture": "https://m.media-amazon.com/images/M/MV5BNzU3NDg4NTAyNV5BMl5BanBnXkFtZTcwOTg2ODg1Mg@@._V1_UX182_CR0,0,182,268_AL_.jpg",
        "Rating": "7.6",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
      },
      {
            "id": 2,
            "title": "Harry Potter and the Chamber of Secrets",
            "picture": "https://m.media-amazon.com/images/M/MV5BMTcxODgwMDkxNV5BMl5BanBnXkFtZTYwMDk2MDg3._V1_UX182_CR0,0,182,268_AL_.jpg",
            "Rating": "7.4",
            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        },
        {
            "id": 3,
            "title": "Harry Potter and the Prisoner of Azkaban",
            "picture": "https://m.media-amazon.com/images/M/MV5BMTY4NTIwODg0N15BMl5BanBnXkFtZTcwOTc0MjEzMw@@._V1_UX182_CR0,0,182,268_AL_.jpg",
            "Rating": "7.9",
            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
      },
      {
            "id": 4,
            "title": "Charlie and the Chocolate Factory",
            "picture": "https://m.media-amazon.com/images/M/MV5BNjcxMjg1Njg2NF5BMl5BanBnXkFtZTcwMjQ4NzMzMw@@._V1_UX182_CR0,0,182,268_AL_.jpg",
            "Rating": "6.6",
            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
      },
      {
            "id": 5,
            "title": "Harry Potter and the Deathly Hallows: Part 2 ",
            "picture": "https://m.media-amazon.com/images/M/MV5BMGVmMWNiMDktYjQ0Mi00MWIxLTk0N2UtN2ZlYTdkN2IzNDNlXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_UX182_CR0,0,182,268_AL_.jpg",
            "Rating": "8.1",
            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
      },
      {
            "id": 6,
            "title": "Fantastic Beasts and Where to Find Them",
            "picture": "https://m.media-amazon.com/images/M/MV5BMjMxOTM1OTI4MV5BMl5BanBnXkFtZTgwODE5OTYxMDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
            "Rating": "7.3",
            "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
      },
]);

    //Fetches individual movie from database
    const fetchMovies = async (id) => {
      const response = await fetch(database_address + `?id=${id}`)
      const data = await response.json()

      return data
    }

    const {store, actions} = useContext(AppContext); 
    if(store.movie == null)
      actions.syncMovies();

    return(
      <AppContext.Consumer>
        {context => <>
          <div id="content-wrap">
          <div className="NavBar">
          <MyNav /> 
          </div>
          <Container fluid>
            <Row>
              <Col ><Movies movie={context.store.movie}/></Col>
              <Col md={5} lg={9} className="p-3 mr-5 ">
                <Row className="MovieTitle">
                  <Header movie={context.store.movie}/>
                </Row>
                <Row className="Ratings">
                  <Rating movie={context.store.movie} />
                </Row>
                <Row className="Summary">
                  <Summary movie={context.store.movie}/>
                </Row>
              </Col>
            </Row>
            <Row>
              <Col ></Col>
              <Col  md={10} className="SimilarMovies">
                <h3 className='p-3' > Recommendations </h3>
               <SimilarMovies movies={simShowMovies}/>
              </Col>
            </Row>
          </Container>
          </div>
          <div id="footer">
          <Footer/>
          </div>
        </> }
      </AppContext.Consumer>
  );
}

export default ZoomedPage;


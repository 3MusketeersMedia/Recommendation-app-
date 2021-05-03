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


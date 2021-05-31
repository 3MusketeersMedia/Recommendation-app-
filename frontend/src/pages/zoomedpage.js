import React from 'react';
import Movies from "../components/moviePic"
import Header from "../components/header"
import Summary from "../components/summary"
import SimilarMovies from "../components/similarMovies"
import Rating from "../components/review"
import MyNav from '../components/navbar'
import Footer from '../components/Footer';
import {AppContext} from '../AppContext';
import {Container, Row} from 'react-bootstrap'
import ReactStars from "react-rating-stars-component";
import './zoomed-paged-grid.css';


export default class zoomedpage extends React.Component {
  static contextType = AppContext;
  constructor() {
    super();
    this.state = {
    rating: 0,
    recMovies: []
    };
  }

  componentDidMount() {
    let movie = this.context.store.movie; 
    this.loadMovies(movie.id, movie.mediatype || movie.mediaType);
    if(this.context.actions.checkedLogin()){
      this.context.actions.getRating(movie)
        .then(data => {
          if(data !== undefined){
              this.setState({rating: data});
          } else {
            console.log("Connection Error")
          }
        })
        .catch(err => {console.log(err);});
    }
  }

  loadMovies = async(media_id, mediaType) =>
  {
    const response = await fetch(this.context.store.address + `movie_recommendation?media_id=${media_id}&mediaType=${mediaType}`);
    const recMovies = await response.json();
    console.log(recMovies);
    await this.setState({recMovies});
  }

  ratingChanged = (newRating) => {
    this.setState({rating: newRating});
  };

  ratingSubmit = () => {
    let newRating = this.context.store.movie;
    newRating.rating = this.state.rating;
    console.log("hello");
    this.context.actions.setRating(newRating)
      .then(flag => {
        if(flag){
          alert("Rating has been changed to " + this.state.rating * 2);
        } else {
          if(!(this.context.actions.checkedLogin())){
            alert("Login to Rate")
            this.context.actions.openLoginModal();
          } else{
            alert("Connection Failed")
          }
        }
      })
      .catch(err => {console.log(err);});
  }

  render() {
    if(this.context.store.movie == null)
      this.context.actions.syncMovies();
    document.getElementById("where-to-render")
    return (
      <div>
        <AppContext.Consumer>
        {context => <>
          <div id="content-wrap">
          <div className="NavBar">
          <MyNav />
          </div>
          <Container fluid>
            <Row>
              <div className="MovieBanner">
                {console.log(context.store)}
                <img src={context.store.movie.link} alt="movie link"></img>
                  <Movies movie={context.store.movie}/>
              </div>
            </Row>
            <Row className="MovieTitle justify-content-center d-flex">
              <Header title={context.store.movie.name}/>
            </Row>
            <Row className="Ratings justify-content-center d-flex">
              <Rating movie={context.store.movie} />
            </Row>
            <Row className="mb-3 m-1 justify-content-center d-flex">
            <ReactStars classNames="text-center"
              count={5}
              value={this.state.rating}
              onChange={this.ratingChanged}
              size={24}
              isHalf={true}
              emptyIcon={<i className="far fa-star"></i>}
              halfIcon={<i className="fa fa-star-half-alt"></i>}
              fullIcon={<i className="fa fa-star"></i>}
              activeColor="#ffd700"
            />
            </Row>
            <Row className="justify-content-center d-flex">
            <button type="submit" className="btn btn-primary text-center"
                    onClick={this.ratingSubmit}>Submit Rating</button>
            </Row>
            <Row className="Summary justify-content-center d-flex m-5">
              <Summary movie={context.store.movie}/>
            </Row>
            <Row className="justify-content-center d-flex Recommendation-box">
                <h3 className='p-3' > Recommendations </h3>
              </Row>
            <Row className="SimilarMovies">
                <SimilarMovies movies={this.state.recMovies}/>
            </Row>
          </Container>
          </div>
          <div id="footer">
          <Footer/>
          </div>
        </> }
      </AppContext.Consumer>
      </div>
    )
  }
}

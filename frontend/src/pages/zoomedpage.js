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
      simShowMovies: [
        {
          "id": 1,
          "name": "Harry Potter and the Half-Blood Prince",
          "link": "https://m.media-amazon.com/images/M/MV5BNzU3NDg4NTAyNV5BMl5BanBnXkFtZTcwOTg2ODg1Mg@@._V1_UX182_CR0,0,182,268_AL_.jpg",
          "rating": "7.6",
          "summary": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        },
        {
              "id": 2,
              "name": "Harry Potter and the Chamber of Secrets",
              "link": "https://m.media-amazon.com/images/M/MV5BMTcxODgwMDkxNV5BMl5BanBnXkFtZTYwMDk2MDg3._V1_UX182_CR0,0,182,268_AL_.jpg",
              "rating": "7.4",
              "summary": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
          },
          {
              "id": 3,
              "name": "Harry Potter and the Prisoner of Azkaban",
              "link": "https://m.media-amazon.com/images/M/MV5BMTY4NTIwODg0N15BMl5BanBnXkFtZTcwOTc0MjEzMw@@._V1_UX182_CR0,0,182,268_AL_.jpg",
              "rating": "7.9",
              "summary": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        },
        {
              "id": 4,
              "name": "Charlie and the Chocolate Factory",
              "link": "https://m.media-amazon.com/images/M/MV5BNjcxMjg1Njg2NF5BMl5BanBnXkFtZTcwMjQ4NzMzMw@@._V1_UX182_CR0,0,182,268_AL_.jpg",
              "rating": "6.6",
              "summary": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        },
        {
              "id": 5,
              "name": "Harry Potter and the Deathly Hallows: Part 2 ",
              "link": "https://m.media-amazon.com/images/M/MV5BMGVmMWNiMDktYjQ0Mi00MWIxLTk0N2UtN2ZlYTdkN2IzNDNlXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_UX182_CR0,0,182,268_AL_.jpg",
              "rating": "8.1",
              "summary": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        },
        {
              "id": 6,
              "name": "Fantastic Beasts and Where to Find Them",
              "link": "https://m.media-amazon.com/images/M/MV5BMjMxOTM1OTI4MV5BMl5BanBnXkFtZTgwODE5OTYxMDI@._V1_UX182_CR0,0,182,268_AL_.jpg",
              "rating": "7.3",
              "summary": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        },
    ],
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

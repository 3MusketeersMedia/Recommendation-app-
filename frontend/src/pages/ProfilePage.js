import React from 'react'; 
import { Container, Row, Col } from 'react-bootstrap';
import {AppContext} from '../AppContext';
import MyNav from '../components/navbar';
import Footer from '../components/Footer';
import ProfilePic from '../components/ProfilePicture'
import ProfilePicChanger from '../components/ProfilePicChanger';
import ExamplePic from '../pics/niko_icon.png';
import MoviePic from '../components/moviePic';
import MediaModal from '../components/MediaModal';
import Header from '../components/header'

export default class ProfilePage extends React.Component { 
    static contextType = AppContext;
    constructor() { 
        super();
        const favoritedMovieList = JSON.parse(localStorage.getItem('movie-favorites'));
        const watchedMovieList = JSON.parse(localStorage.getItem('movie-watched'));
        let user =  sessionStorage.getItem('username');
        this.state = {
            isMainProf: true,
            userName: user, 
            favoritedMovies : favoritedMovieList,
            watchedMovies : watchedMovieList,
        };
        console.log(this.state.userName);
    }   


    render() { 
        let page;
        let favorites = 
        (<div className="align-middle">
            {this.state.favoritedMovies.map((movie, index) => 
            <div key={movie.id} className="d-inline-flex">
                <MoviePic movie={movie} />
            </div>)}
        </div>); 

        let watched = 
        (<div className="align-middle">
            {this.state.watchedMovies.map((movie, index) => 
            <div key={movie.id} className="d-inline-flex">
                <MoviePic movie={movie} />
            </div>)}
        </div>);

        if(this.state.isMainProf){
            /* Profile background */
            page = (  
                <>
                <div className="m-5 p-3">
                    <Header title="Movies"/>
                    <hr/>
                <Container fluid="md" className='p-3 d-flex' > 
                <Row> 
                    {/* Media lists  */}
                    <Col>
                    <MediaModal image="https://d279m997dpfwgl.cloudfront.net/wp/2020/12/GettyImages-1150049038-1000x630.jpg" 
                        title="WatchList"
                        list={watched}/>
                    </Col>
                    {/* Liked Components */}
                    <Col>
                    <MediaModal image="https://www.twosisterscrafting.com/wp-content/uploads/2016/01/how-to-make-the-perfect-popcorn-pinnable5-720x540.jpg" 
                        title="LikedList"
                        list={favorites}/>
                        {/* <MovieList movies={this.state.favoritedMovies} /> */}
                    </Col>
                    {/* News Feeds */}
                    <Col>                    
                    <MediaModal image="https://www.vshsolutions.com/wp-content/uploads/2020/02/recommender-system-for-movie-recommendation.jpg" 
                        title="Recommendations"
                        list="some content"/></Col>
                </Row>
                </Container>
                </div>
                </>);
        } else { 
            page = (<h2>A table of movies </h2>);
        }

        let user = this.state.userName;

        return (
        <AppContext.Consumer>
        {context => <>
            <MyNav/>
            <div className='text-center align-items-center justify-content-center p-2 m-5'>
                <ProfilePic /> {/*picture={ExamplePic}*/}
                <ProfilePicChanger/>
                <h3 className='p-2 m-3'>Hello {`${user}`}</h3>
            </div>
            {page}
            <Footer/>
            </> }
        </AppContext.Consumer>
        )

    }
}
import React from 'react'; 
import { Container, Row, Col } from 'react-bootstrap';
import MyNav from '../components/navbar';
import Footer from '../components/Footer';
import ProfilePic from '../components/ProfilePicture'
import ProfilePicChanger from '../components/ProfilePicChanger';
import ExamplePic from '../pics/niko_icon.png';
import MoviePic from '../components/moviePic';
import MediaModal from '../components/MediaModal';
import Header from '../components/header'

export default class ProfilePage extends React.Component { 
    constructor() { 
        super();
        const favoritedMovieList = JSON.parse(localStorage.getItem('movie-favorites'));
        this.state = {
            isMainProf: true,
            favoritedMovies : favoritedMovieList,
        };
        console.log(this.state.favoritedMovies);
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
                        list="some content"/>
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

        return <>
            <MyNav/>
            <div className='text-center align-items-center justify-content-center p-2 m-5'>
                <ProfilePic picture={ExamplePic}/>
                <ProfilePicChanger/>
            </div>
            {page}
            <div>
                {/* <img src="https://www.awakenthegreatnesswithin.com/wp-content/uploads/2018/08/Nature-Quotes-1.jpg"/> */}
                <div className="overlay">
                    <img className="blurThis" src="https://www.awakenthegreatnesswithin.com/wp-content/uploads/2018/08/Nature-Quotes-1.jpg"/>
                </div>
            </div>
            <Footer/>
        </> 
    }
}
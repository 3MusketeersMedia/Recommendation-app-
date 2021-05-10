import React from 'react'; 
import { Container, Row, Col } from 'react-bootstrap';
import MyNav from '../components/navbar';
import Footer from '../components/Footer'
import ProfilePic from '../components/ProfilePicture'
import ProfilePicChanger from '../components/ProfilePicChanger';
import ExamplePic from '../pics/niko_icon.png'
import MovieList from '../components/similarMovies'

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
        
        if(this.state.isMainProf){
            /* Profile background */
            page = (  
                <Row> 
                    {/* Media lists  */}
                    <Col></Col>
                    {/* Liked Components */}
                    <Col>
                        <MovieList movies={this.state.favoritedMovies} />
                    </Col>
                    {/* News Feeds */}
                    <Col></Col>
                </Row>);
        } else { 
            page = (<h2>A table of movies </h2>);
        }

        return <>
            <MyNav/>
            <div className='text-center align-items-center justify-content-center p-2 m-5'>
                <ProfilePic picture={ExamplePic}/>
                <ProfilePicChanger/>
            </div>
            <Container fluid="md" className='p-3'> 
                {page}
            </Container>
            <Footer/>
        </> 
    }
}
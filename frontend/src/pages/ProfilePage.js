import React from 'react'; 
import { Container, Row, Col } from 'react-bootstrap';
import {UserPreferenceContext} from '../UserPreferenceContext';
import MyNav from '../components/navbar';
import Footer from '../components/Footer'
import ProfilePic from '../components/ProfilePicture'
import ProfilePicChanger from '../components/ProfilePicChanger';
import ExamplePic from '../pics/niko_icon.png'
import MovieList from '../components/similarMovies'

export default class ProfilePage extends React.Component { 
    constructor() { 
        super();
        const favoriteList = JSON.parse(localStorage.getItem('react-movie-app-favorites'));
        console.log (favoriteList)
        this.state = {
            isMainProf: true,
            favorites: favoriteList
        };
    }   


    saveToLocalStorage = (item) =>{ 
        localStorage.setItem('react-movie-app-favorites', JSON.stringify(item))
    }

    addFavoriteMovie = (movie) =>{ 
        console.log("Hello");
        const newFavouriteList =  {... this.state.favorites, movie}; 
        this.setState({favorites: newFavouriteList}); 
        this.saveToLocalStorage(newFavouriteList);
    }

    render() { 
        let page;
        
        if(this.state.isMainProf){
            page = (
                /* Profile background */
                <Row> 
                    /* Media lists */
                    <Col></Col>
                    /* Liked Components */
                    <Col>
                        <MovieList movies={this.state.favorites} />
                    </Col>
                    /* News Feeds */
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
            <Container fluid="md" classname='p-3'> 
                {page}
            </Container>
            <Footer/>
        </> 
    }
}
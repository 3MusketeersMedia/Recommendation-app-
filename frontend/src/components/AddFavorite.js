import React, { useState, useContext } from 'react';
import {ToggleButton, ToggleButtonGroup} from 'react-bootstrap/';
import { useHistory } from 'react-router-dom';
import {AppContext} from '../AppContext'; 

const AddFavorite = ({isHover, movie, isFavorited, isWatched}) => {
    const {store, actions} = useContext(AppContext);
    const [favorited, setFavorited] = useState(isFavorited);
    const [watched, setWatched] = useState(isWatched);
    let history = useHistory(); 

    let goldStar = (
    <div onClick={() => {removeFavoriteMovie(movie)}}>
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" 
    fill="Gold" className="bi bi-star-fill" viewBox="0 0 16 16">
        <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
    </svg></div>);

    let whiteStar = ( 
    <div onClick ={() => {addFavoriteMovie(movie)}}>                 
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" 
        fill="White" className="bi bi-star" viewBox="0 0 16 16">
        <path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"/>
    </svg></div>);

    let emptyEye = (
    <div onClick ={() => {addWatchedMovie(movie)}}>
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-eye" viewBox="0 0 16 16">
        <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
        <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>
        </svg>
    </div>
    );

    let filledEye = (
        <div onClick ={() => {removeWatchedMovie(movie)}}>
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="gold" className="bi bi-eye-fill" viewBox="0 0 16 16">
        <path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0z"/>
        <path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8zm8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z"/>
        </svg>
        </div>
    );

    let watchButton = (
    <ToggleButtonGroup type="radio" name="preference" size="sm" className="float-right">
        <ToggleButton variant="dark" className="btn btn-secondary m-auto">
            {favorited ? goldStar : whiteStar}
        </ToggleButton>
        <ToggleButton variant="dark" className="btn btn-secondary m-auto">
            {watched ? filledEye : emptyEye}
        </ToggleButton>
    </ToggleButtonGroup>
    );


    const addFavoriteMovie = async (movie) =>{ 
        /**Redirect user to login  if they have not logged in*/
        if(!actions.checkedLogin()){
            history.push("/login");
        }

        if (actions.setMovieFavorite(movie)){
            setFavorited(true);
        } else {
            console.log("Can't add to favorited");
        }
    }; 

    const removeFavoriteMovie = async (movie) =>{
        if (actions.removeMovieFavorite(movie)){
            setFavorited(false);
        } else {
            console.log("Can't add to favorited");
        }
    }

    const addWatchedMovie = async (movie) =>{ 
        /**Redirect user to login  if they have not logged in*/
        if(!actions.checkedLogin()){
            history.push("/login");
        }

        if (actions.setMovieWatched(movie)){
            setWatched(true);
        } else {
            console.log("Can't add to favorited");
        }
    }; 

    const removeWatchedMovie = async (movie) =>{
        if (actions.removeMovieWatched(movie)){
            setWatched(false);
        } else {
            console.log("Can't add to favorited");
        }
    }
    
    return ( 
        <div>
            {/* <h5 className='mr-2 text-light float-left'>Add to Preferences</h5> */}
            {watchButton}
        </div>
    )
}

export default AddFavorite

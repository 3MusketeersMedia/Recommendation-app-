import React from 'react';
import AddFavorite from './AddFavorite'

//Compoment takes in the image of the movie, the title and the link to where
// the image is stored. 
const moviePic = ({movie}) => {
    let list = localStorage.getItem('react-movie-app-favorites');
    let favorites = [];
    if(list)
        favorites = JSON.parse(list);
    return (
        <div className='MovieFrame d-flex justify-content-start m-3'>            
            <img src={movie.link} alt={movie.name + " picture"}></img>
            <div className="overlay d-flex align-items-center justify-content-center">
                <AddFavorite movie={movie} 
                isFavorited={favorites.find((ele) => movie.name === ele.name) ? true : false}/>
            </div>
        </div>
    )
}

moviePic.defaultProps = {
    text: "A movie picture"
}

export default moviePic

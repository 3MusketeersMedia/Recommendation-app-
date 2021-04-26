import React from 'react';
import AddFavorite from './AddFavorite'

//Compoment takes in the image of the movie, the title and the link to where
// the image is stored. 
const moviePic = ({movie}) => {
    console.log(movie)
    console.log(movie.title)
    return (
        <div className='MovieFrame d-flex justify-content-start m-3'>            
            <img src={movie.picture} alt={movie.title + " picture"}></img>
            <div className="overlay d-flex align-items-center justify-content-center">
                <AddFavorite isHover={false}/>
            </div>
        </div>
    )
}

moviePic.defaultProps = {
    text: "A movie picture"
}

export default moviePic

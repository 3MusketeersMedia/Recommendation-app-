import React from 'react'

import '../pages/zoomedpage'
import MoviePic from '../components/moviePic'

const similarMovies = (props) => {
    return (
        <>
        <div className='container-fluid Media-app p-2 '> 
            <div className='row'>
                <div className='d-flex justify-content-start m-3'>
                {props.movies.map((movie, index) => <div key={movie.id}>
                    <MoviePic movie={movie} />
                </div>)} 
      </div></div></div>
      </>
    )
}

export default similarMovies

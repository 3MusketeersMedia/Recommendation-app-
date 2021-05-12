import React from 'react'

import '../pages/zoomedpage'
import MoviePic from '../components/moviePic'

const similarMovies = (props) => {
    return (
        <>
        <div className='container-fluid Media-app p-2 ml-5 d-flex justify-content-center '> 
            <div className='row'>
                <div className='d-inline-flex'>
                {props.movies.map((movie, index) => <div key={movie.id}>
                    <div className="ml-2">
                    <MoviePic movie={movie} />
                    </div>
                </div>)} 
      </div></div></div>
      </>
    )
}

export default similarMovies

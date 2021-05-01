import React from 'react'
import Table from 'react-bootstrap/Table'
import Carousel from 'react-bootstrap/Carousel'
import '../pages/zoomedpage'
import MoviePic from '../components/moviePic'

const similarMovies = (props) => {
    console.log(props.movies)
    return (
        <>
        <div className='container-fluid Media-app p-2 '> 
            <div className='row'>
                <div className='d-flex justify-content-start m-3'>
                {props.movies.map((movie, index) => <div>
                    <MoviePic movie={movie} />
                </div>)} 
      </div></div></div>
      </>
    )
}

export default similarMovies

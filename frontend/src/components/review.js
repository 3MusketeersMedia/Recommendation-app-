const review = ({movie}) => {
    return (
        <div>
            <header>Rating from IMDB:</header>
            <h1>{movie.Rating}/10</h1>
        </div>
    )
}

export default review

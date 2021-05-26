const review = ({movie}) => {
    return (
        <div>
            <header>Rating:</header>
            <h1>{movie.rating}/10</h1>
        </div>
    )
}

export default review

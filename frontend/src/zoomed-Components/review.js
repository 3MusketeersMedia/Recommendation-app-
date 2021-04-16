const review = ({movie}) => {
    return (
        <div>
            <header>Rating from IMDB:</header>
            <h1>{movie[0].Rating}</h1>
        </div>
    )
}

export default review

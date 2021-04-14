
//Compoment takes in the image of the movie, the title and the link to where
// the image is stored. 
const moviePic = ({movie}) => {
    return (
        <div>
            <img src={movie[0].picture} alt={movie[0].title + " picture"}/>
        </div>
    )
}

moviePic.defaultProps = {
    text: "A movie picture"
}

export default moviePic

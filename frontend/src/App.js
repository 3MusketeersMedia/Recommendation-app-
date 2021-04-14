import './App.css';
import {useState, useEffect} from 'react'; 
import Movies from "./zoomed-Components/moviePic"
import Header from "./zoomed-Components/header"
import Summary from "./zoomed-Components/summary"
import SimilarMovies from "./zoomed-Components/similarMovies"
import Rating from "./zoomed-Components/review"

function App() {
  const database_address = "http://localhost:4000/movies"; 
  const [showMovie, setMovie] = useState ([{"id": 0,
  "title": "",
  "picture": "",
  "Rating": "",
  "text": "" }]);
  const [simShowMovies, setSimMovies] = useState ([{"id": 0,
  "title": "",
  "picture": "",
  "Rating": "",
  "text": "" }]);
  

  //Updates movies on effect
  useEffect(() => {
    const id = Math.floor(Math.random() * 20) + 1
    const getMovies = async () => {
      const movieFromServer = await fetchMovies(id) 
      setMovie(movieFromServer)
    }
    getMovies(); 
    getSimMovies(id)
  }, [])

    //Fetches similar movies from database
    const getSimMovies = async (id) => {
      await setSimMovies(0)
      //Substitute with backend call for similar movies. 
      const movies = 9; // Show 3 recommended movies
      let temp_id = id; 
      for (let i = 0; i < movies; i++) { 
        temp_id = ((++temp_id) % 20) + 1 
        const movieFromServer = await fetchMovies(temp_id); 
        console.log(movieFromServer[0])
        await setSimMovies([...simShowMovies, movieFromServer[0]])
      }
      console.log(simShowMovies)
    }

    //Fetches individual movie from database
    const fetchMovies = async (id) => {
      const response = await fetch(database_address + `?id=${id}`)
      const data = await response.json()
  
      return data
    }


    return(
  <div className="zoom-container">
    <div className="titleNav">
      . 
    </div>
    <div className="MoviePic">
      <Movies movie={showMovie}/>
    </div>
    <div className="SimilarMovies">
      <SimilarMovies />
    </div>
    <div className="MovieTitle">
      <Header movie={showMovie}/>
    </div>
    <div className="Ratings">
      <Rating movie={showMovie} />
    </div>
    <div className="Summary">
      <Summary movie={showMovie}/>
    </div>
    
  </div>
  );
}

export default App;

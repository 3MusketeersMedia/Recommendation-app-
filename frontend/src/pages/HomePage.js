//import Header from "./components/header"
//import navbar from "./components/navbar";
import { buildQueries } from '@testing-library/dom';
import MyNav from '../components/navbar';
import HpHeader from '../components/homepageHeader';
import { Link, Router } from 'react-router-dom';
import MovieList from './MovieList'



export default function HomePage() {
  return (
    <div>
      <div>
        <MyNav />
      </div>

      <div>
        <HpHeader />
      </div>

      <div>
        <MovieList />
      </div>

    </div>
  );
}
//import Header from "./components/header"
//import navbar from "./components/navbar";
import { buildQueries } from '@testing-library/dom';
import MyNav from '../components/navbar'
import './homePage.css';
import { Link } from 'react-router-dom';

export default function HomePage() {
  return (
    <div>
      <div>
        <MyNav />
      </div>

      <div className = "mainBody">
        <div className = "containerPic">
          <h1>
            Place Holder, will put an image/logo
          </h1>
        </div>

        <div className = "containerText">
          <div className = "textWrapper">
            <h1 className = "headline">
            Tired of garbage media recommendations?
            </h1>
            <h3 className = "description">
            Get started with RecomMedia today, and gain access to personalized
            recommendation lists based the things you love.
            </h3>
          </div>
          
          <Link to="/login" className = "btn">Sign Up/Log In</Link>
        </div>
      </div>
    </div>
  );
}
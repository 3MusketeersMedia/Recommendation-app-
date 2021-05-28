import React, { useState, useContext} from 'react';
import 'antd/dist/antd.css' 
import '../pages/profilePage.css'
import {AppContext} from '../AppContext';

const RecomClicker = (props) => {
  const context = useContext(AppContext);
  async function callRec()
  {
      context.actions.getUserRecs();
  }
  return (
    <>
      <div className="d-inline-block border border-secondary rounded-top MediaModalImage" style={{height: "100%"}} onClick={() => callRec()}>
        <img src={props.image} alt="Media Card image"
        className="img-responsive img-thumbnail rounded mx-auto" alt="Responsive image"/>
        <p className="text-justify text-center font-weight-bold p-3 mb-2 bg-light text-dark">{props.title}</p>
      </div>
    </>
  );
};

export default RecomClicker
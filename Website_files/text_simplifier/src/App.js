import logo from './logo.svg';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import './App.css';
import React, { useState } from 'react';
import axios from 'axios';
import HomePage from './HomePage';
import Team from './Team';
import AboutProj from './AboutProj';


function App() {
  return (<>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />}/>
        <Route path="/team" element={<Team/>}/>
        <Route path="/aboutProject" element={<AboutProj />}/>
          
      </Routes>
    </BrowserRouter></>);
}

export default App;

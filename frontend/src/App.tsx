import React from 'react';
// import logo from './logo.svg';
// import './App.css';
import HeaderComponent from "./components/headerComponent/HeaderComponent";
import BodyComponent from "./components/bodyComponent/BodyComponent";

const App = () => {
    return (
        <div className="App">
            <HeaderComponent/>
            <BodyComponent/>
        </div>
    );
}

export default App;

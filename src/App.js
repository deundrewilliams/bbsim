import './App.css';
import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';


import WelcomePage from './pages/WelcomePage';
import HomePage from './pages/HomePage';
import GamePage from './pages/GamePage';
import CreateGamePage from './pages/CreateGamePage';


function App() {
    return(
        <Router>
            <div className="App">
                <Switch>
                    <Route path="/" component={WelcomePage} exact />
                    <Route path="/home" component={HomePage} />
                    <Route path="/game" component={GamePage} />
                    <Route path="/create-game" component={CreateGamePage} />
                </Switch>
            </div>
        </Router>
    )
}

export default App;

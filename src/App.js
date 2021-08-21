import './App.css';
import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import PrivateRoute from './components/PrivateRoute';
import PublicRoute from './components/PublicRoute';

import WelcomePage from './pages/WelcomePage';
import HomePage from './pages/HomePage';
import GamePage from './pages/GamePage';
import CreateGamePage from './pages/CreateGamePage';


function App() {
    return(
        <Router>
            <div className="App">
                <Switch>
                    <PublicRoute restricted={true} path="/" component={WelcomePage} exact />
                    <PrivateRoute path="/home" component={HomePage} />
                    <PrivateRoute path="/game" component={GamePage} />
                    <PrivateRoute path="/create-game" component={CreateGamePage} />
                </Switch>
            </div>
        </Router>
    )
}

export default App;

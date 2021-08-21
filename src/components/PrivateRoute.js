import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import { isLoggedIn } from '../utils';

const PrivateRoute = ({ component: Component, ...rest }) => {

    return (
        // If user is not logged in, redirect to login page
        <Route {...rest} render={props => (isLoggedIn() ?
            <Component {...props}/> :
            <Redirect to="/" />
        )}/>
    );

};

export default PrivateRoute;

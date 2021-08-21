import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import { isLoggedIn } from '../utils';

const PublicRoute = ({ component: Component, restricted, ...rest }) => {

    return (
        // If user is logged in, and component is restricted, redirect to home
        <Route {...rest} render={props => (isLoggedIn() && restricted ?
            <Redirect to="/home" /> :
            <Component {...props} />
        )}/>
    );

};

export default PublicRoute;

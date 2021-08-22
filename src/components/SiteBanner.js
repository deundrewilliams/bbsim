import '../css/SiteBanner.css';

import { logout } from '../utils';

import axios from 'axios';

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
       var c = ca[i];
       while (c.charAt(0) ===' ') c = c.substring(1);
       if(c.indexOf(name) === 0)
          return c.substring(name.length,c.length);
    }
    return "";
}

const options = {
    headers: {"X-CSRFToken": getCookie('csrftoken')}
}

const SiteBanner = (props) => {

    const { buttonText, buttonAction } = props;

    const handleLogout = async () => {

        await axios.post('/api/logout', {}, options)
        .then(res => res.data)
        .catch(err => err.response.data)
        .then(data => {
            if (data.success) {
                logout();
                window.location.href = '/';
            }
        });

    }


    return(
        <div className="site-banner">
            <button id="log-out" onClick={handleLogout}>Log Out</button>
            <h1>BIG BROTHER SIM</h1>
            {buttonText ? <button id="side-button" onClick={buttonAction}>{buttonText}</button> : null}
        </div>
    )
}

export default SiteBanner;

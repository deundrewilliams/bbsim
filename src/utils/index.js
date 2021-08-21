const TOKEN_KEY = 'bbsim';

export const login = () => {
    localStorage.setItem(TOKEN_KEY, true);
}

export const logout = () => {
    localStorage.removeItem(TOKEN_KEY);
}

export const isLoggedIn = () => {
    if (localStorage.getItem(TOKEN_KEY)) {
        return true;
    }
    return false;
}

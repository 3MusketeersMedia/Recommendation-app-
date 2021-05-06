import React from 'react';

//Stores User preferences
/** May potentially be modified to store all user data */
export const UserPreferenceContext = React.createContext({
    favorites: [],
});
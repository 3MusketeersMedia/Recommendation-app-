import React, { useState, useEffect } from "react";
import { useHistory } from "react-router-dom";

export const AppContext = React.createContext();

/** App Context Template taken from WebApp boilerplate with React JS
 *  Read more here to learn how the template can be applied https://github.com/4GeeksAcademy/react-hello-webapp/tree/master/src/js/store
 *
 *  ContextWrapper provides global variables and methods in a single Context. It does so by intializing a state (getState) where you can inject
 *  and intialize different sets of context into a single state (see below) and provides certain functions to get and update them.
 *  It then wraps the context in APP.js by taking all the child components in APP.js passed as {children} and passing it as subscribers of
 *  Appcontext (the context we are using).
 *
 *  Use Cases:
 *
 *   -> Classes: simply import AppContext to componenets and set ContextType to it.
 *              -> To access variables use this this.context.store.<varType>
 *              -> To access action use this this.context.action.<actionType>
 *
 *   -> Hooks: Use import Appcontext from Appcontext; ... const {store, actions} = useContext(AppContext);
 *              -> To access variables or actions, simply append the type you want. (i.e. action.setMovies(), store.token)
 *
 * It's preferred to use this Context when setting global variables and fetching from back end. Data shared here will be available to any
 * Components inside App.js
*/
const ContextWrapper = ({children}) => {
    const [state, setState] = useState(
        GetState({
            getStore: () => state.store,
            getActions: () => state.actions,
            setStore: updatedStore =>
                setState({
                    store: Object.assign(state.store, updatedStore),
                    actions: { ...state.actions }
                })
        })
    );

    useEffect(() => {
        /**
         * EDIT THIS!
         * This function is the equivalent to "window.onLoad", it only runs once on the entire application lifetime
         * you should do your ajax requests or fetch api requests here. Do not use setState() to save data in the
         * store, instead use actions, like this:
         **/

        // eslint-disable-next-line react-hooks/exhaustive-deps
        state.actions.syncToken();
        if(state.actions.checkedLogin()){
            state.actions.getMovieFavorites();
            state.actions.getmovieWatched();
            state.actions.getUserName();
        }
    },[state.store.token]);

    // The initial value for the context is not null anymore, but the current state of this component,
    // the context will now have a getStore, getActions and setStore functions available, because they were declared
    // on the state of this component
    return (
        <AppContext.Provider value={state}>
            {children}
        </AppContext.Provider>
    );
};

export default ContextWrapper;


/** getState - Stores the global variables and methods in a single Context. You can also use the props in
 *             other to access other states in the Context:
 *           -> getStore(): gets the current value of store in the context.
 *           -> get Actions: Calls an action in the current context
 *           -> setStore(): Updates the store in the variable
 *
 * @returns States that will be used to create a context in ContextWrapper (see above)
*/
const GetState = ({ getStore, getActions, setStore }) => {
    let history = useHistory();
	return {
		store: {
			movie: null,
			token: null,
            loginModalShown: false,
            movieFavorites: [],
            movieWatched: [],
            searchContents: null,
            advSearchContents: null,
            address: "https://recommedia-api.herokuapp.com/" //"http://localhost:5000/"
		},
		actions: {
            /** */
            syncToken: async () => {
                const token = await sessionStorage.getItem("token");
                if(token && token !=="" && token!==undefined)
                    setStore({token: token});
            },

            /** Checks if user is logged in */
            checkedLogin: () => {
                const store = getStore();
                if (store.token && store.token !== "" && store.token !== 'undefined'){
                    return true;
                }
                return false;
            },

            loadMovies: async (limit, offset) => {
              console.log('load movies');
              if (getStore().searchContents !== null) {
                console.log('normal search');
                const response = await fetch(getStore().address + 'search', {
                  method: 'POST',
                  headers: {
                    'content-type': 'application/json',
                  },
                  body: JSON.stringify({searchContents: getStore().searchContents, limit, offset}),
                });
                const data = await response.json();
                console.log(data);
                return data;
              } else if (getStore().advSearchContents !== null) {
                console.log('advanced search');
                const {name, mediaType,genre, minYear, minRate, maxYear, maxRate} = getStore().advSearchContents;
                const response = await fetch(getStore().address + 'advSearch', {
                  method: 'POST',
                  headers: {
                    'content-type': 'application/json',
                  },
                  body: JSON.stringify({name, mediaType,genre, minYear, minRate, maxYear, maxRate, limit, offset}),
                });
                const data = await response.json();
                console.log(data);
                return data;
              } else {
                console.log('list')
                const response = await fetch(getStore().address + `pages?limit=${limit}&offset=${offset}`);
                const data = await response.json();
                console.log(data);
                return data;
              }
            },

            openLoginModal: () => {
              setStore({loginModalShown: true});
            },

            closeLoginModal: () => {
              setStore({loginModalShown: false});
            },

            /** Calls normal search, gets the data, and then loads up movie list*/
            search: async (searchContents) => {
                console.log('search');
                await setStore({searchContents: searchContents, advSearchContents: null});
                history.push("/");
                history.push("/list");
            },

            /** Calls normal search, gets the data, and then loads up movie list*/
            advancedSearch: async (name, mediaType, genre, minYear, minRate, maxYear, maxRate) => {
                const advSearchContents = {name, mediaType, genre, minYear, minRate, maxYear, maxRate};
                console.log('advanced search');
                await setStore({advSearchContents, searchContents: null});
                // Now that the search is conducted, should load up list page,
                // which will check that the searchList is not NULL and load up
                // the results of the search rather than the default movie list
                history.push("/");
                history.push("/list");
            },

            /** Resets the list of the search results so that the default movies are loaded into list next time */
            resetSearchList: async() => {
                setStore({searchContents: null, advSearchContents: null});
            },

            /**Login checks new  and returns token
             * @return Currently returns  TRUE/FALSE whether methods is successful
             * ---> May need to change return type for rendering conditions in
             *      login Component
            */
            login: async (username, password) => {

                const args = ({
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({username, password}),
                });

                try{
                    const response = await fetch(getStore().address + 'login',args);
                    const data = await response.json();
                    console.log(data);

                    if(response.status !== 200){
                        console.log("Status Code: " + response.status);
                        return false;
                    }

                    sessionStorage.setItem("token", data.token);
                    setStore({token: data.token})
                    return true;
                }
                catch(error){
                    console.log("Login connection dropped");
                }
            },


            /** Simply removes token from sessionStorage*/
            logout: async () => {
                const token = sessionStorage.removeItem("token");
                setStore({token: null});
                history.push("/");
            },


            /**Signup takes a new set of user/pass and stores the new token
             * @return Currently returns  TRUE/FALSE whether methods is successful
             * ---> May need to change for some sort of email validation check.
             *      to prevent botting.
             * ---> May need to change return type for rendering conditions in
             *      login Component
            */
            signup: async (username, password) => {

                const args = ({
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({username, password}),
                });

                try{
                    const response = await fetch(getStore().address + 'signup', args)
                    const data = await response.json();
                    console.log(data);

                    if(response.status !== 200){
                        console.log("Status Code: " + response.status);
                        return false;
                    }

                    sessionStorage.setItem("token", data.token);
                    setStore({token: data.token})
                    return true;
                }
                catch(error){
                    console.log("Signup connection dropped");
                }
            },

            getUserName: async() => {
                const store = getStore();
                await getActions().syncToken();

                const opts = {
                    method: "GET",
                    headers: {
                        Authorization: "Bearer " + store.token
                    },
                };
                try{
                    const response = await fetch(getStore().address + 'profile', opts);
                    const data = await response.json();
                    console.log(data);

                    if(response.status !== 200){
                        console.log("Status Code: " + response.status);
                        return false;
                    }

                    console.log(data.username);
                    sessionStorage.setItem("username", data.username);
                    return true;
                }
                catch(error){
                    console.log("Signup connection dropped");
                }
            },

            /** Changes the current movie in route /movies by modifying
             * "movie" in the store state and localstorage.
            */
            setMovie: async(movie) => {
                localStorage.setItem('movie', JSON.stringify(movie));
                await setStore({movie: movie});
                history.push("/movie");
            },

            /** Ensures that the local storage value of "movie" is
             *  loaded into store.movie.
             *  --> currently called by zoomed-page
            */
            syncMovies: async() =>{
                const movie = JSON.parse(localStorage.getItem('movie'));
                await setStore({movie: movie});
            },

            /** Gets favorited movies and stores in localstorage */
            getMovieFavorites: async() =>{
                const store = getStore();
                const opts = {
                    method: "GET",
                    headers: {
                        Authorization: "Bearer " + store.token
                    },
                };
                const response = await fetch(getStore().address + "favorite", opts);
                const data = await response.json();

                if(response.status !== 200){
                    console.log("Status Code: " + response.status);
                    return false
                }

                const favorites = JSON.stringify(data);
                console.log(favorites);
                localStorage.setItem('movie-favorites', favorites);
                setStore({movieFavorites: favorites})
            },

            setMovieFavorite: async(movie) =>{
                const store = getStore();
                const opts = {
                    method: "POST",
                    headers: {
                        Authorization: "Bearer " + store.token,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(movie),
                };
                const response = await fetch(getStore().address + "favorite", opts);

                if(response.status !== 200){
                    console.log("Status Code: " + response.status);
                    return false
                }

                const favorites = [...getStore().movieFavorites, movie];
                console.log(favorites);
                localStorage.setItem('movie-favorites', JSON.stringify(favorites));
                setStore({movieFavorites: favorites})
            },

            removeMovieFavorite: async(movie) => {
                const store = getStore();
                const opts = {
                    method: "DELETE",
                    headers: {
                        Authorization: "Bearer " + store.token,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(movie),
                };
                const response = await fetch(getStore().address + "favorite", opts);

                if(response.status !== 200){
                    console.log("Status Code: " + response.status);
                    return false
                }

                const favorites = getStore().movieFavorites.filter(item => item !== movie)
                localStorage.setItem('movie-favorites', JSON.stringify(favorites));
                setStore({movieFavorites: favorites})
            },

            /** Gets Watchedd movie and stores in localstorage */
            getmovieWatched: async() =>{
                const store = getStore();
                const opts = {
                    method: "GET",
                    headers: {
                        Authorization: "Bearer " + store.token
                    },
                };
                const response = await fetch(getStore().address + "watchlist", opts);
                const data = await response.json();

                if(response.status !== 200){
                    console.log("Status Code: " + response.status);
                    return false
                }

                const watched = JSON.stringify(data);
                console.log(watched);
                localStorage.setItem('movie-watched', watched);
                setStore({movieWatched: watched});
            },

            setMovieWatched: async(movie) =>{
                const store = getStore();
                const opts = {
                    method: "POST",
                    headers: {
                        Authorization: "Bearer " + store.token,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(movie),
                };
                const response = await fetch(getStore().address + "watchlist", opts);

                if(response.status !== 200){
                    console.log("Status Code: " + response.status);
                    return false
                }

                const watched = [...getStore().movieWatched, movie];
                console.log(watched);
                localStorage.setItem('movie-watched', JSON.stringify(watched));
                setStore({movieWatched: watched})
            },

            removeMovieWatched: async(movie) => {
                const store = getStore();
                const opts = {
                    method: "DELETE",
                    headers: {
                        Authorization: "Bearer " + store.token,
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(movie),
                };
                const response = await fetch(getStore().address + "watchlist", opts);

                if(response.status !== 200){
                    console.log("Status Code: " + response.status);
                    return false
                }

                const watched = getStore().movieWatched.filter(item => item !== movie)
                localStorage.setItem('movie-watched', JSON.stringify(watched));
                setStore({movieWatched: watched})
            },
		}
	};
};

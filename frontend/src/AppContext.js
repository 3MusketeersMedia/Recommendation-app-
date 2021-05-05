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
 *   -> Hooks: Use import Appcontext from Appcontext; ... const {state, actions} = useContext(AppContext);
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
		},
		actions: {
            /** */
            syncToken: async () => {
                const token = await sessionStorage.getItem("token");
                if(token && token !== "" && token !== undefined)
                    setStore({token: token});
            },

            /**Login checks new  and returns token
             * @return Currently returns  TRUE/FALSE whether methods is successful
             * ---> May need to change return type for rendering conditions in
             *      login Component
            */
            login: async (username, password) => {

                const args = {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({username, password}),
                };

                try{
                    const response = await fetch('http://localhost:5000/login',args);
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

                const args = {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({username, password}),
                };

                try{
                    const response = await fetch('http://localhost:5000/signup', args)
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

            /** Changes the current movie in route /movies by modifying
             * "movie" in the store state and localstorage.
            */
            setMovie: async(movie) => {
                localStorage.setItem('movie', JSON.stringify(movie));
                await setStore({movie: movie});
            },

            /** Ensures that the local storage value of "movie" is
             *  loaded into store.movie.
             *  --> currently called by zoomed-page
            */
            syncMovies: async() =>{
                const movie = JSON.parse(localStorage.getItem('movie'));
                await setStore({movie: movie});
                console.log("Hello");
            }
		}
	};
};

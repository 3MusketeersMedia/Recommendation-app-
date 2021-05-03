import React, { useState, useEffect } from "react";

export const AppContext = React.createContext();

// This function injects the global store to any view/component where you want to use it, we will inject the context to layout.js, you can see it here:
// https://github.com/4GeeksAcademy/react-hello-webapp/blob/master/src/js/layout.js#L35
const ContextWrapper = ({children}) => {
    //this will be passed as the contenxt value
    const [state, setState] = useState(
        getState({
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
    }, []);

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

const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			movie: null, 
			token: null,
		},
		actions: {
            syncToken: async () => {
                const token = await sessionStorage.getItem("token");
                if(token && token != "" && token != undefined) 
                    setStore({token: token});
            }, 

            login: async (username, password) => {
                console.log(username,  password)
                const args = ({
                    method: "POST", 
                    headers: {
                        "Content-Type": "application/json"
                    }, 
                    body: JSON.stringify({username, password}),
                });
                const response = await fetch('http://localhost:5000/login',args);
                const data = await response.json(); 
                try{
                    console.log(args) 
                    const response = await fetch('http://localhost:5000/login',args);
                    const data = await response.json(); 
                    console.log(data);
                    
                    if(response.status !== 200){
                        console.log("Invalid"); 
                        return false; 
                    } 
                    
                    sessionStorage.setItem("token", data.token);
                    setStore({token: data.token})
                    return true;
                }
                catch(error){
                    console.log("Invalid");
                }
            }, 


            logout: async () => {
                const token = sessionStorage.remove("token");
                setStore({token: null});
            }, 


            /**Signup takes a new set of user/pass and returns token 
             * ---> May need to change for some sort of email validation check.
             *      to prevent botting.  
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
                    const response = await fetch('http://localhost:5000/signup', {args})
                    const data = await response.json(); 
                    console.log(data);
                    
                    if(response.status !== 200){
                        console.log("Invalid"); 
                        return false; 
                    } 
                    
                    sessionStorage.setItem("token", data.token);
                    return true;
                }
                catch(error){
                    console.log(error);
                }
            }, 

            setMovie: async(movie) => {
                localStorage.setItem('movie', JSON.stringify(movie));
                await setStore({movie: movie});
            },

            syncMovies: async() =>{
                const movie = JSON.parse(localStorage.getItem('movie'));
                await setStore({movie: movie});
                console.log("Hello");
            }
		}
	};
};
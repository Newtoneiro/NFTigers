import { useState, createContext, useEffect, useContext, useCallback} from "react";
import {onAuthStateChanged, createUserWithEmailAndPassword, signOut, signInWithEmailAndPassword, signInWithPopup, FacebookAuthProvider, GoogleAuthProvider} from 'firebase/auth'
import {auth} from '../firebase-config'
import axios from 'axios'

export const AuthContext = createContext();

export function useAuth(){
    return useContext(AuthContext)
}

export const AuthProvider = ({children}) => {
    const [currentUser, setCurrentUser] = useState(null)
    const [wallet, setWallet] = useState(0)
    
    const [loading, setLoading] = useState(true)

    const authFetch = axios.create({
      withCredentials: true,
      baseURL: "/api",
    });

    async function signupCreateUserDB(email, usId, method) {
        const response = await authFetch.post('./users/', {email, usId, method})
        return response
    }
    
    function signup(email, password){
        try{
            const responseDB = createUserWithEmailAndPassword(auth, email, password).then((responseFirebase) => {
                return signupCreateUserDB(email, responseFirebase.user.uid, 'email')
            });
            
            return responseDB
        }
        catch(error) {
            console.error(error)
        }
    }

    function login(email, password){
        return signInWithEmailAndPassword(auth, email, password);
    }

    function signout(){
        return signOut(auth);
    }

    function signInWithFacebook(){
        const provider = new FacebookAuthProvider();
        try{
            const responseDB = signInWithPopup(auth, provider).then((responseFirebase) => {
                return signupCreateUserDB(responseFirebase.user.email, responseFirebase.user.uid, 'email')
            });
            
            return responseDB
        }
        catch(error) {
            console.error(error)
        }
    }

    function signInWithGoogle(){
        const provider = new GoogleAuthProvider();
        try{
            const responseDB = signInWithPopup(auth, provider).then((responseFirebase) => {
                return signupCreateUserDB(responseFirebase.user.email, responseFirebase.user.uid, 'email')
            });
            
            return responseDB
        }
        catch(error) {
            console.error(error)
        }
    }

    const getWallet = useCallback(async (usId) => {
        if (!usId){
            usId = currentUser.uid
        }
        if (currentUser){
            const response = await authFetch.post('./wallet/', {usId: usId});
            setWallet(response.data.wallet)
        }
    }, [authFetch, currentUser])

    const topUp = async (income) => {
        if (currentUser !== null && income > 0){
            const response = await authFetch.put('./wallet/', {usId: currentUser.uid, income});
            if (response.statusText === 'Accepted'){
                getWallet();
            }
        }
    }

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, user => {
            setLoading(true)
            setCurrentUser(user)
            setLoading(false)
        })
        
        return unsubscribe
    }, [])

    useEffect(() => {
        currentUser && getWallet(currentUser.uid)
    }, [currentUser, getWallet])

    return (
        <AuthContext.Provider
        value={{
            currentUser,
            signup,
            login,
            signout,
            signInWithFacebook,
            signInWithGoogle,
            authFetch,
            wallet,
            topUp,
            getWallet,
        }}>
            {!loading && children}
        </AuthContext.Provider>
    )
}

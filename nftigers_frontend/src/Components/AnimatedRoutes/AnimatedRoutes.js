import React from 'react'
import {Routes,
  Route,
  useLocation} from 'react-router-dom';

import SignUp from '../../Components/SignUp/SignUp';
import Login from '../../Components/Login/Login';
import Home from '../../Components/Home/Home';
import PrivateRoute from '../../Utils/PrivateRoute';

import {AnimatePresence} from 'framer-motion'
import { HomeProvider } from '../Home/HomeContext';


const AnimatedRoutes = () => {
  const location = useLocation();

  return (
    <AnimatePresence>
        <Routes location={location} key={location.pathname}>
          <Route exact path="/" element={
            <PrivateRoute>
              <HomeProvider>
                <Home/>
              </HomeProvider>
            </PrivateRoute>
          }
          />
          <Route exact path="/login" element={<Login/>} />
          <Route exact path="/signup" element={<SignUp/>} />
          <Route path='*' element={<h1>404</h1>}/>
        </Routes>
    </AnimatePresence>
  )
}

export default AnimatedRoutes

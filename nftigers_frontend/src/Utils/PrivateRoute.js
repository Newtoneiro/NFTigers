import React from 'react'
import { useAuth } from './Auth'
import { Navigate } from 'react-router-dom'

const PrivateRoute = ({children}) => {
  const { currentUser } = useAuth()
 
  return currentUser ? children : <Navigate to="/login" replace></Navigate>

}

export default PrivateRoute

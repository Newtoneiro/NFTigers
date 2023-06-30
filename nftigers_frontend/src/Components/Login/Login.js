import React from 'react'
import { useAuth } from '../../Utils/Auth'
import CustomForm from '../../Utils/FormUtil/CustomForm';
import { Navigate } from 'react-router-dom';

import {BiEnvelope, BiLockAlt} from 'react-icons/bi'

import {motion} from 'framer-motion'

import './login.css'

const Login = () => {
  const providedFields = [
    {
      name: "email",
      type: "text",
      placeholder: "Email",
      icon: <BiEnvelope/>
    },
    {
      name: "password",
      type: "password",
      placeholder: "Password",
      icon: <BiLockAlt/>
    }
  ]
  const formConfig = {
    title: "Log in",
    subtitle: "Please log in to use platform",
    redirectMessage: "Don't have an account yet?",
    redirectText: "Sign up",
    redirectTO: "/signup"
  }

  const { currentUser, login } = useAuth()

  const handleSubmit = async (fields) => {
    return login(fields.email, fields.password);
  }

  return <motion.div className='login'
      initial={{opacity: 0}}
      animate={{opacity: 1}}
      exit={{opacity: 0}}
    >
    {currentUser? <Navigate to="/" replace></Navigate>:
    <CustomForm props={{providedFields, formConfig, handleSubmit}}/>}
  </motion.div>

}

export default Login

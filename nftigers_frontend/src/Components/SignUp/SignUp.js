import React from 'react'
import { useAuth } from '../../Utils/Auth'
import CustomForm from '../../Utils/FormUtil/CustomForm';
import { Navigate } from 'react-router-dom';

import {BiEnvelope, BiLockAlt} from 'react-icons/bi'

import { motion } from 'framer-motion';

import './signup.css'

const SignUp = () => {
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
    },
    {
      name: "confirmPassword",
      type: "password",
      placeholder: "Confirm password",
      icon: <BiLockAlt/>
    }
  ]
  const formConfig = {
    title: "Sign up",
    subtitle: "Please sign up to use platform",
    redirectMessage: "Already have an account?",
    redirectText: "Log in",
    redirectTO: "/login"
  }

  const { currentUser, signup } = useAuth()

  const handleSubmit = async (fields) => {
    if (fields.password !== fields.confirmPassword){
      const error = {code: "passwords_dont_match"}
      throw error
    }
    return signup(fields.email, fields.password);
  }

    return <motion.div className='signup'
        initial={{opacity: 0}}
        animate={{opacity: 1}}
        exit={{opacity: 0}}
      >
      {currentUser? <Navigate to="/" replace></Navigate>:
      <CustomForm props={{providedFields, formConfig, handleSubmit}}/>}
    </motion.div>
}

export default SignUp

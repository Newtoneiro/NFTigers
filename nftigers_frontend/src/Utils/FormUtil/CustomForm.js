import React, {useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom';

import './customForm.css'
import tigerLogo from '../../resources/tiger.png'
import { useAuth } from '../Auth';

import {BsFacebook, BsGoogle} from 'react-icons/bs'

const CustomForm = ({props}) => {
  const {providedFields, formConfig, handleSubmit} = props;

  const [fields, setFields] = useState({})
  const [loadingFields, setLoadingFields] = useState(true)
  
  const [errorMsg, setErrorMsg] = useState("")
  const [loading, setLoading] = useState(false)

  const navigate = useNavigate();

  const {signInWithFacebook, signInWithGoogle} = useAuth();

  useEffect(() => {
    let newFields = {}
    providedFields.forEach(field => {
      newFields[field.name] = "";
    })

    setFields(newFields)
    setLoadingFields(false)
  }, [providedFields])

  const updateField = (field, value) => {
    var newFields = fields;
    newFields[field] = value;
    setFields(newFields)
  }

  const submitFunction = async (e) => {
    e.preventDefault()

    for (var property in fields) {
      if (fields[property] === "") {
        setErrorMsg('Fill the spaces')
        return
      }
    }

    setLoading(true)
    try{
      await handleSubmit(fields);
      navigate("/")
    }
    catch(error) {
      switch(error.code){
      case 'auth/invalid-email':
        setErrorMsg("Invalid email")
        break;
      case 'auth/user-not-found':
        setErrorMsg("Authentication failed")
        break;
      case 'auth/weak-password':
        setErrorMsg("Password should have at least 6 characters")
        break;
      case 'passwords_dont_match':
        setErrorMsg("Passwords don't match")
        break;
      default:
        setErrorMsg("Some error occured")
        break;
      }
    }
    setLoading(false)
  }

  const handleLogInWithFacebook = async (e) => {
    e.preventDefault()

    setLoading(true)
    try{
      await signInWithFacebook();
      navigate("/")
    }
    catch(error) {
      switch(error.code){
        case 'auth/account-exists-with-different-credential':
          setErrorMsg("Try using other service. (Email connected to other service)")
          break;
        default:
          setErrorMsg("Couldn't log in using Facebook")
          break;
      }
    }
    setLoading(false)
  }

  const handleLogInWithGoogle = async (e) => {
    e.preventDefault()

    setLoading(true)
    try{
      await signInWithGoogle();
      navigate("/")
    }
    catch(error) {
      setErrorMsg("Couldn't log in using Google")
    }
    setLoading(false)
  }

  return <>
        {loadingFields || <div className='main'>
        <img className='logo' alt='logo' src={tigerLogo}></img>
        <h1 className='title'>{formConfig.title}</h1>
        <h3 className='subtitle'>{formConfig.subtitle}</h3>
        <div className='error'>
            {errorMsg}
        </div>
        <form className='form' onSubmit={(e) => submitFunction(e)}>
          {
            providedFields.map((field) => {
              return <div key={field.name} className={`input ${errorMsg && 'input_error'}`}>
                {field.icon}
                <input placeholder={field.placeholder} type={field.type} defaultValue={fields[field.name]} onChange={e => updateField(field.name, e.target.value)}></input>
              </div>
            })
          }
          <button className='submit' type='submit' disabled={loading}>Submit</button>
        </form>
        <div className='redirect_div'>
            <h2>{formConfig.redirectMessage}</h2>
            <Link to={formConfig.redirectTO}>{formConfig.redirectText}</Link>
        </div>
        <div className='services'>
          <button className='service_login' disabled={loading} onClick={(e) => handleLogInWithFacebook(e)}><BsFacebook/></button>
          <button className='service_login' disabled={loading} onClick={(e) => handleLogInWithGoogle(e)}><BsGoogle/></button>
        </div>
    </div>}
    </> 
}

export default CustomForm

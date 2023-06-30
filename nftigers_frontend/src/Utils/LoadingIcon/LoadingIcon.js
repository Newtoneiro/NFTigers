import React from 'react'
import {AiOutlineLoading3Quarters} from 'react-icons/ai'
import './loadingicon.css'

const LoadingIcon = () => {
  return (<div className='spin'>
    <AiOutlineLoading3Quarters/>
  </div>
  )
}

export default LoadingIcon
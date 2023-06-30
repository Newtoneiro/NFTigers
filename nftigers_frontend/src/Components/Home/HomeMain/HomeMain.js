import React from 'react'

import './homeMain.css'

import logo from '../../../resources/tiger.png'
import { useHomeContext } from '../HomeContext'
import { motion } from 'framer-motion'

const HomeMain = () => {
  const {setSite} = useHomeContext();

  return (
    <motion.div className='home_main'
      initial={{transform: "translateY(-50%)", opacity: 0}}
      animate={{transform: "translateY(0%)", opacity: 1}}
    >
        <div className='home_main_logo'>
          <img className='home_main_logo_img' alt='home_main_logo' src={logo}/>
          <h2 className='home_main_logo_text'>
            NFTigers
          </h2>
        </div>
        <div className='home_main_text_container'>
          <h1 className='home_main_text'>NFTIGERS</h1>
          <div className='home_main_text-2'>
            NFTIGERS
          </div>
          <div className='home_main_text-3'>
            NFTIGERS
          </div>
        </div>
        <div className='home_main_footing'>
          <button onClick={() => setSite("Auctions")}>Go To Auctions</button>
        </div>
      </motion.div>
  )
}

export default HomeMain

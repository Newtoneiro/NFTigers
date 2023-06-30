import React, { useState } from 'react'
import { useAuth } from '../Auth'

import logo from '../../resources/tiger.png'
import './navbar.css'
import { useHomeContext } from '../../Components/Home/HomeContext'
import LoadingIcon from '../LoadingIcon/LoadingIcon'

const Navbar = () => {
  const [inputMoney, setInputMoney] = useState(0);
  const [topUpLoading, setTopUpLoading] = useState(false)
  const {signout, currentUser, wallet, topUp} = useAuth();
  const {site, setSite, NavbarRoutes} = useHomeContext();

  const handleSignOut = async () => {
    await signout()
  }

  const handleTopUp = async () => {
    setTopUpLoading(true)
    await topUp(inputMoney)
    setInputMoney(0)
    setTopUpLoading(false)
  }

  return (
    <div className='navbar_main'>
      <div className='navbar_logo'>
        <img className='navbar_logo_img' alt='navbar_logo' src={logo}/>
        <h2>
          NFTigers
        </h2>
      </div>
      <div className='navbar_routes'>
        {
          NavbarRoutes.map((route) => {
            return <button key={route} className={`navbar_route ${site === route && 'navbar_route_selected'}`}
            onClick={() => setSite(route)}>{route}</button>
          })
        }
      </div>
      <div className='navbar_logout'>
        <div className='navbar_wallet'>
          <h4>Balance: {wallet} $</h4>
          <div className='navbar_wallet_spacing'/>
          {topUpLoading ? <LoadingIcon/> : <>
            <input className='navbar_wallet_input' type="number" min="1" max="99" value={inputMoney} onChange={(e) => setInputMoney(e.target.value)}></input>
            <button className='navbar_wallet_add' onClick={() => handleTopUp()}>+</button>
          </>}
        </div>
        <h2 className='navbar_logout_text'>
          {currentUser.email}
        </h2>
        <button className='navbar_logout_button' onClick={() => handleSignOut()}>Log out</button>
      </div>
    </div>
  )
}

export default Navbar

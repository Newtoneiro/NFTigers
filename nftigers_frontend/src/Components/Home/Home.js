import Navbar from '../../Utils/Navbar/Navbar'

import { AnimatePresence } from 'framer-motion';

import { useHomeContext } from './HomeContext'
import HomeMain from './HomeMain/HomeMain';
import Auctions from './Auctions/Auctions';
import NFT from './NFT/NFT';

import './home.css'
import { AuctionsProvider } from './Auctions/AuctionsContext';
import { NFTProvider } from './NFT/NFTContext';

const Home = () => {
  const {site} = useHomeContext();

  return (
    <AuctionsProvider>
      <NFTProvider>
        <div className='home_main_div'>
          <div className='home_main_panel'>
            <AnimatePresence>
              {site === "Home" && <HomeMain/>}
              {site === "Auctions" && <Auctions/>}
              {site === "NFT" && <NFT/>}
            </AnimatePresence>
          </div>
          <Navbar/>
        </div>
      </NFTProvider>
    </AuctionsProvider>
  )
}

export default Home

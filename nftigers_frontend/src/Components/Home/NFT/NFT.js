import React, { useEffect, useState } from 'react'

import { motion } from 'framer-motion'
import { useNFTContext } from './NFTContext'

import './NFT.css'

const NFT = () => {
  const [selectedNFT, setSelectedNFT] = useState(null)
  const {nfts} = useNFTContext()

  useEffect(() => {
    if (nfts.length > 0){
      setSelectedNFT(nfts[0])
    }
  }, [nfts])

  return (
    <motion.div className='nft_main'
      initial={{transform: "translateY(-50%)", opacity: 0}}
      animate={{transform: "translateY(0%)", opacity: 1}}
    >
      {selectedNFT && <>
        <div className='nft_selected'>
          <div className='nft_selected_image_container'>
                <img className='nft_selected_image_background' src={`data:image/jpeg;base64,${selectedNFT.graphic}`} alt='nft_image'></img>
                <img className='nft_selected_image' src={`data:image/jpeg;base64,${selectedNFT.graphic}`} alt='nft_image'></img>
          </div>
          <div className='nft_selected_desc'>
                <h2>{selectedNFT.author_name} {selectedNFT.author_surname}</h2>
                <div className='nft_selected_desc_right'>
                  <h2>Acquired: {selectedNFT.end_date.split('T')[0]}</h2>
                  <h3>Final Price: ${selectedNFT.current_price}</h3>
                </div>
          </div>
        </div>
        </>}
        {nfts.length === 0 && <h1 className='nft_nonfts'>You don't have any NFT's yet</h1>}
        <div className='nft_list'>
          {
            nfts && nfts.map((nft) => {
              return <div key={nft.nft_id} className={`nft_list_nft ${nft.nft_id === selectedNFT?.nft_id && "nft_list_nft_focused"}`} onClick={() => setSelectedNFT(nft)}>
                  <img className='nft_list_nft_image' src={`data:image/jpeg;base64,${nft.graphic}`} alt='nft_image'></img>
                </div>
            })
          }
        </div>
    </motion.div>
  )
}

export default NFT

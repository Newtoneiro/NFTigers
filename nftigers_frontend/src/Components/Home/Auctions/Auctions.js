import React, { useState } from 'react'

import { motion } from 'framer-motion'

import './auctions.css'
import { useAuctionsContext } from './AuctionsContext'
import {BsSearch} from 'react-icons/bs'
import { useAuth } from '../../../Utils/Auth'
import LoadingIcon from '../../../Utils/LoadingIcon/LoadingIcon'

const Auctions = () => {
  const [selectedCategory, setSelectedCategory] = useState(null)
  const [selectedClass, setSelectedClass] = useState(null)
  const [bidError, setBidError] = useState("")
  const [bidLoading, setBidLoading] = useState(false)
  const {auctions, loading, focusAuction, setFocusAuction, categories,
    classes, bidPrice, setBidPrice, bid, getAllAuctions} = useAuctionsContext();
  const { getWallet, currentUser } = useAuth()

  const handleSetFocusAuction = (auction) => {
    document.getElementById('auctions_grid').scrollTo({ top: 0, behavior: 'smooth' })
    setFocusAuction(auction)
    setBidPrice(auction.current_price)
  }

  const handleBid = () => {
    setBidLoading(true)
    bid().then(() => {
      getAllAuctions()
      getWallet()
      setBidError("")
      setBidLoading(false)
    }).catch((err) => {
      console.log(err)
      setBidError(err.response.data)
      setBidLoading(false)
    })
  }

  const Auction = ({auction}) => {
    return (<div key={auction.nft_id} className='auctions_item' onClick={() => handleSetFocusAuction(auction)}>
              {auction.user_id === currentUser.uid && 
              <h1 className='auctions_item_winner_header'>You're currently winning this auction</h1>}
              <img className='auctions_item_image' src={`data:image/jpeg;base64,${auction.graphic}`} alt='nft_image'></img>
              <div className='auctions_item_desc'>
                <h2>{auction.author_name}</h2>
                <h2>{auction.author_surname} - {auction.className}</h2>
                <div className='auctions_item_dates'>
                  <h3>{auction.start_date.split('T')[0]}</h3>
                  <h3>-</h3>
                  <h3>{auction.end_date.split('T')[0]}</h3>
                </div>
              </div>
              <h2 className='auctions_item_price'>${auction.current_price}</h2>
            </div>)
  }

  const FocusAuction = ({auction}) => {
    return (<div className='auctions_focused_auction'>
              {auction.user_id === currentUser.uid && 
              <h1 className='auctions_item_winner_header'>You're currently winning this auction</h1>}
              <div className='auctions_focused_auction_image_container'>
                <img className='auctions_focused_auction_image_background' src={`data:image/jpeg;base64,${auction.graphic}`} alt='nft_image'></img>
                <img className='auctions_focused_auction_image' src={`data:image/jpeg;base64,${auction.graphic}`} alt='nft_image'></img>
              </div>
              <div className='auctions_focused_auction_desc'>
                <h2>{auction.author_name} {auction.author_surname}  - {auction.className}</h2>
                <div className='auctions_focused_bid_container'>
                  {bidLoading ? <LoadingIcon/> :
                  <div className='auctions_focused_bid' onClick={() => {handleBid()}}>
                    <button className='auctions_focused_bid_button'>Bid!</button>
                    <h2>$</h2>
                    <input type="number" 
                          min={auction.current_price} 
                          value={bidPrice}
                          onChange={(e) => setBidPrice(e.target.value)}></input>
                  </div>
                  }
                  {bidError && <h2 className='auctions_focused_bid_error'>{bidError}</h2>}
                </div>
                <div className='auctions_focused_auction_desc_right'>
                  <div className='auctions_item_dates'>
                    <h3>{auction.start_date.split('T')[0]}</h3>
                    <h3>-</h3>
                    <h3>{auction.end_date.split('T')[0]}</h3>
                  </div>
                  <h2>${auction.current_price}</h2>
                </div>
              </div>
            </div>)
  }

  const handleChangeCategory = (category) => {
    if (category.category_id === selectedCategory?.category_id){
      setSelectedCategory(null)
    }
    else{
      setSelectedCategory(category)
    }
  }

  const handleChangeClass = (classElem) => {
    if (classElem.schoolclass_id === selectedClass?.schoolclass_id){
      setSelectedClass(null)
    }
    else {
      setSelectedClass(classElem)
    }
  }
  
  return (loading ||
    <motion.div className='auctions_main'
      initial={{transform: "translateY(-50%)", opacity: 0}}
      animate={{transform: "translateY(0%)", opacity: 1}}
    >
      <div className='auctions_header'>
        <div className='auctions_input'>
          <BsSearch/>
          <input type='text' placeholder='Search'/>
        </div>
        <div className='auctions_categories'>
          {categories.map((category, i) => {
            return <h2 key={i} 
                       className={`${category.category_id === selectedCategory?.category_id && 'selected'}`}
                       onClick={() => handleChangeCategory(category)}>
                      {category.name}</h2>
          })}
        </div>
        <div className='auctions_classes'>
          {classes.map((classElem) => {
            return <h2 key={classElem.schoolclass_id} 
                       className={`${classElem.schoolclass_id === selectedClass?.schoolclass_id && 'selected'}`}
                       onClick={() => handleChangeClass(classElem)}>
                      {classElem.name} {`[`}{classElem.start_year}{`]`}</h2>
          })}
        </div>
      </div>
      <div className='auctions_grid' id='auctions_grid'>
        {auctions.length > 0 && auctions.filter((auction) => {
          if (!selectedCategory) {
            return true;
          }
          return selectedCategory.category_id === auction.category_id
        }).filter((auction) => {
          if (!selectedClass) {
            return true;
          }
          return selectedClass.schoolclass_id === auction.schoolclass_id
        }).map((auction) => {
          if (focusAuction?.nft_id === auction.nft_id) {
            return <FocusAuction key={auction.nft_id} auction={auction}/>
          }
          else{
            return <Auction key={auction.nft_id} auction={auction}/>}
          })}
      </div>
    </motion.div>
  )
}

export default Auctions

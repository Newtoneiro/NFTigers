import { createContext, useContext, useState, useEffect } from "react";

import { useAuth } from "../../../Utils/Auth";

export const AuctionsContext = createContext();

export const useAuctionsContext = () => {
  return useContext(AuctionsContext);
}

export const AuctionsProvider = ({children}) => {
  const [auctions, setAuctions] = useState([])
  const [categories, setCategories] = useState([])
  const [classes, setClasses] = useState([])
  const [focusAuction, setFocusAuction] = useState(null)
  const [loading, setLoading] = useState(true)
  const [bidPrice, setBidPrice] = useState(0)
  const {authFetch, currentUser } = useAuth()

  const getAllAuctions = async () => {
    const fetchedAuctions = await authFetch.get('/auctions')
    setAuctions(fetchedAuctions.data)
  }

  useEffect(() => {
    async function fetchData(){
      setLoading(true)
      try{
	      const fetchedAuctions = await authFetch.get('/auctions')
        const fetchedCategories = await authFetch.get('/categories')
        const fetchedClasses = await authFetch.get('/classes')
        
        const auctionsWithClasses = fetchedAuctions.data.length > 0 && fetchedAuctions.data.map((auction) => {
          const className = fetchedClasses.data.find((classElem) => {
            return classElem.classroom_id === auction.classroom_id;
          }).name;
          return {...auction, className: className}
        })

        setAuctions(auctionsWithClasses)
        setCategories(fetchedCategories.data)
        setClasses(fetchedClasses.data)
      }
      catch (e){
        console.error(e)
      }
      setLoading(false)
    }

    return () => fetchData()
    
  }, [authFetch])

  const bid = () => {
    return authFetch.post('/auctions/', {
      usId: currentUser.uid,
      nftId: focusAuction.nft_id,
      bid: bidPrice
    })
  }

  return (
    <AuctionsContext.Provider
    value={{loading,
      auctions,
      focusAuction,
      setFocusAuction,
      categories,
      bidPrice,
      setBidPrice,
      bid,
      getAllAuctions,
      classes
    }}>
        {children}
    </AuctionsContext.Provider>
  )
}
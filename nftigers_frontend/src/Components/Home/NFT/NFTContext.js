import { createContext, useContext, useState, useEffect } from "react";

import { useAuth } from "../../../Utils/Auth";

export const NFTContext = createContext();

export const useNFTContext = () => {
  return useContext(NFTContext);
}

export const NFTProvider = ({children}) => {
  const [nfts, setNfts] = useState([])
  const [loading, setLoading] = useState(true)

  const {authFetch, currentUser} = useAuth()

  useEffect(() => {
    async function fetchData(){
      setLoading(true)
      try{
	      const fetchedNFTs = await authFetch.post('/nfts/', {
          usId: currentUser.uid
        })
        setNfts(fetchedNFTs.data)
      }
      catch (e){
        console.error(e)
      }
      setLoading(false)
    }

    fetchData()
  
  }, [authFetch, currentUser.uid])

  return (
    <NFTContext.Provider
    value={{nfts,
      loading
    }}>
        {children}
    </NFTContext.Provider>
  )
}
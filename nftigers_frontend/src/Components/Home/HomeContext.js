import { createContext, useContext, useState } from "react";


export const HomeContext = createContext();

export const useHomeContext = () => {
  return useContext(HomeContext);
}

export const HomeProvider = ({children}) => {
  const NavbarRoutes = ["Home", "Auctions", "NFT"]
  
  const [site, setSite] = useState("Home");

  return (
    <HomeContext.Provider
    value={{
      site,
      setSite,
      NavbarRoutes
    }}>
        {children}
    </HomeContext.Provider>
  )
}
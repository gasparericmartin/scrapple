import React, { useEffect, useState } from "react"
import { Outlet } from 'react-router-dom'


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  
  return (
    <>
      <h1 className='font-bold underline'>Nav Bar Here</h1> 
      <Outlet context={{isLoggedIn, setIsLoggedIn}}/>  
    </>
  )

}

export default App;

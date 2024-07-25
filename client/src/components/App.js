import React, { useEffect, useState } from "react"
import { Outlet } from 'react-router-dom'
import NavBar from './NavBar'


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [user, setUser] = useState({})
  
  useEffect(() => {
    fetch('/checksession')
    .then(r => {
      if(r.ok){
        r.json()
        .then((response) => console.log(response))
        .then(setIsLoggedIn(true))
      }
    })
  }, [])
  
  return (
    <>
      <NavBar isLoggedIn={isLoggedIn} 
              setIsLoggedIn={setIsLoggedIn}
              user={user}
              setUser={setUser}/>
      <Outlet context={{isLoggedIn, setIsLoggedIn}}/>  
    </>
  )

}

export default App;

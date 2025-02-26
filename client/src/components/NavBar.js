import { useOutletContext, useNavigate } from "react-router-dom"

function NavBar({isLoggedIn, setIsLoggedIn, user, setUser}) {
    const navigate = useNavigate() 
    
    function handleLogout() {
        fetch('/logout')
        .then(r => {
            if(r.ok) {
                setUser({})
                setIsLoggedIn(false)
                navigate('/login')
            }
            else{
                r.json().then((data) => console.log(data.error))
            }
        })
    }


    return (
        <div className="navbar bg-base-100">
            <div className="navbar-start">
                <div className="dropdown">
                <div tabIndex={0} role="button" className="btn btn-ghost btn-circle">
                    <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-5 w-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M4 6h16M4 12h16M4 18h7" />
                    </svg>
                </div>
                <ul
                    tabIndex={0}
                    className="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow">
                    {isLoggedIn ?
                    <>
                        <li><a href='/dashboard'>Dashboard</a></li>
                        <li><a href='/searches'>Searches</a></li>
                        <li><a>About</a></li>
                    </>
                    :
                    <>
                    <li><a href='/signup'>Signup</a></li>
                    <li><a>About</a></li>
                    </>
                    }
                </ul>
                </div>
            </div>
            <div className="navbar-center">
                <a className="btn btn-ghost text-xl">Scrapple</a>
            </div>
            <div className="navbar-end">
                {!isLoggedIn ?
                <button onClick={() => navigate('/login')}className="btn btn-circle">
                Login
                </button>
                :
                <button onClick={handleLogout} className="btn btn-circle">
                Logout
                </button>}
            </div>
            </div>
    )
}

export default NavBar
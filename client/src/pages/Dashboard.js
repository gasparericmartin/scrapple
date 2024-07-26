import { useOutletContext, useNavigate, redirect } from "react-router-dom"
import { useState, useEffect } from "react"
import SearchCard from '../components/SearchCard'
import PostCard from '../components/PostCard'
import NewSearchForm from '../components/NewSearchForm'

function Dashboard() {
    const navigate = useNavigate()
    const {isLoggedIn, setIsLoggedIn, user} = useOutletContext()
    const [userSearches, setUserSearches] = useState([])
    const [posts, setPosts] = useState([])
    const [showNewSearch, setShowNewSearch] = useState(false)
    
    useEffect(() => {
        fetch('/searches-by-user')
        .then(r => {
            if(r.ok) {
                r.json().then((data) => setUserSearches(data))
            }
        })

        fetch('/posts')
        .then(r => {
            if(r.ok) {
                r.json().then((data) => setPosts(data))
            }
        })
        
    }, [])

    function handleUpdateStates(rData) {
        setUserSearches(userSearches.map((search) => {
            if (search.id !== rData.search.id) {
                return search
            }
            else {
                return rData.search
            }
        }))

        setPosts([...posts, rData.posts])
    }

    

    if(isLoggedIn){
        return(
            <>
                <h1 className='pb-12' key={Date.now().toString(36) + Math.floor(Math.pow(10, 12) + Math.random() * 9*Math.pow(10, 12)).toString(36)}
                >Welcome {user.username}</h1>
                    {userSearches ? 
                    userSearches.map((search) => <SearchCard 
                    search={search} 
                    key={search.id}
                    handleUpdateStates={handleUpdateStates}/>)
                    : <h1 key={Date.now().toString(36) + Math.floor(Math.pow(10, 12) + Math.random() * 9*Math.pow(10, 12)).toString(36)}
                    >Loading searches</h1>}
                
                <button className='btn btn-sm btn-primary' 
                onClick={() => setShowNewSearch(!showNewSearch)}>New Search</button>
                <div key={46585}>
                    {showNewSearch ? <NewSearchForm user={user}
                                                    key={Date.now().toString(36) + Math.floor(Math.pow(10, 12) + Math.random() * 9*Math.pow(10, 12)).toString(36)}
                                                    userSearches={userSearches}
                                                    setUserSearches={setUserSearches}/> : null}
                </div>
                <div className='flex flex-wrap justify-center mt-0 p-4'>
                    {posts ?
                    posts.map((post) => <PostCard key={post.reddit_id} post={post} />)
                    : <h1>Loading posts</h1>}
                </div>
            </>
        )

    }
    else{
        return (
            <h1>Not yet logged in</h1>
        )
    }
}

export default Dashboard
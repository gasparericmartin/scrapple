import { useOutletContext, Navigate, redirect } from "react-router-dom"
import { useState, useEffect } from "react"
import SearchCard from '../components/SearchCard'
import PostCard from '../components/PostCard'
import NewSearchForm from '../components/NewSearchForm'

function Dashboard() {
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

    

    if(isLoggedIn){
        return(
            <>
                <h1 className='pb-12'>Welcome {user.username}</h1>
                    {userSearches ? 
                    userSearches.map((search) => <SearchCard 
                    search={search}
                    userSearches={userSearches}
                    setUserSearches={setUserSearches} 
                    key={search.id}
                    posts={posts}
                    setPosts={setPosts}/>)
                    : <h1>Loading searches</h1>}
                
                <button className='btn btn-sm btn-primary'
                onClick={() => setShowNewSearch(!showNewSearch)}>New Search</button>
                <div>
                    {showNewSearch ? <NewSearchForm user={user}
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
            <h1>Loading</h1>
            
            
        )
    }
}

export default Dashboard
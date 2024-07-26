import { useOutletContext, Navigate, redirect } from "react-router-dom"
import { useState, useEffect } from "react"
import SearchCard from '../components/SearchCard'
import PostCard from '../components/PostCard'

function Dashboard() {
    const {isLoggedIn, setIsLoggedIn, user} = useOutletContext()
    const [userSearches, setUserSearches] = useState([])
    const [posts, setPosts] = useState([])

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
                <h1>Welcome {user.username}</h1>
                {userSearches ? 
                userSearches.map((search) => <SearchCard search={search} key={search.id}/>)
                : <h1>Loading searches</h1>}
                <div className='flex flex-wrap justify-center mt-0 p-4'>
                    {posts ?
                    posts.map((post) => <PostCard key={post.id} post={post} />)
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
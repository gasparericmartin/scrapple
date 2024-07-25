import { useState, useEffect } from "react"
import SearchTableRow from "../components/SearchTableRow"
import { useOutletContext } from "react-router-dom"

function Searches() {
    const [searches, setSearches] = useState([])
    const {user} = useOutletContext()
    const [searchDetail, setSearchDetail] = useState(null)
    const [viewComments, setViewComments] = useState(null)
    
    useEffect(() => {
        fetch('/searches')
        .then(r => {
            if(r.ok) {
                r.json().then((data) => setSearches(data))
            }
            else{

            }
        })
    }, [])

    function handleRowClick(search) {
        //Setting search here for some reason puts it in a dictionary?
        if(!searchDetail) {
            setSearchDetail(search)
        }
        else if(search.id !== searchDetail.id) {
            setSearchDetail(search)
        }
        else{
            setSearchDetail(null)
        }
    }

    function CommentCard({comment, user}) {
        
        return (
            <>
                <li>{comment.body}</li>
                {comment.user_id === user.id ? 
                <button className='btn btn-sm'>Delete Comment</button>
                : null}
            </>
        )
    }

    function SearchDetailCard(search) {
        const userSearchIds = user.searches.map((search) => search.id)

        return (
        <div className='grid place-items-center'>
            <h1 className='font-bold'>{search.search.title}</h1>
            <p>{search.search.search_terms.replace('+', ',')}</p>
            <button className='btn btn-sm'
            onClick={() => setViewComments(!viewComments)}>View Comments</button>
            {viewComments ?
            <div>
                <ul>
                {search.search.comments.map((comment) => <CommentCard 
                                                            key={comment.id} 
                                                            comment={comment} 
                                                            user={user}/>)}
                </ul> 
                <button className='btn btn-sm'>Add Comment</button> 
            </div>
            : null}
            {userSearchIds.includes(search.search.id)?
            <button className='btn btn-sm'>Remove</button>
            :
            <button className='btn btn-sm'>Add</button>
            }
        </div>

        )
    }

    return (
        <div className='p-4 content-center'>
            
            {searchDetail ? <SearchDetailCard search={searchDetail}/>: null}
            
            
            <div className='overflow-x-hidden grow justify-end'>
                <table className='table'>
                    <thead>
                        <tr>
                        <th></th>
                        <th>Search Title</th>
                        <th>Search Terms</th>
                        </tr>
                    </thead>
                    <tbody>
                        {searches ? 
                        searches.map((search) => <SearchTableRow 
                                                    key={search.id}
                                                    search={search}
                                                    handleRowClick={handleRowClick}/>)
                        : <p>No Searches</p>}
                    </tbody>
                </table>
            </div>
        
        </div>
    )
}

export default Searches
import AddCommentForm from './AddCommentForm'
import CommentCard from './CommentCard'
import { useState } from 'react'

function SearchDetailCard({
                        search, 
                        user, 
                        viewComments, 
                        setViewComments,
                        handleAddComment,
                        searches,
                        setSearches}) {
    const userSearchIds = user.searches.map((search) => search.id)
    const [showCommentForm, setShowCommentForm] = useState(false)
    const [error, setError] = useState(false)

    function handleCommentDelete(comment) {
        fetch(`/comments/${comment.id}`, {
            method: 'DELETE'
        })
        .then(r => {
            if (r.ok) {
                    
                    const search = searches.filter((search) => search.id === comment.search_id)
                    
                    const modSearch = search[0].comments.filter((searchComment) => searchComment.id !== comment.id)
                    
                    search[0].comments = modSearch
                    
                    const new_searches = searches.map((search) => {
                        if(search.id !== modSearch.id){
                            return search
                        }
                        else{
                            return modSearch
                        }
                    })
                    setSearches(new_searches)
            }
            else {
                r.json().then((errorObj) => setError(errorObj.error))
            }
        })
    }

    function handleCommentEdit(comment, values) {
        const postObj = {
            body: values.comment
        }
        fetch(`/comments/${comment.id}`, {
            method: 'PATCH',
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify(postObj)
        })
        .then(r => {
            if(r.ok){
            console.log('did it')    
            
            }
            
        })
        

        
    }
    
    return (
    <div className='grid place-items-center'>
        <h1 className='font-bold'>{search.title}</h1>
        <p>{search.search_terms.replace('+', ',')}</p>
        <button className='btn btn-sm'
        onClick={() => setViewComments(!viewComments)}>View Comments</button>
        {error ? <p>{error}</p> : null}
        {viewComments ?
        <div>
            <ul>
            {search.comments.map((comment) => <CommentCard 
                                                        key={comment.id} 
                                                        comment={comment} 
                                                        user={user}
                                                        handleCommentDelete={handleCommentDelete}
                                                        handleCommentEdit={handleCommentEdit}/>)}
            </ul> 
            <button className='btn btn-sm'
            onClick={() => setShowCommentForm(!showCommentForm)}>Add Comment
            </button> 
            {showCommentForm ? <AddCommentForm 
                                handleSubmit={handleAddComment}
                                search={search}/> : null}
        </div>
        : null}
        {userSearchIds.includes(search.id)?
        <button className='btn btn-sm'>Remove</button>
        :
        <button className='btn btn-sm'>Add</button>
        }
    </div>

    )
}

export default SearchDetailCard
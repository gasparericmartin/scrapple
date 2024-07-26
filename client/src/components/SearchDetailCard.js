import AddCommentForm from './AddCommentForm'
import CommentCard from './CommentCard'
import { useState } from 'react'

function SearchDetailCard({
                        search, 
                        user, 
                        viewComments, 
                        setViewComments,
                        handleAddComment}) {
    const userSearchIds = user.searches.map((search) => search.id)
    const [showCommentForm, setShowCommentForm] = useState(false)

    return (
    <div className='grid place-items-center'>
        <h1 className='font-bold'>{search.title}</h1>
        <p>{search.search_terms.replace('+', ',')}</p>
        <button className='btn btn-sm'
        onClick={() => setViewComments(!viewComments)}>View Comments</button>
        {viewComments ?
        <div>
            <ul>
            {search.comments.map((comment) => <CommentCard 
                                                        key={comment.id} 
                                                        comment={comment} 
                                                        user={user}/>)}
            </ul> 
            <button className='btn btn-sm'
            onClick={() => setShowCommentForm(!showCommentForm)}>Add Comment
            </button> 
            {showCommentForm ? <AddCommentForm handleSubmit={handleAddComment}/> : null}
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
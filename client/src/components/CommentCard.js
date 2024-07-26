function CommentCard({comment, user, handleCommentDelete}) {
        
    return (
        <>
            <li>{comment.body}</li>
            {comment.user_id === user.id ? 
            <button onClick={() => handleCommentDelete(comment)} 
            className='btn btn-sm'>Delete Comment</button>
            : null}
        </>
    )
}

export default CommentCard
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

export default CommentCard
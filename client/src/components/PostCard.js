

function PostCard({post}) {
    const {
        id,
        reddit_id,
        created,
        title,
        url,
        img_url,
        body
    } = post
    
    if(img_url){
        return (
            <div className="card card-side bg-base-100 shadow-xl border-solid p-0 max-w-sm">
                <figure>
                    <img
                    className='max-w-screen-sm'
                    src={img_url}
                    alt="Image" />
                </figure>
                <div className="card-body max-w-screen-sm">
                    <h2 className="card-title">{title}</h2>
                    <p>{created}</p>
                    <p>{body}</p>
                    <div className="card-actions justify-end">
                    <a href={url} className="btn btn-primary">Reddit Link</a>
                    </div>
                </div>
            </div>
        )

    }
    else {
        return (
            <div className="card bg-base-100 w-96 shadow-xl">
                <div className="card-body">
                    <h2 className="card-title">{title}</h2>
                    <p>{body}</p>
                    <div className="card-actions justify-end">
                        <a href={url} className="btn btn-primary">Buy Now</a>
                    </div>
                </div>
            </div>
        )
    }

}

export default PostCard


function SearchCard({search}) {
    const search_terms = search.search_terms.split('+')
    
    return (
        <>
            <h1 className='font-bold pt-5'>{search.title}</h1>
            <ul>
                {search_terms.map((term) => <li key={term}>{term}</li>)}
            </ul>
        </>

    )

}

export default SearchCard
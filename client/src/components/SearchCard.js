import { useState } from "react"
import ScrapeForm from './ScrapeForm'

function SearchCard({search, posts, setPosts, userSearches, setUserSearches}) {
    const [showForm, setShowForm] = useState(false)
    const search_terms = search.search_terms.replace('+', ' ')
    
    function handleShowForm(e) {
        setShowForm(!showForm)
    }
    
    return (
        
        <div className="collapse bg-base-200 pt-3">
                <input type="radio" name="my-accordion-1" />
                <div className="collapse-title text-xl font-medium">{search.title}</div>
                    <div className="collapse-content">
                        <p>Search Terms: {search_terms}</p>
                <div className='pt-2'>
                    <button className='btn btn-sm btn-primary'
                    onClick={handleShowForm}>Scrape it baby!</button>
                    <button className='btn btn-sm btn-primary'>Scrape again</button>
                </div>
                </div>
                {showForm ? <ScrapeForm 
                            search={search} 
                            showForm={showForm}
                            setShowForm={setShowForm} 
                            posts={posts}
                            setPosts={setPosts}
                            userSeraches={userSearches}
                            setUserSearches={setUserSearches}/> : null}
        </div>
            
    

    )

}

export default SearchCard
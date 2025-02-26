import { useState, useEffect } from "react"
import SearchTableRow from "../components/SearchTableRow"
import { useOutletContext } from "react-router-dom"
import SearchDetailCard from '../components/SearchDetailCard'
import Formik from 'formik'
import * as Yup from 'yup'

function Searches() {
    const [searches, setSearches] = useState([])
    const {user} = useOutletContext()
    const [searchDetail, setSearchDetail] = useState(null)
    const [viewComments, setViewComments] = useState(null)
    console.log(`In Searches:`, searches)
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

    function handleAddComment(values, search) {
        const postObj = {
            body: values.comment,
            search_id: search.id,
        }
        console.log(values)
        console.log(search)

        fetch('/comments', {
            method: 'POST',
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify(postObj)
        })
        .then(r => {
            if(r.ok) {
                r.json().then((newComment) => {
                    setSearches(
                        searches.map((search) => {
                        if(search.id !== newComment.search_id) {
                            return search
                        }
                        else {
                            search.comments = [...search.comments, newComment]
                            return search
                        }
                        }
                    )
                )})
                    
            }
        })
    }

    return (
        <div className='p-4 content-center'>
            
            {searchDetail ? <SearchDetailCard 
                            search={searchDetail} 
                            user={user}
                            viewComments={viewComments}
                            setViewComments={setViewComments}
                            handleAddComment={handleAddComment}
                            searches={searches}
                            setSearches={setSearches}/>: null}
            
            
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
                        : <tr><td>No Searches</td></tr>}
                    </tbody>
                </table>
            </div>
        
        </div>
    )
}

export default Searches
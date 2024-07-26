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

    return (
        <div className='p-4 content-center'>
            
            {searchDetail ? <SearchDetailCard 
                            search={searchDetail} 
                            user={user}
                            viewComments={viewComments}
                            setViewComments={setViewComments}/>: null}
            
            
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
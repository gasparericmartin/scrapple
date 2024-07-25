import { useState } from "react"

function SearchTableRow({search, handleRowClick}) {
    const [clicked, setClicked] = useState()
    
    function handleClick() {
        setClicked(!clicked)
    }
    
    return (
        <>
            <tr id={search.id} className='hover' onClick={() => handleRowClick(search)}>
                <th>{search.id}</th>
                <td>{search.title}</td>
                <td>{search.search_terms.replace('+', ', ')}</td>
            </tr>
            {clicked ? 
            <button className='btn justify-self-center'>Add to dashboard</button>
            : null}
            
        </>
                        
    )

}

export default SearchTableRow
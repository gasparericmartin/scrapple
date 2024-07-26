import { useState } from 'react'
import {Formik, Form, Field} from 'formik'
import * as Yup from 'yup'

function ScrapeForm({search, 
                    showForm, 
                    setShowForm, 
                    posts, 
                    setPosts,
                    userSearches,
                    setUserSearches}) {    
    const [error, setError] = useState(null)
    

    function handleSubmit(values, search) {
        let reddit_id = ''

        if(values.before_after === 'before') {
            reddit_id = search.posts.reduce(
                function(a, b) {
                    const date1 = new Date(a.created).getTime()
                    const date2 = new Date(b.created).getTime()
                    
                    return date1 > date2 ? a.reddit_id : b.reddit_id
                }
            )
        }
        else if(values.before_after === 'after') {
            reddit_id = search.posts.reduce(
                function(a, b) {
                    const date1 = new Date(a.created).getTime()
                    const date2 = new Date(b.created).getTime()
                    
                    return date1 < date2 ? a.reddit_id : b.reddit_id
                }
            )
        }

        const postObj = {
            search_id: search.id,
            search_terms: search.search_terms,
            limit: values.limit,
            reddit_id: reddit_id,
            before_after: values.before_after
        }
        
        console.log(values)
        console.log(postObj)

        fetch('/scrape', {
            method: 'POST',
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify(postObj)
        })
        .then(r => {
            if(r.ok){
                r.json().then((data) => {setPosts([...posts, data.posts])})
                // console.log(userSearches)
                // setUserSearches(userSearches.map((search) => {
                //     if (search.id !== data.seach.id) {
                //         return search
                //     }
                //     else {
                //         return data.search
                //     }
                // }))
            }
            else {
                r.json().then((data) => console.log(data.error))
            }
        })
        
    }
    
    return (
        <div>
            <Formik
            validateOnChange={false}
            validateOnBlur={false}
            initialValues={{
                limit: '',
                before_after: ''

            }}
            validationSchema={Yup.object().shape({
                limit: Yup.number()
                    .min(25, 'Limit must be at least 25')
                    .max(100, 'Limit maximum is 100'),
                before_after: Yup.string(),

                
            })}
            onSubmit={(values) => {
                handleSubmit(values, search)
            }}
        >
            {({errors}) => (
                <Form className='max-w-sm mx-auto p-4'>

                    <div>
                    <label htmlFor='limit'>Number of Posts to Return (25-100)</label>
                    <Field 
                        name='limit' 
                        type='number' 
                        className='input input-bordered w-full max-w-xs'/>
                    {errors.limit ? <p>{errors.limit}</p>: null}
                    </div>

                    <div className="mb-4">
                        <label htmlFor='Newer/Older/All'>Before/After/All</label>
                        <div className="flex items-center">
                        <label className="mr-4">
                            <Field type="radio" name="before_after" value="before" className="mr-2" />
                            Newer
                        </label>
                        <label>
                            <Field type="radio" name="before_after" value="after" className="mr-2" />
                            Older
                        </label>
                        <label>
                            <Field type="radio" name="before_after" value="" className="mr-2 ml-4" />
                            All
                        </label>
                        </div>
                    </div>


                    <button type='submit>' className='btn btn-primary'>Submit</button>
                    {error ? <h2>{error}</h2>: null}
                </Form>
            )}
        </Formik>
        </div>
    )
}

export default ScrapeForm
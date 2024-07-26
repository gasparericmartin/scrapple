import { useState } from 'react'
import {Formik, Form, Field} from 'formik'
import * as Yup from 'yup'

function NewSearchForm({user, userSearches, setUserSearches}) {
    const [error, setError] = useState(null)

    function handleSubmit(values) {
        let search_terms = values.search_terms

        if(search_terms.includes('&') || search_terms.includes('+')) {
            search_terms = search_terms.replaceAll('&', '%26')
            search_terms = search_terms.replaceAll('+', '%2B')
        }
        search_terms = search_terms.replaceAll(' ', '+')
        
        const postObj = {
            user_id: user.id,
            title: values.title,
            search_terms: search_terms
        }

        fetch('/searches', {
            method: 'POST',
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify(postObj)
        })
        .then(r => {
            if(r.ok) {
                r.json().then((new_search) => setUserSearches([...userSearches, new_search]))
            }
            else {
                r.json().then((errorObj) => setError(errorObj.error))
            }
        })
    }

    return (
        <>
        <Formik
            validateOnChange={false}
            validateOnBlur={false}
            initialValues={{
                title: '',
                search_terms: '',
                

            }}
            validationSchema={Yup.object().shape({
                title : Yup.string()
                    .max(30, 'Titles can be up to 30 characters')
                    .required('Required'),
                search_terms: Yup.string()
                    .max(50, 'Search terms can be 50 characters max')
                    .required('Required')
            })}
            onSubmit={(values) => {
                handleSubmit(values, user)
            }}
        >
            {({errors}) => (
                <Form className='max-w-sm mx-auto p-4'>
                    <div>
                    <label htmlFor='title'>Title</label>
                    <Field 
                        name='title' 
                        type='text' 
                        className='input input-bordered w-full max-w-xs'/>
                    {errors.limit ? <p>{errors.limit}</p>: null}
                    </div>
                    
                    <div>
                    <label htmlFor='search_terms'>Search Terms</label>
                    <Field 
                        name='search_terms' 
                        type='text' 
                        className='input input-bordered w-full max-w-xs'/>
                    {errors.search_terms ? <p>{errors.search_terms}</p>: null}
                    </div>


                    <button type='submit>' className='btn btn-primary'>Submit</button>
                    {error ? <h2>{error}</h2>: null}
                </Form>
            )}
        </Formik>
        </>
    )
}

export default NewSearchForm
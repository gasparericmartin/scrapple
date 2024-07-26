import {Formik, Form, Field} from 'formik'
import * as Yup from 'yup'
import { useState } from 'react'

function AddCommentForm({handleSubmit}) {
    const [error, setError] = useState(false)
    
    return (
        <Formik
            validateOnChange={false}
            validateOnBlur={false}
            initialValues={{
                comment: ''
            }}
            validationSchema={Yup.object().shape({
                bike: Yup.string()
                    .max(140, 'Must be 140 characters or less')
                    .required('Required')
            })}
            onSubmit={(values, props, initialValues) => {
                handleSubmit(values)
                props.resetForm(initialValues)
            }}
        >
            {({errors}) => (
                <Form>
                    <Field name='comment' type='textarea' 
                        className='textarea textarea-bordered'/>
                    {errors.bike ? <p>{errors.bike}</p>: null}
            
                    <button 
                        type='submit' 
                        className='btn btn-sm'>Submit</button>

                    {error ? <h2>{error}</h2> : null}
                </Form>
            )}

        </Formik>
    )
}

export default AddCommentForm



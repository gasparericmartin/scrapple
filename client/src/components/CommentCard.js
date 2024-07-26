import { useState } from "react"
import {Formik, Form, Field} from 'formik'
import * as Yup from 'yup'


function CommentCard({comment, user, handleCommentDelete, handleCommentEdit}) {
    const [edit, setEdit] = useState(false) 
    
    function EditForm() {
        const [error, setError] = useState(false)
    
        return (
            <Formik
                validateOnChange={false}
                validateOnBlur={false}
                initialValues={{
                    comment: comment.body
                }}
                validationSchema={Yup.object().shape({
                    comment: Yup.string()
                        .max(140, 'Must be 140 characters or less')
                        .required('Required')
                })}
                onSubmit={(values, props, initialValues) => {
                    handleCommentEdit(comment, values)
                    props.resetForm('')
                }}
            >
                {({errors}) => (
                    <Form>
                        <Field name='comment' type='textarea' 
                            className='textarea textarea-bordered'/>
                        {errors.comment ? <p>{errors.comment}</p>: null}
                
                        <button 
                            type='submit' 
                            className='btn btn-sm'>Submit</button>

                        {error ? <h2>{error}</h2> : null}
                    </Form>
                )}

            </Formik>
        )
    }
    
    
    return (
        <>
            <li>{comment.body}</li>
            {comment.user_id === user.id ? 
            <div>
                <button onClick={() => handleCommentDelete(comment)} 
                className='btn btn-sm'>Delete Comment</button>
                <button onClick={() => setEdit(true)}
                className='btn btn-sm'>Edit Comment</button>
            </div>
            : null}

            {edit ? <EditForm /> : null}
            
        </>
    )
}

export default CommentCard
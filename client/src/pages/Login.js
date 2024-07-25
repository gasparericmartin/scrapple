import {useState} from 'react'
import { useOutletContext, useNavigate } from 'react-router-dom'
import {Formik, Form, Field} from 'formik'
import * as Yup from 'yup'

function Login() {
    const {isLoggedIn, setIsLoggedIn, user} = useOutletContext()
    const [error, setError] = useState(false)
    const navigate = useNavigate()

    function handleSubmit(values) {
        
        const postObj = {
            username: values.username,
            password: values.password
        }
        
        fetch('/login', {
            method: 'POST',
            headers: {
                'content-type': 'application/json'
            },
            body: JSON.stringify(postObj)
        })
        .then(r => {
            if(r.ok) {
                setIsLoggedIn(true)
                navigate('/dashboard')
            }
            else {
                r.json()
                .then((errorObj) => setError(errorObj.error))
            }
        })
    }
    

    return (
        <>
            <h1 className='text-2xl font-bold text-center'>Login</h1>
            <Formik
                validateOnChange={false}
                validateOnBlur={false}
                initialValues={{
                    username: '',
                    password: ''
                }}
                validationSchema={Yup.object().shape({
                    username: Yup.string()
                        .max(32, 'Usernames must be 32 characters max')
                        .required('Required'),
                        password: Yup.string()
                            .max(128, 'Passwords are 128 characters max')
                            .required('Required')
                })}
                onSubmit={(values) => {
                    handleSubmit(values)
                }}
            >
                {({errors}) => (
                    <Form>
                        <label htmlFor='username'>Username</label>
                        <Field 
                            name='username' 
                            type='text' 
                            className='input input-bordered w-full max-w-xs'/>
                        {errors.username ? <p>{errors.username}</p>: null}

                        <label htmlFor='password'>Password</label>
                        <Field 
                            name='password'
                            type='password'
                            className='input input-bordered w-full max-w-xs'/>
                        {errors.password ? <p>{errors.password}</p>: null}

                        <button type='submit>' className='btn btn-primary'>Submit</button>
                        {error ? <h2>{error}</h2>: null}
                    </Form>
                )}
            </Formik>
        </>
    )

}

export default Login
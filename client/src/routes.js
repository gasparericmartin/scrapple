import App from './components/App'
import Login from './pages/Login'
import Signup from './pages/Signup'

const routes = [
    {
        path: '/',
        element: <App />,
        children: [
            {
                path: '/login',
                element: <Login />
            },
            {
                path: '/signup',
                element: <Signup />
            }
        ]
    }
]

export default routes
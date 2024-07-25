import App from './components/App'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Dashboard from './pages/Dashboard'
import Searches from './pages/Searches'

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
            },
            {
                path: '/dashboard',
                element: <Dashboard />
            },
            {
                path: '/searches',
                element: <Searches />
            }
        ]
    }
]

export default routes
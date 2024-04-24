import { ImageProvider } from '@/components/domain/dashboard/ImageContext'
import Dashboard from '@/pages/Dashboard'
import Settings from '@/pages/Settings'
import Analysis from '@/pages/Analysis'
import Notification from '@/pages/Notification'
import {
  createBrowserRouter,
  RouterProvider,
  Route,
  Link,
} from 'react-router-dom'
import Navbar from './components/common/Navbar'

function App() {

  const router = createBrowserRouter([
    {
      path: "/",
      element: <Navbar />,
      children: [
        {
          path: "/dashboard",
          element: <Dashboard />,
        },
        {
          path: "/analysis",
          element: <Analysis />,
        },
        {
          path: "/notification",
          element: <Notification />,
        },
        {
          path: "/settings",
          element: <Settings />,
        },
      ],
    },

  ])

  return (
    <ImageProvider>
      <RouterProvider router={router} />
    </ImageProvider>
  )
}

export default App

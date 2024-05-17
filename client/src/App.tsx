import Dashboard from '@/pages/Dashboard'
import Settings from '@/pages/Settings'
import Correlation from '@/pages/Correlation'
import Notification from '@/pages/Notification'
import Board from "@/pages/Board";
import {
  createBrowserRouter,
  Navigate,
  RouterProvider,
} from 'react-router-dom'
import Navbar from '@/components/common/Navbar';
import ReactDOM from 'react-dom/client'
import "@/app/global.css"
import { Toaster } from "./components/base/toaster";
import BoardDetail from "./components/domain/board/post/DetailedPost";


function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <Navbar />,
      children: [
        {
          index: true,
          element: <Navigate to="/dashboard" replace />
        },
        {
          path: "/dashboard",
          element: <Dashboard />,
        },
        {
          path: "/correlation",
          element: <Correlation />,
        },
        {
          path: "/notification",
          element: <Notification />,
        },
        {
          path: "/settings",
          element: <Settings />,
        },
        {
          path: "/board",
          element: <Board />,
        },
        {
          path: "/board/:ids",
          element: <BoardDetail />
        }
      ],
    },

  ])

  return (
    <>
      <RouterProvider router={router} />
      <Toaster />
    </>

  )
}

export default App
ReactDOM.createRoot(document.getElementById('root')).render(
  <App />
)
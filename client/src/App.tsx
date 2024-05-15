import { createContext, useState, useContext } from "react";
import Dashboard from '@/pages/Dashboard'
import Settings from '@/pages/Settings'
import Analysis from '@/pages/Analysis'
import Notification from '@/pages/Notification'
import Board from "@/pages/Board";
import {
  createBrowserRouter,
  Navigate,
  RouterProvider,
} from 'react-router-dom'
import Navbar from './components/common/Navbar'
import ReactDOM from 'react-dom/client'
import "@/app/global.css"
import { Toaster } from "./components/base/toaster";
import BoardDetail from "./components/domain/board/post/DetailedPost";

const ImageContext = createContext();

const ImageProvider = ({ children }) => {
  const [image, setImage] = useState(null);

  return (
    <ImageContext.Provider value={{ image, setImage }}>
      {children}
    </ImageContext.Provider>
  );
};

const useImage = () => useContext(ImageContext);

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
        {
          path: "/board",
          element: <Board/>,
        },
        {
          path:"/board/:ids",
          element: <BoardDetail/>
        }
      ],
    },

  ])

  return (
    <ImageProvider>
      <RouterProvider router={router} />
      <Toaster />
    </ImageProvider>
  )
}

ReactDOM.createRoot(document.getElementById('root') as HTMLElement)
  .render(
    <App />
  )

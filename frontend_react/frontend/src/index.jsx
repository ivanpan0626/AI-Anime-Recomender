import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { createBrowserRouter,RouterProvider,Route } from 'react-router-dom'
import Home from './home';
import LoginPage from './assets/login';
import SearchPage from './assets/Search';
import ReccomendationsPage from './assets/Reccomend';
import FavoritesPage from './assets/Favorites';

//Creates the router that directs the user to multiple pages in the react frontend
const router = createBrowserRouter([
  {
    path: "/",
    element: <Home />,
  },
  {
    path: "login",
    element: <LoginPage/>,
  },
  {
    path: "searchAnimes",
    element: <SearchPage/>,
  },
  {
    path: "recAnimes",
    element: <ReccomendationsPage/>,
  },
  {
    path: "favAnimes",
    element: <FavoritesPage/>,
  }
  /*For more pages, copy template and paste above 
  {
    path: "<URL>",
    element: <function>,
  },
  */
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
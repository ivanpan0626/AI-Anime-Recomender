import React, { useState, useEffect } from "react";
import Navbar from "./Navbar";
import axios from 'axios';

function FavoritesPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState("");
  const [favorites, setFavorites] = useState([]);
  const getToken = sessionStorage.getItem("accessToken");
  const api = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    withCredentials: true,  //Include Cookies
  })

  //On page refresh or load, automatically checks for token to ensure its a valid user
  useEffect(() => {
    if (getToken && getToken != "" && getToken != undefined) {
      setIsLoggedIn(true);
      getUser();
    }
  }, []);

  const getUser = async () => {
    const response = await api.get('/get-user')
    .then(response =>{
      setUser(response.data.user)
      getFavs()
      //setFavorites(response.data.favoritesList)
    })
    .catch(error => {
      console.error("Error:", error.response.data.message)
    })
  };

  const getFavs = async () => {
    const response = await api.get('/anime/get-fav')
    .then(response =>{
      setFavorites(response.data)
    })
    .catch(error => {
      console.error("Error:", error.response.data.message)
    })
  };
  
  return (
    <>
      <Navbar></Navbar>
      {isLoggedIn ? (<>
      <h1>Favorites</h1>
        <div className="table-list">
      <table border="1" cellPadding="0" cellSpacing="0" width="100%" className="search-table">
        <tbody>
          <tr className="table-header" >
            <td><strong>Popularity</strong></td>
            <td> </td>
            <td><strong>Rating</strong></td>
            <td><strong>Title</strong></td>
            <td><strong>Synopsis</strong></td>
            <td><strong>Genre</strong></td>
          </tr>
          {favorites.map((animes, index) => (
                    <tr key={index}>
                        <td width="5%">{animes.popularity}</td>
                        <td width="7%">
                            <img src={animes.img_url} alt={animes.title} style={{ width: '100px', height: 'auto' }} />
                        </td>
                        <td width="5%">{animes.score}</td>
                        <td width="10%">{animes.title}</td>
                        <td width="50%">{animes.synopsis}</td>
                        <td width="11%">{animes.genre}</td>
                    </tr>
                ))}
        </tbody>
      </table>
      </div>
      </>) : (<></>)}
    </>
  );
}

export default FavoritesPage;

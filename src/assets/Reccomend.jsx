import React, { useState, useEffect } from "react";
import Navbar from "./Navbar";
import axios from 'axios';

function ReccomendationsPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState("");
  const [anime, setAnime] = useState([]);
  const [query, setQuery] = useState();
  const getToken = sessionStorage.getItem("accessToken");
  const api = axios.create({
    baseURL: 'http://127.0.0.1:5000',  // Your Flask backend URL
    withCredentials: true,  // Include cookies in requests
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
    })
    .catch(error => {
      console.error("Error:", error.response.data.message)
    })
  };

  const getAnime = async (e) => {
    e.preventDefault()
    const response = await api.get('/anime/getRecs', 
      {params: { "query": query }})
    .then(response =>{
      setAnime(response.data)
    })
    .catch(error => {
      //console.error("Error:", error.response.data.message)
    })
  };

  return (
    <>
      <Navbar></Navbar>
      {isLoggedIn ? (<>
      <div className="searchBar">
      <form onSubmit={getAnime}>
                <input
                    type="text"
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Search for an anime"
                />
                <button type="submit" className="searchbar-btn">Search</button>
            </form>
      </div>
      <div className="table-list">
      <table border="20" cellPadding="0" cellSpacing="0" width="100%" className="search-table">
        <tbody>
          <tr className="table-header" >
            <td><strong>Popularity</strong></td>
            <td> </td>
            <td><strong>Rating</strong></td>
            <td><strong>Title</strong></td>
            <td><strong>Synopsis</strong></td>
            <td><strong>Genre</strong></td>
          </tr>
          {anime.map((animes, index) => (
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

export default ReccomendationsPage;

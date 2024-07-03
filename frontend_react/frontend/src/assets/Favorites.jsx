import React, { useState, useEffect } from "react";
import Navbar from "./Navbar";
import axios from 'axios';

function FavoritesPage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState("");
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

  return (
    <>
      <Navbar></Navbar>
      {isLoggedIn ? (<><h1> hi welcome user: {user} <br></br> {sessionStorage.getItem("accessToken")}
        <br></br> Keys Page
      </h1>
      </>) : (<></>)}
    </>
  );
}

export default FavoritesPage;

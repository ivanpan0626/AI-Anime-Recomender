import React, { useState, useEffect } from "react";
import Navbar from "./assets/Navbar";
import "./home.css";
import axios from 'axios';

function Home() {
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
      {isLoggedIn ? (<><h1 align="center"> Hello!<br></br>Welcome back, {user}!<br></br>
      </h1>
      </>) : (<></>)}
    </>
  );
}

export default Home;

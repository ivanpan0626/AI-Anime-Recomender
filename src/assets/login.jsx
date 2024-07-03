import { useState } from "react";
import Navbar from "./Navbar";
import axios from 'axios';

function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const getToken = sessionStorage.getItem("accessToken")
  const api = axios.create({
    baseURL: 'http://127.0.0.1:5000',  // Your Flask backend URL
    withCredentials: true,  // Include cookies in requests
  })
  
  const onSubmit = async (e) => {
    e.preventDefault();

    const data = {
      email,
      password,
    };
    const response = await api.post('/login', data)
      .then(response =>{
        sessionStorage.setItem("accessToken", response.data.message)
      window.location.href="http://localhost:3000";
      })
      .catch(error => {
        console.error("Error:", error.response.data.message)
      })
  };
  
  return (
    <>
      <Navbar></Navbar>
      {getToken && getToken!="" && getToken!=undefined ? 
      (<><h1>You are logged in {getToken}</h1></>) : (<>
        <form onSubmit={onSubmit}>
        <h3 align="center">Login</h3>
        <div className="form-group">
          <label htmlFor="email">Email Adress</label>
          <input
            type="email"
            className="form-control"
            id="email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter Email"
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            className="form-control"
            id="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter Password"
          />
        </div>
        <br />

        <button type="submit" className="btn btn-primary">
          Submit
        </button>
        </form>
    </>
      )}
    </>
  );
}

export default LoginPage;

import { useState } from "react";
import Navbar from "./Navbar"
import axios from 'axios';

const SignupForm = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");
  const api = axios.create({
    baseURL: 'http://127.0.0.1:5000',  // Your Flask backend URL
    withCredentials: true,  // Include cookies in requests
  })

  const onSubmit = async (e) => {
    e.preventDefault();

    const data = {
      username,
      email,
      password1,
      password2,
    };

    const response = await api.post('/signup', data)
    .then(response =>{
      window.location.href="http://localhost:3000/login";
    })
    .catch(error => {
      alert(error.response.data.message);
    })
  };
  
  return (
        <form onSubmit={onSubmit}>
        <div>
          <label className="modal-items" htmlFor="username">Username</label>
          <input
            type="text"
            className="form-control"
            id="username"
            name="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter Username"
          />
        </div>
        <div>
          <label className="modal-items" htmlFor="email">Email Adress</label>
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
        <div>
          <label className="modal-items" htmlFor="password1">Password</label>
          <input
            type="password"
            className="form-control"
            id="password1"
            name="password1"
            value={password1}
            onChange={(e) => setPassword1(e.target.value)}
            placeholder="Enter Password"
          />
        </div>
        <div>
          <label className="modal-items" htmlFor="password2">Password Confirmation</label>
          <input
            type="password"
            className="form-control"
            id="password2"
            name="password2"
            value={password2}
            onChange={(e) => setPassword2(e.target.value)}
            placeholder="Confirm Password"
          />
        </div>
        <br />

        <button type="submit" className="btn btn-primary">
          Signup
        </button>
        </form>
  );
};

export default SignupForm;

import React, {useState} from "react"
import {Link} from "react-router-dom"
export function Login(){

    const [email, setEmail] = useState ('');
    const [pass, setPass] = useState ('');

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(email);
    }

    return (
        <div className="auth-form-container">
        <img src="../images/SAICMotor_logo.png" alt="logo" width={300} height={300} />
        <form className="loginForm" onSubmit={handleSubmit}>
            <label htmlFor="email">Email: </label>
            <input onChange={(e) => setEmail(e.target.value)} value={email} type="email" placeholder="Username@email.com" id="email"/>
            <label htmlFor="Password">Password: </label>
            <input onChange={(e) => setPass(e.target.value)} value={pass} type="Password" placeholder="Password" id="Password"/>
            <button type="submit">Login</button>
            <Link to="/Register"><button className="link-button">Don't have an account yet? Click here to sign up.</button></Link>
        </form>
        <Link to="/Login/Dashboard"><button>Developer button</button></Link>
        </div>
    )
}
import React, {useState} from "react"
import {Link} from "react-router-dom"
export function Register() {
    const [email, setEmail] = useState ('');
    const [pass, setPass] = useState ('');
    const [firstName, setFirstName] = useState ('');
    const [lastName, setLastName] = useState ('');

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log(email);
    }
    return (
        <div className="auth-form-container">
        <img src="../images/SAICMotor_logo.png" alt="logo" width={300} height={300} />
        <form className="registerForm" onSubmit={handleSubmit}>
            <label htmlFor="FirstName">First Name:</label>
            <input onChange={(e) => setFirstName(e.target.value)} value={firstName} type="text" placeholder="First Name" id="firstName"/>
            <label htmlFor="FirstName">Last Name:</label>
            <input onChange={(e) => setFirstName(e.target.value)} value={lastName} type="text" placeholder="Last Name" id="lastName"/>
            <label htmlFor="email">Email:</label>
            <input onChange={(e) => setEmail(e.target.value)} value={email} type="email" placeholder="Username@email.com" id="email"/>
            <label htmlFor="Password">Password</label>
            <input onChange={(e) => setPass(e.target.value)} value={pass} type="Password" placeholder="Password" id="Password"/>
            <Link to="/">
                <button>Register</button>
            </Link>
        </form>
       
        </div>
    )
}
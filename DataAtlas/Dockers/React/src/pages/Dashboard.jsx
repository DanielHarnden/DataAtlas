import React, {useState, Component, useEffect} from "react";
import axios from 'axios';
import {Link} from "react-router-dom"



class DropDownMenu extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            selectedOption: '',
            selectedOptionTwo: '',
            imageSrc: ''
        };
    }
    
    componentDidMount() {
        fetch('http://localhost:5000/requestDatabases')
            .then(response => response.json())
            .then(data => this.setState({ data }));
    }
    
    handleOptionChange = (event) => {
        this.setState({ selectedOption: event.target.value });
    }

    handleOptionChangeTwo = (event) => {
        this.setState({ selectedOptionTwo: event.target.value });
    }

    handleButtonClick = () => {
        const { selectedOption } = this.state;
        const { selectedOptionTwo } = this.state;
        if (selectedOption !== "") {
            if (selectedOptionTwo == "")
            {
                fetch(`http://localhost:5000/beginAtlasing/${selectedOption}`, {responseType: 'blob'})
                    .then((response) => {
                        if (!response.ok) {
                        throw new Error('Network response was not ok');
                        }
                        return response.blob();
                    })
                    .then((blob) => {
                        const imageUrl = URL.createObjectURL(blob);
                        this.setState({ imageSrc: imageUrl });
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });
            } else if (selectedOption != selectedOptionTwo) {
                fetch(`http://localhost:5000/beginAtlasingTwo/${selectedOption}/${selectedOptionTwo}`, {responseType: 'blob'})
                    .then((response) => {
                        if (!response.ok) {
                        throw new Error('Network response was not ok');
                        }
                        return response.blob();
                    })
                    .then((blob) => {
                        const imageUrl = URL.createObjectURL(blob);
                        this.setState({ imageSrc: imageUrl });
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });
            }
        }
    };
    
    render() {
        const { data, selectedOption, selectedOptionTwo, imageSrc } = this.state;
        
        return (
            <div className="buttons">
                <select className="dropdown" value={selectedOption} onChange={this.handleOptionChange}>
                    <option value="">Select a Database...</option>
                    {data.map(item => (
                        <option key={item} value={item}>{item}</option>
                    ))}
                </select>

                <br></br><br></br>

                <select className="dropdown" value={selectedOptionTwo} onChange={this.handleOptionChangeTwo}>
                    <option value="">Select a Second Database to Merge (or leave blank)...</option>
                    {data.map(item => (
                        <option key={item} value={item}>{item}</option>
                    ))}
                </select>

                <br></br><br></br>
                <button className="generate" onClick={this.handleButtonClick}>Generate Database Image</button>
                <br></br><br></br>

                {imageSrc && <img className="generatedIMG" src={imageSrc} alt="logo" style={{width: '95%'}}/>}
            </div>
        );
    }
}




export function Dashboard(){

    return (
        <>
        <div  className="auth-form-container">
        <form className="dataForm" >
        <Link to="/">
        <button className="signout"><img className="img" src="../images/SAICMotor_logo.png" alt="logo" /></button>
        </Link>
           <h1>Data Atlas Dashboard</h1>
        </form>



        <div>
            <DropDownMenu />
        </div>    



           
        
        </div>
        <div/>
        </>
    )
}
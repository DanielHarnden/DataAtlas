import {Route, Routes} from  "react-router-dom";
import {Login} from  "./pages/Login";
import {Register} from  "./pages/Register";
import {Dashboard} from  "./pages/Dashboard";
import './App.css';


function App() {
return (
<div className="App">
<Routes>
  <Route path="/" element={<Login />} />
  <Route path="/Register" element={<Register />} />
  <Route path="/Login/Dashboard" element={<Dashboard />} />
</Routes>
  </div>
  )
}

export default App

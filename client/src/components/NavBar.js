import React, { useContext } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { AppContext } from "./AppProvider";
import style from './appNavBarStyle.css';

function NavBar() {
    const { currentUser, setCurrentUser } = useContext(AppContext)
    const navigate = useNavigate();

    function handleLogoutClick() {
        fetch(`${process.env.REACT_APP_API_URL}/logout`, {
            method: "DELETE" 
        })
        .then(res => {
          if (res.ok) {
            sessionStorage.removeItem('user_id')
            setCurrentUser(null);
            navigate(`/login`)
          }
        });
    }

    return (
        <nav>
            {currentUser ? (
            <>
                <NavLink 
                to="/profile"
                className="nav-link"
                activeClassName="active">Profile</NavLink>
                <NavLink 
                to="/sensors"
                className="nav-link"
                activeClassName="active">Sensors</NavLink>
                <NavLink 
                to="/statuses"
                className="nav-link"
                activeClassName="active">Statuses</NavLink>
                <span onClick={handleLogoutClick} className="nav-link">Logout</span>
            </>
            ) : (
            <>  
                <NavLink 
                to="/"
                className="nav-link"
                activeClassName="active">Home</NavLink>
                <NavLink 
                to="/login"
                className="nav-link"
                activeClassName="active">Login</NavLink>
            </>
            )}
        </nav>
    )
}

export default NavBar;
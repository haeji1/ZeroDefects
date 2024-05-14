import React, { useState } from 'react';
import SamsungLogo from '@/assets/images/Logo_WHITE.png';
import { Link, Outlet } from 'react-router-dom';
import './Navbar.css'

function Navbar() {
    const [activeLink, setActiveLink] = useState('dashboard');

    const handleClick = (name) => {
        setActiveLink(name);
    };

    const selectedLinkClass = (name) => {
        return activeLink === name ? 'selected' : '';
    };

    return (
        <>
            <div className="flex flex-row justify-between h-[80px] w-full bg-slate-700">
                <a href="/dashboard">
                    <img src={SamsungLogo} className="h-full" alt="Samsung" />
                </a>
                <div className='flex flex-row space-x-8 text-[25px] items-center mx-10'>
                    <Link to="/dashboard" onClick={() => handleClick('dashboard')}>
                        <p className={`link ${selectedLinkClass('dashboard')}`}>대시보드</p>
                    </Link>
                    <Link to="/analysis" onClick={() => handleClick('analysis')}>
                        <p className={`link ${selectedLinkClass('analysis')}`}>분석</p>
                    </Link>
                    <Link to="/board" onClick={() => handleClick('board')}>
                        <p className={`link ${selectedLinkClass('board')}`}>게시판</p>
                    </Link>
                    <Link to="/notification" onClick={() => handleClick('notification')}>
                        <p className={`link ${selectedLinkClass('notification')}`}>알림</p>
                    </Link>
                    <Link to="/settings" onClick={() => handleClick('settings')}>
                        <p className={`link ${selectedLinkClass('settings')}`}>관리</p>
                    </Link>
                </div>
            </div>
            <Outlet />
        </>
    );
}

export default Navbar;

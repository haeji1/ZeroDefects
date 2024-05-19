import { useState } from 'react';
import SamsungLogo from '@/assets/images/Logo_WHITE.png';
import { Link, Outlet } from 'react-router-dom';
import './Navbar.css'

function Navbar() {

    const [activeLink, setActiveLink] = useState('dashboard');

    const selectedLinkClass = (name: string) => {
        return activeLink === name ? 'selected' : '';
    };

    const handleClickLink = (e: React.MouseEvent<HTMLParagraphElement, MouseEvent>) => {
        const { id } = e.target as React.DetailedHTMLProps<React.HTMLAttributes<HTMLParagraphElement>, HTMLParagraphElement>;
        setActiveLink(id!);
    }

    return (
        <>
            <div className="flex flex-row justify-between h-[80px] w-full bg-slate-700">
                <a href="/">
                    <img src={SamsungLogo} className="h-full" alt="Samsung" />
                </a>
                <div className='flex flex-row space-x-8 text-[25px] items-center mx-10'>
                    <Link to="/dashboard">
                        <p id='dashboard' className={`link ${selectedLinkClass('dashboard')}`} onClick={handleClickLink}>
                            대시보드
                        </p>
                    </Link>
                    <Link to="/correlation">
                        <p id='correlation' className={`link ${selectedLinkClass('correlation')}`} onClick={handleClickLink}
                        >상관 분석</p>
                    </Link>
                    <Link to="/tglife">
                        <p id='tglife' className={`link ${selectedLinkClass('tglife')}`} onClick={handleClickLink}>
                            수명 분석
                        </p>
                    </Link>
                    <Link to="/board">
                        <p id='board' className={`link ${selectedLinkClass('board')}`} onClick={handleClickLink}>게시판</p>
                    </Link>
                    <Link to="/settings">
                        <p id='settings' className={`link ${selectedLinkClass('settings')}`} onClick={handleClickLink}>데이터 관리</p>
                    </Link>
                </div>
            </div>
            <Outlet />
        </>
    );
}

export default Navbar;

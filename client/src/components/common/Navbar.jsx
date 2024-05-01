import SamsungLogo from '@/assets/images/Logo_WHITE.png'
import { Link, Outlet } from 'react-router-dom'

function Navbar() {
    return (
        <>
            <div className="flex flex-row justify-between h-[80px] w-full bg-slate-700">
                <img src={SamsungLogo} height='auto' alt="" />
                <div className='flex flex-row space-x-8 text-[25px] items-center mx-10'>
                    <Link to="dashboard">
                        <p>대시보드</p>
                    </Link>
                    <Link to="/analysis">
                        <p>분석</p>
                    </Link>
                    <Link to="/notification">
                        <p>알림</p>
                    </Link>
                    <Link to="/settings">
                        <p>관리</p>
                    </Link>
                </div>
            </div>
            <Outlet />
        </>
    )
}

export default Navbar;
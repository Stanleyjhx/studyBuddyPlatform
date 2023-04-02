import React, { useState } from 'react';
import { AppstoreOutlined, MailOutlined, SettingOutlined, UsergroupAddOutlined} from '@ant-design/icons';
import { Button } from 'antd';
import './Header.css'
import { useNavigate } from 'react-router-dom';
import cookie from 'react-cookies';
import { useCookies } from 'react-cookie';

const Header: React.FC = () => {
  let history = useNavigate();
  const sessionID = cookie.load("session_id");
  const [userCookies, setUserCookie, removeUserCookies] = useCookies(["session_id"]);

  const logout = () => {
    // setUserCookie([])
    removeUserCookies("session_id", {path: '/'});
    window.location.reload(false);
    history.push('/login')
  }

  return (
    <header className='page__header'>
        <h3 className='header__title'>NexUS</h3>
        <Button type="primary" onClick={logout}>Logout</Button>
    </header>
  )
};

export default Header;

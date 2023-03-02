import React, { useState } from 'react';
import { AppstoreOutlined, MailOutlined, SettingOutlined, UsergroupAddOutlined} from '@ant-design/icons';
import { Button } from 'antd';
import './Header.css'

const Header: React.FC = () => {
  const [status, setStatus] = useState('logined');
  return (
    <header className='page__header'>
        <h3 className='header__title'>Study Buddy Platform</h3>
        <Button type="primary">Logout</Button>
    </header>
  )
};

export default Header;

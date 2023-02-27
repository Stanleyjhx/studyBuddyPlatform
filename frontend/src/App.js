import { FileOutlined, PieChartOutlined, UserOutlined, DesktopOutlined, TeamOutlined, HomeOutlined} from '@ant-design/icons';
import { Breadcrumb, Layout, Menu, theme } from 'antd';
import { useState } from 'react';
import { useNavigate, Routes, Route } from 'react-router-dom'
import Home from './components/Home/Home';
import './App.css'
import Navbar from './components/Header/Header';

const { Header, Content, Footer, Sider } = Layout;
function getItem(label, key, icon, children) {
  return {
    key,
    icon,
    children,
    label,
  };
}
const items = [
  getItem('Home', '/home', <HomeOutlined />),
  getItem('Profile', '/profile', <UserOutlined />),
  getItem('Group', '/group', <TeamOutlined />),
  getItem('Group Management', '/group_mgmt', <DesktopOutlined />),
];
const App = () => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();

  const onClick = (e) => {
    navigate(e.key, {replace: true});
  }
  const {
    token: { colorBgContainer },
  } = theme.useToken();
  return (
    <Layout
      style={{
        minHeight: '100vh',
      }}
    >
      <Sider className='sidebar' collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}>
        <div className='sidebar__title' >
        </div>
        <Menu theme="dark" defaultSelectedKeys={['/home']} mode="inline" items={items} onClick={onClick}/>
      </Sider>
      <Layout className="site-layout">
          <Navbar />
        <Content
          style={{
            margin: '0 16px',
          }}
        >
          <Breadcrumb
            style={{
              margin: '16px 0',
            }}
          >
            <Breadcrumb.Item>User</Breadcrumb.Item>
            <Breadcrumb.Item>Bill</Breadcrumb.Item>
          </Breadcrumb>
          <div
            className='page__content'
            style={{
              padding: 24,
              minHeight: 560,
              background: colorBgContainer,
            }}
          >
            <Routes>
              <Route exact path='/home' element={<Home />}></Route>
            </Routes>
          </div>
        </Content>
        <Footer
          style={{
            textAlign: 'center',
          }}
        >
          Study Buddy Platform ©2023
        </Footer>
      </Layout>
    </Layout>
  );
};
export default App;
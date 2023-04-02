import { FileOutlined, PieChartOutlined, UserOutlined, DesktopOutlined, TeamOutlined, HomeOutlined} from '@ant-design/icons';
import { Breadcrumb, Layout, Menu, theme, Button, Tooltip, Typography, Card } from 'antd';
import { useState, useEffect } from 'react';
import { useNavigate, Routes, Route, useLocation } from 'react-router-dom'
import Home from './pages/Home/Home';
import ProfilePage from './pages/Profile/Profile';
import Group from './pages/Group/Group';
import GroupDetail from './pages/GroupDetail/GroupDetail'; 
import Members from './pages/GroupDetail/Members';
import GroupInfo from './pages/GroupDetail/GroupInfo';
import StudyPlanDetail from './pages/GroupDetail/StudyPlan/StudyPlanDetail';
import Register from './pages/Login/Register';
import Login from './pages/Login/Login';
import './App.css'
import Navbar from './components/Header/Header';
import Task from './pages/Invitation/Tasks';
import cookie from 'react-cookies';
import background from "./images/campus-background-3.jpg"

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
  getItem('Group Management', '/group_invitation/', <DesktopOutlined />),
];
const App = () => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  let location = useLocation();
  const [current, setCurrent] = useState(location.pathname);

  useEffect(() => {
    if (location) {
        if( current !== location.pathname ) {
            setCurrent(location.pathname);
        }
    }
}, [location, current]);

  const handleClick = (e) => {
    setCurrent(e.key);
  }

  const onClick = (e) => {
    navigate(e.key, {replace: true});
  }
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  const sessionID = cookie.load("session_id");

  if (sessionID == undefined || sessionID == "") {
    return (
      <div style={{height:"100vh", width:"180vh", top:"0", left:"0", right:"0", backgroundImage:`url(${background})`}}>
        <Routes className='content__detail'>
          <Route 
            exact path='/register' 
            element={
              <Card style={{position:"absolute", top:"10%", left:"35%", width:"35%"}} title="Register NexUS">
                <Register/>
              </Card>
            } 
            className='page__element'>
          </Route>
          <Route 
            exact path='/login' 
            element={
              <Card style={{position:"absolute", top:"20%", left:"40%", width:"25%"}} title="Login NexUS">
                <Login/>
              </Card>
            } 
            className='page__element'>
          </Route>
        </Routes>
      </div>
    )
  }
  
  return (
    <Layout>
      <Sider className='sidebar' collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}>
        <div className='sidebar__title' >
        </div>
        <Menu theme="dark" defaultSelectedKeys={['/home']} mode="inline" items={items} onClick={onClick} selectedKeys={[current]}/>
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
          </Breadcrumb>
          <div
            className='page__content'
            style={{
              minHeight: '80vh',
              background: colorBgContainer,
            }}
          >
            <Routes className='content__detail'>
              <Route exact path='/home' element={<Home />} className='page__element'></Route>
              <Route exact path='/group' element={<Group />} className='page__element'></Route>
              <Route exact path='/profile' element={<ProfilePage />} className='page__element'></Route>
              <Route exact path='/group_detail/plans/:id' element={<GroupDetail />} className='page__element'></Route>
              <Route exact path='/group_detail/members/:id' element={<Members />} className='page__element'></Route>
              <Route exact path='/group_detail/info/:id' element={<GroupInfo />} className='page__element'></Route>
              <Route exact path='/group_detail/plan_detail/:id' element={<StudyPlanDetail />} className='page__element'></Route>
              <Route exact path='/group_invitation/' element={<Task />} className='page__element'></Route>
            </Routes>
          </div>
        </Content>
        <Footer
          style={{
            textAlign: 'center',
          }}
        >
          NexUS ©2023
        </Footer>
      </Layout>
    </Layout>
  );
};
export default App;

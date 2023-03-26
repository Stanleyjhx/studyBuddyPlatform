import { FileOutlined, PieChartOutlined, UserOutlined, DesktopOutlined, TeamOutlined, HomeOutlined} from '@ant-design/icons';
import { Breadcrumb, Layout, Menu, theme, Button, Tooltip } from 'antd';
import { useState } from 'react';
import { useNavigate, Routes, Route } from 'react-router-dom'
import Home from './pages/Home/Home';
import Group from './pages/Group/Group';
import GroupDetail from './pages/GroupDetail/GroupDetail'; 
import Members from './pages/GroupDetail/Members';
import GroupInfo from './pages/GroupDetail/GroupInfo';
import StudyPlanDetail from './pages/GroupDetail/StudyPlan/StudyPlanDetail';
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
  getItem('Group Management', '/group_mgmt/plans', <DesktopOutlined />),
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
    <Layout>
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
              <Route exact path='/group_detail/plans/:id' element={<GroupDetail />} className='page__element'></Route>
              <Route exact path='/group_detail/members/:id' element={<Members />} className='page__element'></Route>
              <Route exact path='/group_detail/info/:id' element={<GroupInfo />} className='page__element'></Route>
              <Route exact path='/group_detail/plan_detail/:id' element={<StudyPlanDetail />} className='page__element'></Route>
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

import { React, useState, useEffect }  from 'react';
import { LikeOutlined, MessageOutlined, StarOutlined, TeamOutlined, FileAddOutlined, UserOutlined, PlusCircleOutlined } from '@ant-design/icons';
import { Avatar, List, Typography, Popover, Button, Tabs, Tooltip } from 'antd';
import { useCookies } from 'react-cookie';
import { Link, useNavigate, useParams } from 'react-router-dom';
import Loader from '../../components/Loader';
import AddPopUp from './AddGroupPopUp';
import axios from 'axios';
import cookie from 'react-cookies';
import './Group.css'

const Group: React.FC = () => {
  const [cookies, setCookie, removeCookie] = useCookies(['session_id']);
  const [err, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [addVisible, setAddVisible] = useState(false);
  const [actualData, setData] = useState([]);

  const params = useParams();
  const sessionID = cookie.load("session_id");
  const config = {
    headers: { Authorization: `Bearer ${sessionID}` }
  };

  const fetchData = async () => {
    const res = await axios.get(
      `${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/group/get_groups?limit=0&offset=100`,
      config
    );
    setData(res.data.data.groups);
  };
  const fetchMyData = async () => {
    const res = await axios.get(
      `${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/group/get_groups?limit=0&offset=100&show_mygroup=true`,
      config
    );
    setData(res.data.data.groups);
  };

  useEffect(() => {
    fetchData();
  }, []);


  const groupCards = () => {
    return (
      <List
      itemLayout="vertical"
      bordered="true"
      size="large"
      pagination={{
      onChange: (page) => {
        console.log(page);
      },
      pageSize: 5,
      align: "center"
      }}
      dataSource={actualData}
      renderItem={(item) => (
        <List.Item
          key={item.group_name}
          onClick={() => console.log(item.group_id)}
        >
          <List.Item.Meta
            avatar={<TeamOutlined />}
            title={
              <Link to={`/group_detail/plans/${item.group_id}`} >
                <a href={item.href}>{item.group_name}</a >
              </Link>
            }
            description={item.group_description}
          />
          
          <Popover
            title="User Information" 
            trigger="hover"
            content={
              <div>
                <p>Student ID: {item.group_owner.student_id}</p>
                <p>Name: {item.group_owner.first_name + ' ' + item.group_owner.last_name}</p>
                <p>Major: {item.group_owner.major}</p>
                <p>Description: {item.group_owner.description}</p>
              </div>
            }
          >
            <Button><UserOutlined/>Group owner: {item.group_owner.user_name}</Button>
          </Popover>
        </List.Item>
      )}
    />
    )
  }
  
  const showAddModal = () => {
    setAddVisible(true);
  };

  const tabLabel = ["All Groups", "My Groups"]
  return (
    <div>
      <header className='detail__header'>
        <Typography/>
        <Tooltip title="Create A Study Group">
          <Button onClick={showAddModal} type="primary" ><PlusCircleOutlined style={{fontSize: "120%"}} /> Create A Study Group </Button>
        </Tooltip>
      </header>
      
       <AddPopUp setAddVisible={setAddVisible} addVisible={addVisible}/>
      
      <Tabs
          defaultActiveKey="1"
          centered
          onChange= {(activeKey) => {
              if (activeKey == "All Groups") {
                fetchData()
              } else {
                fetchMyData()
              }
            }
          }
          items={[{
            label: "All Groups",
            key: "All Groups",
          }, {
            label: "My Groups",
            key: "My Groups",
          }]}
      />
      
       <List
        itemLayout="vertical"
        bordered="true"
        size="large"
        pagination={{
        onChange: (page) => {
          console.log(page);
        },
        pageSize: 5,
        align: "center"
        }}
        dataSource={actualData}
        renderItem={(item) => (
          <List.Item
            key={item.group_name}
            onClick={() => console.log(item.group_id)}
          >
            <List.Item.Meta
              avatar={<TeamOutlined />}
              title={
                <Link to={`/group_detail/plans/${item.group_id}`} >
                  <a href={item.href}>{item.group_name}</a >
                </Link>
              }
              description={item.group_description}
            />
            
            <Popover
              title="User Information" 
              trigger="hover"
              content={
                <div>
                  <p>Student ID: {item.group_owner.student_id}</p>
                  <p>Name: {item.group_owner.first_name + ' ' + item.group_owner.last_name}</p>
                  <p>Major: {item.group_owner.major}</p>
                  <p>Description: {item.group_owner.description}</p>
                </div>
              }
            >
              <Button><UserOutlined/>Group owner: {item.group_owner.user_name}</Button>
            </Popover>
          </List.Item>
        )}
      /> 
    </div>
  )
};

export default Group;

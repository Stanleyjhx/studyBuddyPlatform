import { React, useState, useEffect }  from 'react';
import { LikeOutlined, MessageOutlined, StarOutlined, UserOutlined } from '@ant-design/icons';
import { Avatar, List, Space, Typography } from 'antd';
import { useParams } from 'react-router-dom';
import Loader from '../../../components/Loader';
import axios from 'axios';
import cookie from 'react-cookies';

const EventMembers: React.FC = () => {
  const [members, setMembers] = useState(null);
  const [cachedData, setCachedData] = useState(null);

  const sessionID = cookie.load("session_id");
  const config = {
    headers: { Authorization: `Bearer ${sessionID}` }
  };

  const params = useParams();
  const eventId = params.id; 

  useEffect(() => {
    if (cachedData) {
      setMembers(cachedData);
      return;
    }
    const fetchData = async () => {
      const res = await axios.get(
        `${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/group_detail/get_event_members/${eventId}?limit=0&offset=10`,
        config
      );
      setMembers(res.data.data.event_members);
      setCachedData(res.data.data.event_members);
    };
    fetchData();
  }, []); 

  if (members == undefined) {
      return (
        <div>
          <header className='detail__header'>
          </header>
          <Loader />
        </div>
      );
  }
  return (
    <div>
      <List
        itemLayout="vertical"
        size="large"
        pagination={{
        onChange: (page) => {
            console.log(page);
        },
        pageSize: 4,
        align: "center"
        }}
        dataSource={members}
        renderItem={(item) => (
        <List.Item
            key={item.person_name}
            onClick={() => console.log(item.person_id)}
        >
            <List.Item.Meta
            avatar={<UserOutlined />}
            title={<a href={item.href}>{item.first_name + " " + item.last_name}</a>}
            description={<Typography>Self-description: {item.description}</Typography>}
            />
        </List.Item>
        )}
      />
    </div>
  )
};

export default EventMembers;

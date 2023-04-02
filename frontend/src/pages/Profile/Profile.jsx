import { React, useState, useEffect }  from 'react';
import { Avatar, Button, Descriptions, Modal } from 'antd';
import EditProfilePopUp from './EditProfilePopUp';
import axios from 'axios';
import cookie from 'react-cookies';
import Loader from '../../components/Loader';


const sessionID = cookie.load("session_id");
const config = {
  headers: { Authorization: `Bearer ${sessionID}` }
};

const ProfilePage = () => {
  const [profile, setProfile] = useState({});
  const [visible, setVisible] = useState(false);
  const [deleteVisible, setDeleteVisible] = useState(false);
  // open popup

  useEffect(() => {
    const fetchData = async () => {
      const res = await axios.get(
        `${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/personal-info/get_personal_info`,
        config
      );
      setProfile(res.data.data.personal_info);
      console.log(res);
    };
    fetchData();
  }, []); 

  const showModal = () => {
    setVisible(true);
  };

  if (profile == {} || profile == undefined) {
    return <Loader/>
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', margin:"24px" }}>
      <Avatar 
        size={128} 
        style={{ margin: '2rem' }}
        src={"https://img.freepik.com/free-vector/cute-panda-with-bamboo_138676-3053.jpg?w=1380&t=st=1679817462~exp=1679818062~hmac=dc50e3b780c4fa14a5253ca757d32f9724ff617c0c71a37b6ee3dba260faa625"}
      >
      </Avatar>
      <Descriptions title="Personal Information" bordered={true}>
        <Descriptions.Item label="Name">{profile.first_name + ' ' + profile.last_name}</Descriptions.Item>
        <Descriptions.Item label="Email">{profile.email}</Descriptions.Item>
        <Descriptions.Item label="Major">{profile.major}</Descriptions.Item>
        <Descriptions.Item label="Student ID">{profile.student_id}</Descriptions.Item>
        <Descriptions.Item label="Description">{profile.description}</Descriptions.Item>
      </Descriptions>
      <Button type="primary" style={{ margin: '2rem' }} onClick={showModal}>Edit Profile</Button>
      <EditProfilePopUp visible={visible} setVisible={setVisible} data={profile}/>
      <Modal></Modal>
    </div>
  );
}

export default ProfilePage;

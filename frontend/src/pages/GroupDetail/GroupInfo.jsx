import { React, useState, useEffect }  from 'react';
import { LikeOutlined, MessageOutlined, StarOutlined, UserOutlined, EditOutlined, PlusSquareOutlined } from '@ant-design/icons';
import { Avatar, List, Space, Typography, Tooltip, Button, Descriptions, Tag, Popover } from 'antd';
import TopTab from './TopTab';
import { useParams } from 'react-router-dom';
import Loader from '../../components/Loader';
import EditGroupPopUp from '../Group/EditGroupPopUp';
import axios from 'axios';
import cookie from 'react-cookies';

const GroupInfo: React.FC = () => {
  const [groupInfo, setGroupInfo] = useState(null);
  const [cachedData, setCachedData] = useState(null);
  const [err, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [editGroupVisible, setEditGroupVisible] = useState(false);
  const [isMember, setIsMember] = useState(false);

  const sessionID = cookie.load("session_id");
  const config = {
    headers: { Authorization: `Bearer ${sessionID}` }
  };

  const params = useParams();
  const groupId = params.id; 

  const showEditGroupModal = () => {
    setEditGroupVisible(true);
  };

  const colors= ["magenta","gold","geekblue", "red", "volcano", "lime", "orange", "blue"]

  useEffect(() => {
    if (cachedData) {
        setGroupInfo(cachedData);
      return;
    }
    const fetchData = async () => {
      const res = await axios.get(
        `${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/group/get_groups?group_id=${groupId}&limit=0&offset=10`,
        config
      );
      setGroupInfo(res.data.data.groups[0]);
      setCachedData(res.data.data.groups[0]);
      setIsMember(res.data.data.groups[0].is_a_member);
    };
    fetchData();
  }, []); 

  const joinGroup = async () => {
    const requestBody = {
      apply_reason: ""
    }
    const res = await axios.post(
      `${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/invitation/apply/${groupId}`,
      requestBody,
      config
    );
  }

  if (groupInfo == undefined) {
      return (
        <div>
          <header className='detail__header'>
              <TopTab tab={"info"} groupId={groupId}/>
          </header>
          <Loader />
        </div>
      );
  }
  return (
    <div>
      <header className='detail__header'>
          <TopTab tab={"members"} groupId={groupId}/>
      </header>
      <div className='card__header' style={{height:"5%"}}>
        <Button onClick={joinGroup} disabled={isMember}><PlusSquareOutlined/>Join This Group</Button>
        <Tooltip title="Only Group Members Can Edit Group Information">
          <Button onClick={showEditGroupModal} disabled={!isMember}><EditOutlined style={{ fontSize:"120%" }} /> Edit Group Information</Button>
        </Tooltip>
          <EditGroupPopUp visible={editGroupVisible} setVisible={setEditGroupVisible} data={groupInfo}/>
      </div>
      <Descriptions  layout="vertical" bordered  style={{margin:"20px"}} >
        <Descriptions.Item label="Group Name"> {`${groupInfo.group_name}`} </Descriptions.Item>
        <Descriptions.Item label="Group Description">{`${groupInfo.group_description}`}</Descriptions.Item>
        <Descriptions.Item label="Group size">20</Descriptions.Item>
        <Descriptions.Item label="Group Owner">
          <Popover
            title="User Information" 
            trigger="hover"
            content={
              <div>
                <p>Student ID: {groupInfo.group_owner.student_id}</p>
                <p>Name: {groupInfo.group_owner.first_name + ' ' + groupInfo.group_owner.last_name}</p>
                <p>Major: {groupInfo.group_owner.major}</p>
                <p>Description: {groupInfo.group_owner.description}</p>
              </div>
            }
          >
            <Button><UserOutlined/>User: {groupInfo.group_owner.user_name}</Button>
          </Popover>
        </Descriptions.Item>
        <Descriptions.Item label="Module Tags">
          <Space size={[0, 8]} wrap>    
          {
            groupInfo.module_tags.split(',').map((function (elem, idx) {return(<Tag color={colors[idx]}>{elem}</Tag>)}))
          }
          </Space>
        </Descriptions.Item>
      </Descriptions>
    </div>
  )
};

export default GroupInfo;
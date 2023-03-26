import { React, useState, useEffect }  from 'react';
import { LikeOutlined, MessageOutlined, StarOutlined, UserOutlined, EditOutlined, ClockCircleFilled, PlusSquareOutlined } from '@ant-design/icons';
import { Avatar, List, Space, Typography, Tooltip, Button, Descriptions, Tag, Popover, Modal } from 'antd';
import { useParams } from 'react-router-dom';
import Loader from '../../../components/Loader';
import axios from 'axios';
import dayjs from 'dayjs';
import cookie from 'react-cookies';

const showTimeFormat = 'YYYY-MM-DD HH:mm';


const EventInfo: React.FC = () => {
  const [eventInfo, setEventInfo] = useState(null);
  const [isMember, setIsMember] = useState(false);
  const [countMembers, setCountMembers] = useState(1);
  const [open, setOpen] = useState(false);
  const [confirmLoading, setConfirmLoading] = useState(false);

  const sessionID = cookie.load("session_id");
  const config = {
    headers: { Authorization: `Bearer ${sessionID}` }
  };

  const params = useParams();
  const eventId = params.id; 

  useEffect(() => {
    const fetchData = async () => {
      const res = await axios.get(
        `${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/group_detail/get_study_plan_by_id/${eventId}`,
        config
      );
      setEventInfo(res.data.data.study_plan);
      setIsMember(res.data.data.is_a_member);
    };

    const fetchCountMembers = async () => {
      const res = await axios.get(
        `${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/group_detail/get_event_members/${eventId}?limit=0&offset=10`,
        config
      );
      setCountMembers(res.data.data.event_members.length);
    }
    fetchData();
    fetchCountMembers();
  }, []); 

  const showModal = () => {
    console.log(open)
    setOpen(true);
  };

  

  const handleCancel = () => {
    console.log('Clicked cancel button');
    setOpen(false);
  };

  const joinEvent = () => {
    axios.post(`${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/group_detail/add_event_member/${eventId}`, {}, config)
    .then((response) => {
      console.log('Post created successfully!', response.data);
      window.location.reload(false);
    })
    .catch((error) => {
      console.error('Error adding event member', error);
    });

  }

  const handleOk = () => {
    setConfirmLoading(true);
    joinEvent()
    setTimeout(() => {
      setOpen(false);
      setConfirmLoading(false);
    }, 2000);
  };


  if (eventInfo == undefined) {
      return (
        <div>
          <Loader />
        </div>
      );
  }
  return (
    <div>
      <div style={{display:"flex", justifyContent:"flex-end", marginRight:"25px"}}>
        <Button 
          style={{display:"flex", gap:"10px"}} 
          disabled={eventInfo.capacity <= countMembers || isMember}
          onClick={showModal}
        >
          <PlusSquareOutlined style={{ fontSize:"150%" }}/>
          <Typography>Join this event</Typography>
        </Button>
        <Modal
          title="Join this event..."
          open={open}
          onOk={handleOk}
          confirmLoading={confirmLoading}
          onCancel={handleCancel}
        >
          <p>Do you wish to join this study plan?</p>
        </Modal>
      </div>
      <Descriptions  layout="vertical" bordered  style={{margin:"20px"}} >
        <Descriptions.Item label="Event Name"> {`${eventInfo.event_name}`} </Descriptions.Item>
        <Descriptions.Item label="Event Description">
            {`${eventInfo.event_description}`}
        </Descriptions.Item>
        <Descriptions.Item label="Event Capacity">{countMembers + ' / ' + eventInfo.capacity}</Descriptions.Item>
        <Descriptions.Item label="Event Holder">
          <Popover
            title="User Information" 
            trigger="hover"
            content={
              <div>
                <p>Student ID: {eventInfo.event_holder.student_id}</p>
                <p>Name: {eventInfo.event_holder.first_name + ' ' + eventInfo.event_holder.last_name}</p>
                <p>Major: {eventInfo.event_holder.major}</p>
                <p>Description: {eventInfo.event_holder.description}</p>
              </div>
            }
          >
            <Button><UserOutlined/>User: {eventInfo.event_holder.user_name}</Button>
          </Popover>
        </Descriptions.Item>
        <Descriptions.Item label="Event Time">
          <Typography>
          <ClockCircleFilled />{"\t"}
          {dayjs(eventInfo.start_time).format(showTimeFormat)} - {dayjs(eventInfo.end_time).format(showTimeFormat)}
          </Typography>
        </Descriptions.Item>
      </Descriptions>
    </div>
  )
};

export default EventInfo;

import { React, useState, useEffect, FC }  from 'react';
import { LikeOutlined, MessageOutlined, StarOutlined, InfoCircleOutlined, FileAddOutlined, UserOutlined, PlusCircleOutlined } from '@ant-design/icons';
import { Avatar, List, Tag, Typography, Popover, Button, Tabs, Tooltip } from 'antd';
import { useCookies } from 'react-cookie';
import { Link, useNavigate, useParams } from 'react-router-dom';
import Loader from '../../components/Loader';
import AddPopUp from './RejectPopUp';
import axios from 'axios';
import cookie from 'react-cookies';
import RejectPopUp from './RejectPopUp';
import ApprovePopUp from './ApprovePopUp';
import './Tasks.css'

const Task = () => {
  const [cookies, setCookie, removeCookie] = useCookies(['session_id']);
  const [err, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [actualData, setData] = useState([]);
  const [flag, setFlag] = useState(0);
  const [selectedRequest, setSelectedRequest] = useState(-1);

  const params = useParams();
  const sessionID = cookie.load("session_id");
  const config = {
    headers: { Authorization: `Bearer ${sessionID}` }
  };

  const [approveVisible, setApproveVisible] = useState(false);
  const [rejectVisible, setRejectVisible] = useState(false);
  // open popup
  const showApproveModal = (id) => {
    setApproveVisible(true);
    setSelectedRequest(id);
  };

  const showRejectModal = (id) => {
    setRejectVisible(true);
    setSelectedRequest(id);
    console.log("request_id", selectedRequest);
  }

  const fetchData = async () => {
    const res = await axios.get(
     `${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/invitation/get_requests?role_type=2&limit=0&offset=100`,
     config
    );
    setData(res.data.data.requests);
  };
  const fetchMyData = async () => {
    const res = await axios.get(
      `${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/invitation/get_requests?role_type=1&limit=0&offset=100`,
      config
    );
    setData(res.data.data.requests);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const tabLabel = ["My Task", "My Request"]
  return (
    <div>
      <header className='detail__header'>
        <Typography/>
      </header>
      
      <Tabs
          defaultActiveKey="1"
          centered
          onChange= {(activeKey) => {
              if (activeKey == "My Task") {
                fetchData()
                setFlag(1)
              } else {
                fetchMyData()
                setFlag(0)
              }
            }
          }
          items={[{
            label: "My Task",
            key: "My Task",
          }, {
            label: "My Request",
            key: "My Request",
          }]}
      />
      <RejectPopUp visible={rejectVisible} setVisible={setRejectVisible} data={selectedRequest}/>
      <ApprovePopUp visible={approveVisible} setVisible={setApproveVisible} data={selectedRequest}/>
       <List
        itemLayout="vertical"
        bordered="true"
        size="large"
        pagination={{
        pageSize: 5,
        align: "center"
        }}
        dataSource={actualData}
        renderItem={(item) => (
          <div>
          <List.Item
            key={item.group_name}
          >
            <List.Item.Meta
              avatar={<InfoCircleOutlined style={{fontSize:"120%"}} />}
              title={ "Request to Join the Group" }
              description={item.group_description}
            />
          
            <Tooltip title="Status">{(item.status == -1) && <Tag color="grey">Rejected</Tag>}</Tooltip>
            <Tooltip title="Status">{(item.status == 0) && <Tag color="orange">Pending</Tag>}</Tooltip>
            <Tooltip title="Status">{(item.status == 1) && <Tag color="green">Approved</Tag>}</Tooltip>

            <Typography>Requester Information</Typography>
           
            <div className='event_details'>
            Name: {item.group_owner_id.first_name + ' ' + item.group_owner_id.last_name}
            </div>

            
            <div className='event_details'>
            Major: {item.group_owner_id.major}
            </div>
            

            <Typography>Group Information</Typography>

            <div className='event_details'>
            Group Name: {item.group_info.group_name}
            </div>

            <div className='event_details'>
            Group Owner: {item.group_info.group_owner}
            </div>
        
            {
              (item.status == 0 && flag == 1) && 
              <div>
                <Button 
                  style={{marginRight:"12px"}} 
                  type="primary" 
                  id='approval'
                  onClick={() => showApproveModal(item.request_id)}
                >
                  <span>Approve</span>
                </Button>
                <Button type="primary" danger id='reject' onClick={() => showRejectModal(item.request_id)}>
                  <span>Reject</span>
                </Button>
              </div>
            }
          </List.Item>
          </div>
        )}
      /> 
    </div>
  )
};

export default Task;

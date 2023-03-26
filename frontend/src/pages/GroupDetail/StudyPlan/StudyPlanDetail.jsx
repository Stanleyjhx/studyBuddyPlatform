import { React, useState, useEffect }  from 'react';
import { LikeOutlined, MessageOutlined, StarOutlined, TeamOutlined, FileAddOutlined, UserOutlined, PlusCircleOutlined, InfoCircleOutlined } from '@ant-design/icons';
import { Avatar, List, Typography, Popover, Button, Tabs, Tooltip } from 'antd';
import { useCookies } from 'react-cookie';
import { Link, useNavigate, useParams } from 'react-router-dom';
import Loader from '../../../components/Loader';
import axios from 'axios';
import cookie from 'react-cookies';
import EventMembers from './EventMembers';
import EventInfo from './EventInfo';

const StudyPlanDetail: React.FC = ({planId}) => {
  let history = useNavigate();
  const [eventId, setEventId] = useState(planId);
  const [pageStatus, setPageStatus] = useState("info");

  const sessionID = cookie.load("session_id");
  const config = {
    headers: { Authorization: `Bearer ${sessionID}` }
  };

  return(
    <div>
      <Tabs
        defaultActiveKey="1"
        centered
        onChange= {(activeKey) => {
            if (activeKey == "Study Plan Info") {
              setPageStatus("info");
            } else {
              setPageStatus("members");
            }
          }
        }
        items={[{
          label: (
            <span>
              <InfoCircleOutlined />
              Study Plan Info
            </span>
          ),
          key: "Study Plan Info",
        }, {
          label: (
            <span>
              <TeamOutlined />
              Event Members
            </span>
          ),
          key: "Event Members",
        }]}
      />
      {(pageStatus=="members" && <EventMembers/>)}
      {(pageStatus=="info" && <EventInfo/>)}
    </div>

  );
}

export default StudyPlanDetail;

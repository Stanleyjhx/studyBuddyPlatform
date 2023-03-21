import { react } from 'react';
import { useNavigate } from 'react-router-dom';
import { Tabs, Button } from 'antd';
import { ScheduleOutlined, TeamOutlined, EditOutlined, FileAddOutlined } from '@ant-design/icons';

const TopTab: React.FC = ( {tab} ) => {
    let history = useNavigate();
  
    const handleTabClick = (key) => {
      history.push(`/${key}`)
    }
    return (
      <Tabs
        onChange={(key) => {
          history(`/group_mgmt/${key}`);
        }}
        defaultActiveKey={tab}
        items={
          [
            {
              label: (
                <span>
                  <ScheduleOutlined />
                  Study Plan
                </span>
              ),
              key: "plans",
            },
            {
              label: (
                <span>
                  <TeamOutlined />
                  Group Members
                </span>
              ),
              key: "members",
            }
          ]
        }
      />
    )
  };

  export default TopTab;
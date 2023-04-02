import { react, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Tabs, Button } from 'antd';
import { ScheduleOutlined, TeamOutlined, EditOutlined, FileAddOutlined, InfoCircleOutlined} from '@ant-design/icons';

const TopTab: React.FC = ( {tab, groupId} ) => {
    let history = useNavigate();
    const [groupdId, setGroupId] = useState(groupId);
  
    const handleTabClick = (key) => {
      history.push(`/${key}`)
    }
    return (
      <Tabs
        onChange={(key) => {
          history(`/group_detail/${key}/${groupId}`);
          setGroupId(groupId);
        }}
        defaultActiveKey={tab}
        items={
          [ {
              label: (
                <span>
                  <InfoCircleOutlined />
                  Study Group Info
                </span>
              ),
              key: "info",
            },
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
  
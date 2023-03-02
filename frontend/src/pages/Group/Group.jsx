import { React, useState, useEffect }  from 'react';
import { LikeOutlined, MessageOutlined, StarOutlined, TeamOutlined } from '@ant-design/icons';
import { Avatar, List, Space } from 'antd';
import Loader from '../../components/Loader';

const data2 = [
  {
    "group_id": 1,
    "group_name": "studyBuddy",
    "group_owner": 4,
    "group_description": "Study Buddy dev group"
  },
  {
    "group_id": 2,
    "group_name": "group2",
    "group_owner": 7,
    "group_description": "Another group"
  }
]

interface GroupData {
  "group_id": number,
  "group_name": string,
  "group_owner": number,
  "group_description": string
};

const IconText = ({ icon, text }: { icon: React.FC; text: string }) => (
  <Space>
    {React.createElement(icon)}
    {text}
  </Space>
);

const body = {
  "limit":0,
  "offset":10,
  "show_deleted":0
}

const Group: React.FC = () => {
  const [actualData, setData] = useState(null);
  const [err, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch("http://192.168.0.132:5000/group/get_groups?limit=0&offset=100",{
      method: "GET",
      header: {"Content-type": "application/json"}
    })
    .then((res) => res.json())
    .then((data) => setData(data));
  }, []);

    // const fetchData = async () => {
    //     try {
    //         const response = await fetch(
    //             "http://192.168.0.132:5000/get_groups"
    //         );
    //         if (response.status != 200) {
    //           throw new Error(
    //             `This is an HTTP error: The status is ${response.status}`
    //           );
    //         }
    //         let actualData = await response.json();
    //         setData(actualData);
    //         console.log(actualData);
    //         setError(null);
    //     } catch(err) {
    //         setError(err.message);
    //         setData(null);
    //     } finally {
    //         setLoading(false);
    //     }  
    // }

    if (actualData == undefined) {
        return <Loader />
    }
    return (
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
        dataSource={actualData.data.groups}
        renderItem={(item) => (
        <List.Item
            key={item.group_name}
            onClick={() => console.log(item.group_id)}
        >
            <List.Item.Meta
            avatar={<TeamOutlined />}
            title={<a href={item.href}>{item.group_name}</a>}
            description={item.group_description}
            />
            Group owner:{"\t"}
            {item.group_owner}
        </List.Item>
        )}
    />
    )
};

export default Group;
import { React, useState, useEffect }  from 'react';
import { LikeOutlined, MessageOutlined, StarOutlined, UserOutlined } from '@ant-design/icons';
import { Avatar, List, Space } from 'antd';
import TopTab from './TopTab';
import Loader from '../../components/Loader';

const data2 = [
  {
    "person_id": 1,
    "person_name": "Stanley",
    "self_description": "balabala"
  },
  {
    "person_id": 2,
    "person_name": "Angelia",
    "self_description": "lalala"
  }
]

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

const Members: React.FC = () => {
  const [actualData, setData] = useState(null);
  const [err, setError] = useState(null);
  const [loading, setLoading] = useState(false);

//   useEffect(() => {
//     fetch("http://192.168.0.132:5000/group/get_groups?limit=0&offset=100",{
//       method: "GET",
//       header: {"Content-type": "application/json"}
//     })
//     .then((res) => res.json())
//     .then((data) => setData(data));
//   }, []);

    // actualData=data2
    console.log(actualData)

    // if (actualData == undefined) {
    //     return <Loader />
    // }
    return (
      <div>
        <header className='detail__header'>
            <TopTab tab={"members"}/>
        </header>
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
        dataSource={data2}
        renderItem={(item) => (
        <List.Item
            key={item.person_name}
            onClick={() => console.log(item.person_id)}
        >
            <List.Item.Meta
            avatar={<UserOutlined />}
            title={<a href={item.href}>{item.person_name}</a>}
            description={item.self_description}
            />
            {/* Group owner:{"\t"} */}
            {/* {item.group_owner} */}
        </List.Item>
        )}
    />
    </div>
    )
};

export default Members;
import {React, useState}  from 'react';
import { ScheduleOutlined, TeamOutlined, EditOutlined, FileAddOutlined } from '@ant-design/icons';
import { Tabs, Button } from 'antd';
import { useNavigate } from 'react-router-dom'
import Icon from '@ant-design/icons/lib/components/Icon';
import { makeStyles } from "@material-ui/core/styles";
import {
  Grid,
  Card,
  CardContent,
  Typography,
  CardHeader,
  CardActionArea
} from "@material-ui/core/";
import EditPopUp from './EditPopUp';
import AddPopUp from './AddPopUp';
import TopTab from './TopTab';
import './GroupDetail.css'

// const TopTab: React.FC = () => {
//   let history = useNavigate();

//   const handleTabClick = (key) => {
//     history.push(`/${key}`)
//   }
//   return (
//     <Tabs
//       onChange={(key) => {
//         history(`/group_mgmt/${key}`);
//       }}
//       defaultActiveKey="plans"
//       items={
//         [
//           {
//             label: (
//               <span>
//                 <ScheduleOutlined />
//                 Study Plan
//               </span>
//             ),
//             key: "plans",
//           },
//           {
//             label: (
//               <span>
//                 <TeamOutlined />
//                 Group Members
//               </span>
//             ),
//             key: "members",
//           }
//         ]
//       }
//     />
//   )
// };

const StudyPlan = ( {data} ) => {
  const [visible, setVisible] = useState(false);
  // open popup
  const showModal = () => {
    setVisible(true);
  };

  return (
    <Card>
      <div className='card__header'>
        <CardHeader
          title={`${data.event_name}`}
          subheader={`Event Description : ${data.event_description}`}
        />
        <>
          <EditOutlined style={{ fontSize:"120%" }} onClick={showModal} />
          <EditPopUp visible={visible} setVisible={setVisible} data={data}/>
        </>
      </div>
      <CardContent>
      <div>
        <Typography>Event Holder: {data.event_holder}</Typography>
        <Typography>Location: {data.location}</Typography>
        <Typography
          color="textSecondary"
          gutterBottom
        >
          {data.start_time} - {data.end_time}
        </Typography>
      </div>
      </CardContent>
    </Card>
  )
};

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    padding: theme.spacing(2)
  }
}));

const StudyPlanList = () => {
  const classes = useStyles();
  const data = {
    name: [
      {event_name: "Study plan 1", event_holder: "Stanley", event_description: "balabala", location: "utown", start_time: "00:00", end_time: "11:11"}
    ],
    id: [1, 2, 3, 4]
  };

  const [visible, setVisible] = useState(false);
  // open popup
  const showModal = () => {
    setVisible(true);
  };

  return (
    <div className={classes.root}>
        <Grid
          container
          spacing={2}
          direction="row"
          justify="flex-start"
          alignItems="flex-start"
        >
          {data.name.map(function (elem) {
            return(
              <Grid item xs={3} key={data.name.indexOf(elem)}>
                <StudyPlan data={elem}></StudyPlan>
              </Grid>
            )
          })}
        </Grid>
    </div>
  );
};

const GroupDetail = () => {
  const [addVisible, setAddVisible] = useState(false);
  // open popup
  const showAddModal = () => {
    setAddVisible(true);
  };
  return (
    <div>
      <header className='detail__header'>
        <TopTab tab={"plans"}/>
        <FileAddOutlined style={{fontSize: "150%"}} onClick={showAddModal}/>
      </header>
      <AddPopUp setAddVisible={setAddVisible} addVisible={addVisible}/>
      <StudyPlanList />
    </div>
  )
};

export default GroupDetail;
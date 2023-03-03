import {React, useState}  from 'react';
import { ScheduleOutlined, TeamOutlined, EditOutlined } from '@ant-design/icons';
import { Tabs, Button } from 'antd';
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
import './GroupDetail.css'

const TopTab: React.FC = () => {
  return (
      <Tabs
  defaultActiveKey="1"
  items={
    [
      {
        label: (
          <span>
            <ScheduleOutlined />
            Study Plan
          </span>
        ),
        key: "1",
      },
      {
        label: (
          <span>
            <TeamOutlined />
            Group Members
          </span>
        ),
        key: "2",
      }
    ]
  }
/>
  )
};

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
          title={`Plan Name : ${data.event_name}`}
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
  
  return (
    <div>
      <TopTab />
      <StudyPlanList />
    </div>
  )
};

export default GroupDetail;
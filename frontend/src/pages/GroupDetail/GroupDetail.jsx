import {React, useState}  from 'react';
import { ScheduleOutlined, TeamOutlined } from '@ant-design/icons';
import { Tabs } from 'antd';
import Icon from '@ant-design/icons/lib/components/Icon';
import { makeStyles } from "@material-ui/core/styles";
import {
  Grid,
  Card,
  CardContent,
  Typography,
  CardHeader
} from "@material-ui/core/";

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

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    padding: theme.spacing(2)
  }
}));

const StudyPlan = () => {
  const classes = useStyles();
  const data = {
    name: [
      { quarter: 1, earnings: 13000 },
      { quarter: 2, earnings: 16500 },
      { quarter: 3, earnings: 14250 },
      { quarter: 4, earnings: 19000 },
      { quarter: 5, earnings: 19000 }
    ],
    id: [1, 2, 3, 4]
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
          {data.name.map((elem) => (
            <Grid item xs={3} key={data.name.indexOf(elem)}>
              <Card>
                <CardHeader
                  title={`quarter : ${elem.quarter}`}
                  subheader={`earnings : ${elem.earnings}`}
                />
                <CardContent>
                  <Typography variant="h5" gutterBottom>
                    Hello World
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
    </div>
  );
}

const GroupDetail = () => {
  return (
    <div>
      <TopTab />
      <StudyPlan />
    </div>
  )
};

export default GroupDetail;
import {React, useState, useEffect}  from 'react';
import { 
  TeamOutlined, 
  EditOutlined, 
  FileAddOutlined, 
  DeleteOutlined, 
  ReadFilled, 
  UserOutlined, 
  HomeFilled, 
  EnvironmentFilled, 
  ApartmentOutlined,
  ClockCircleFilled,
  EllipsisOutlined,
  SettingOutlined,
  PlusCircleTwoTone
} from '@ant-design/icons';
import { Tabs, Button, Tag, Tooltip, Descriptions } from 'antd';
import { useNavigate, useParams, Link } from 'react-router-dom';
import axios from 'axios';
import Icon from '@ant-design/icons/lib/components/Icon';
import { makeStyles } from "@material-ui/core/styles";
import dayjs from 'dayjs';
import customParseFormat from 'dayjs/plugin/customParseFormat';
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
import DeletePopUp from './DeletePopUp';
import './GroupDetail.css';
import Loader from '../../components/Loader';
import cookie from 'react-cookies';

const { Meta } = Card;

dayjs.extend(customParseFormat)
dayjs.tz.setDefault("Asia/Singapore")
dayjs.extend(customParseFormat)

const showTimeFormat = 'YYYY-MM-DD HH:mm';
const sessionID = cookie.load("session_id");

const config = {
  headers: { Authorization: `Bearer ${sessionID}` }
};

const StudyPlan = ( {data} ) => {
  const [visible, setVisible] = useState(false);
  const [deleteVisible, setDeleteVisible] = useState(false);
  // open popup
  const showModal = () => {
    setVisible(true);
  };

  const showDeleteModal = () => {
    setDeleteVisible(true);
  }
  
  return (
    <Card style={{overflow:"scroll", height:"450px"}}>
      <div className='card__header' style={{height:"5%"}}>
        {(data.is_deleted != 1) && <div className='edit__plan'>
          <Tooltip title="Edit Study Plan">
            <span><EditOutlined style={{ fontSize:"120%" }} onClick={showModal} /></span>
          </Tooltip>
          <EditPopUp visible={visible} setVisible={setVisible} data={data}/>
        </div>}
        {(data.is_deleted != 1) && <div className='delete__plan'>
          <Tooltip title="Cancel Study Plan">
            <span><DeleteOutlined style={{ fontSize:"120%" }} onClick={showDeleteModal} /></span>
          </Tooltip>
          <DeletePopUp visible={deleteVisible} setVisible={setDeleteVisible} data={data}/>
        </div>}
        <Tooltip title="This event was canceled">{(data.is_deleted == 1) && <Tag color="red">Canceled</Tag>}</Tooltip>
        <Tooltip title="You are already in this event">{(data.is_a_member == 1) && <Tag color="blue">Joined</Tag>}</Tooltip>
      </div>
      <CardHeader
        title={
          <Link to={`/group_detail/plan_detail/${data.event_id}`} >
            <a>{data.event_name}</a>
          </Link>
          }
        subheader={`${data.event_description}`}
        style={{height:"40%"}}
      />
      <CardContent style={{height:"55%"}}>
      <div>
        <Typography>
          <UserOutlined />{"\t"}Event Holder:{"\t"} 
          {data.event_holder.first_name + " " + data.event_holder.last_name}
        </Typography>
        <Typography>
          <EnvironmentFilled />{"\t"}Location: {"\t"}{data.location}
        </Typography>
        <Typography>
          <ApartmentOutlined />{"\t"}Capacity: {"\t"}{data.capacity}
        </Typography>
        <p/>
        <Typography
          color="textSecondary"
          gutterBottom
        >
          <ClockCircleFilled />{"\t"}
          {dayjs(data.start_time).format(showTimeFormat)} - {dayjs(data.end_time).format(showTimeFormat)}
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

const StudyPlanList = ( {groupId} ) => {
  const classes = useStyles();
  const [planList, setPlanlist] = useState(null);
  const [cachedData, setCachedData] = useState(null);
  const [addVisible, setAddVisible] = useState(false);

  const showAddModal = () => {
    setAddVisible(true);
  };

  useEffect(() => {
    if (cachedData) {
      setPlanlist(cachedData);
      return;
    }
    const fetchData = async () => {
      const res = await axios.get(
        `${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/group_detail/get_study_plan_by_group/${groupId}?limit=0&offset=10&show_deleted=true&order_by=is_deleted`,
        config
      );
      setPlanlist(res.data.data.study_plan);
      setCachedData(res.data.data.study_plan);
      console.log(res.data.data.study_plan)
    };
    fetchData();
  }, []);

  const [visible, setVisible] = useState(false);
  // open popup
  const showModal = () => {
    setVisible(true);
  };

  if (planList == undefined) {
    return <Loader/>
  }

  if (planList.length == 0) {
    return <Typography>No Data Available</Typography>
  }

  return (
    <div className={classes.root}>
      <header className='detail__header' style={{display:"flex", justifyContent:"flex-end"}}>
        <Button onClick={showAddModal} type="primary">
        <PlusCircleTwoTone style={{fontSize: "120%"}} /> Create Your Study Plan!</Button>
      </header>
      <AddPopUp setAddVisible={setAddVisible} addVisible={addVisible} groupId={groupId}/>
      <Grid
        container
        spacing={3}
        direction="row"
        justify="flex-start"
        alignItems="flex-start"
      >
        {planList.map(function (elem) {
          return(
            <Grid item xs={4} key={planList.indexOf(elem)}>
              <StudyPlan data={elem}></StudyPlan>
            </Grid>
          )
        })}
      </Grid>
    </div>
  );
};

const GroupDetail = ( props ) => {
  const [addVisible, setAddVisible] = useState(false);
  const [groupOverview, setGroupOverview] = useState({});
  const params = useParams();
  const groupId = params.id;
  // open popup
  const showAddModal = () => {
    setAddVisible(true);
  };

  useEffect(() => {
    const fetchData = async () => {
      const res = await axios.get(
        `http://192.168.0.132:5000/group/get_groups?limit=0&offset=100&group_id=${groupId}`,
        config
      );
      setGroupOverview(res.data.data.groups[0]);
      console.log(groupOverview);
    };
    fetchData();
  }, []);

  return (
    <div style={{overflow:"scroll", height:"1000px"}}>
      <header className='detail__header'>
        <TopTab tab={"plans"} groupId={groupId}/>
      </header>
      <StudyPlanList groupId={groupId}/>
    </div>
  )
};

export default GroupDetail;

import { Button, Checkbox, Form, Input } from 'antd';
import { Link, useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import {cookie} from 'react-cookies';
import { useCookies } from 'react-cookie';

const Login = () => {
  const [cookies, setCookie] = useCookies(['myCookie']);

  const onFinish = (values) => {
    const requestBody = {
        identifier: values.username,
        password: values.password
      }
      axios.post(`${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/login/auth`, requestBody)
        .then((response) => {
        //   console.log('Post created successfully!', response.data);
          window.location.reload(false);
          console.log(response.data.data.token);
          setCookie('session_id', `${response.data.data.token}`, { path: '/' });
          alert("Login Successfully.")
        })
        .catch((error) => {
          console.error('Error authenticating user', error);
        });
  };
  
  const onFinishFailed = (errorInfo) => {
    alert('Error authenticating user:', errorInfo);
  };

  return(
  <Form
    name="basic"
    labelCol={{
      span: 8,
    }}
    wrapperCol={{
      span: 16,
    }}
    style={{
      maxWidth: 600,
    }}
    onFinish={onFinish}
    onFinishFailed={onFinishFailed}
    autoComplete="off"
  >
    <Form.Item
      label="Username"
      name="username"
      rules={[
        {
          required: true,
          message: 'Please input your username!',
        },
      ]}
    >
      <Input />
    </Form.Item>

    <Form.Item
      label="Password"
      name="password"
      rules={[
        {
          required: true,
          message: 'Please input your password!',
        },
      ]}
    >
      <Input.Password />
    </Form.Item>

    <Form.Item
      wrapperCol={{
        offset: 8,
        span: 16,
      }}
    >
      <Button type="primary" htmlType="submit">
        Submit
      </Button>
    </Form.Item>
    <Form.Item  style={{display:"flex", justifyContent:"flex-end"}}>
        <Link to={`/register`}>
            <a>Register</a >
        </Link>
    </Form.Item>
  </Form>)
};

export default Login;

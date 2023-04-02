import { Button, Checkbox, Form, Input, message } from 'antd';
import { Link, useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import cookie from 'react-cookies';


// const sessionID = cookie.load("session_id");
// const config = {
//     headers: { Authorization: `Bearer ${sessionID}` }
// };
const onFinish = (values) => {
  console.log('Success:', values);
  const requestBody = {
    user_name: values.username,
    password: values.password,
    major: values.major,
    email: values.email,
    description: values.description,
    first_name: values.first_name,
    last_name: values.last_name,
    student_id: values.student_id
  }
  axios.post(`${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/register/create_user`, requestBody)
    .then((response) => {
      console.log('Post created successfully!', response.data);
    //   setVisible(false);
      window.location.reload(false);
      alert("Register Successfully. Please check your email.")
    })
    .catch((error) => {
      console.error('Error creating user', error);
    });

};

const onFinishFailed = (errorInfo) => {
  console.log('Failed:', errorInfo);
};
const Register = () => (
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
      label="Major"
      name="major"
      rules={[
        {
          required: false,
          message: 'Please input your major!',
        },
      ]}
    >
      <Input />
    </Form.Item>

    <Form.Item
      label="Email"
      name="email"
      rules={[
        {
          required: true,
          message: 'Please input your email!',
        },
      ]}
    >
      <Input />
    </Form.Item>

    <Form.Item
      label="Description"
      name="description"
      rules={[
        {
          required: false,
          message: 'Please input your description!',
        },
      ]}
    >
      <Input />
    </Form.Item>

    <Form.Item
      label="First Name"
      name="first_name"
      rules={[
        {
          required: true,
          message: 'Please input your description!',
        },
      ]}
    >
      <Input />
    </Form.Item>

    <Form.Item
      label="Last Name"
      name="last_name"
      rules={[
        {
          required: true,
          message: 'Please input your description!',
        },
      ]}
    >
      <Input />
    </Form.Item>

    <Form.Item
      label="Student ID"
      name="student_id"
      rules={[
        {
          required: true,
          message: 'Please input your student id!',
        },
      ]}
    >
      <Input />
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
        <Link to={`/login`}>
            <a>Login</a >
        </Link>
    </Form.Item>
  </Form>
);
export default Register;

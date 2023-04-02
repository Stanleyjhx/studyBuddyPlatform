import { react, useState, useEffect } from 'react';
import { Form, Input, Modal, Select, TimePicker, DatePicker, Button, Space, InputNumber } from 'antd';
import dayjs from 'dayjs'
import customParseFormat from 'dayjs/plugin/customParseFormat';
import timezone from 'dayjs/plugin/timezone'
import axios from 'axios';
import moment from 'moment';
import cookie from 'react-cookies';

dayjs.extend(customParseFormat)
dayjs.extend(timezone)

dayjs.tz.setDefault("Asia/Singapore")

const sessionID = cookie.load("session_id")
const showTimeFormat = 'YYYY-MM-DD HH:mm'

const EditProfilePopUp = ({ visible, setVisible, data }) => {
    const [form] = Form.useForm();
    const [buttonDisabled, setButtonDisabled] = useState(true);

    const transformDateObject = (obj) => {
      return {
        ...obj,
        start_time: moment(obj.start_time),
        end_time: moment(obj.end_time),
      };
    }

    const onCapacityChange = (value: number) => {
      console.log('changed', value);
    };

    const config = {
      headers: { Authorization: `Bearer ${sessionID}` }
    };
    

    const handleOk = () => {
      // handle form submission here
      form.validateFields().then((values) => {
        // customize post body
        const requestBody = {
          edit_type: 2,
          edit_contents: {
            user_name : values.user_name,
            first_name : values.first_name,
            last_name : values.last_name,
            email : values.email,
            description : values.description,
            major: values.major
          }
        }
        console.log(requestBody.sra)
        axios.post(`${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/personal-info/edit_personal_info`, requestBody, config)
          .then((response) => {
            console.log('Post created successfully!', response.data);
            setVisible(false);
            form.resetFields();
            window.location.reload(false)
          })
          .catch((error) => {
            console.error('Error editing study plan', error);
          });
      })
    };

    const handleCancel = () => {
      setVisible(false);
    };

    const handleDeleteForm = () => {
      return;
    }
    
    
    return (
      <div>
        <Modal 
          wrapClassName="modal-wrap"
          okText="Confirm"
          cancelButtonProps={{ shape: 'round' }}
          okButtonProps={{ shape: 'round' }}
          width={600}
          visible={visible}
          title="Edit Personal Profile" 
          onCancel={handleCancel}
          autoFocusButton="OK" 
          onOk={handleOk}
          okButtonProps={{ disabled:  buttonDisabled  }}
        >
          <div className="form">
            <Form 
              form={form} 
              labelCol={{ span: 5 }} 
              wrapperCol={{ span: 16 }} 
              initialValues={data} 
              onFieldsChange={() =>
                setButtonDisabled(
                  form.getFieldsError().some((field) => field.errors.length > 0)
                )
              }
            >
              <Form.Item
                label="User Name"
                name="user_name"
                rules={[
                  { required: false, message: 'Please input user name!' },
                  {
                    max: 100,
                    message: "User name should be less than 100 character",
                  },
                ]}
              >
                <Input maxLength={25}/>
              </Form.Item>
              <Form.Item
                label="First Name"
                name="first_name"
                rules={[
                  { required: false, message: 'Please input first name!' },
                  {
                    max: 100,
                    message: "First name should be less than 100 character",
                  },
                ]}
              >
                <Input maxLength={50}/>
              </Form.Item>
              <Form.Item
                label="Last Name"
                name="last_name"
                rules={[
                    { required: false, message: 'Please input last name!' },
                    {
                        max: 100,
                        message: "Last name should be less than 100 character",
                    },
                ]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                label="Description"
                name="description"
                rules={[
                    { required: false, message: 'Please input event name!' },
                    {
                      max: 149,
                      message: "Event name should be less than 150 character",
                    },
                  ]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                label="Major"
                name="major"
                rules={[{ required: false, message: 'Please input major!' }]}
              >
                <Input /> 
              </Form.Item>
              <Form.Item
                label="Email"
                name="email"
                rules={[{ required: false, message: 'Please input email!' }]}
              >
                <Input type="email" /> 
              </Form.Item>
              
            </Form>
          </div>
        </Modal>
      </div>
    )
};

export default EditProfilePopUp;
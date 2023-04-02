import { react, useState } from 'react';
import { Form, Input, Modal, Select, TimePicker, DatePicker, Button, InputNumber } from 'antd';
import dayjs from 'dayjs'
import customParseFormat from 'dayjs/plugin/customParseFormat';
import timezone from 'dayjs/plugin/timezone'
import axios from 'axios';
import moment from 'moment';
import cookie from 'react-cookies';

const { RangePicker } = DatePicker;
dayjs.extend(customParseFormat)
dayjs.extend(timezone)
dayjs.tz.setDefault("Asia/Singapore")

const sessionID = cookie.load("session_id")
const showTimeFormat = 'YYYY-MM-DD HH:mm'

const AddPopUp = ({ addVisible, setAddVisible, groupId}) => {
    const [form] = Form.useForm();
    const config = {
      headers: { Authorization: `Bearer ${sessionID}` }
    };
    const onCapacityChange = (value: number) => {
      console.log('changed', value);
    };
    const handleOk = () => {
      // handle form submission here
      form.validateFields().then((values) => {
        // customize post body
        const requestBody = {
          start_time : values.event_time[0].format(showTimeFormat),
          end_time : values.event_time[1].format(showTimeFormat),
          event_name : values.event_name,
          description : values.event_description,
          capacity : values.capacity,
          location : values.location
        }
        console.log(requestBody.start_time);
        axios.post(`${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/group_detail/create_study_plan/${groupId}`, requestBody, config)
          .then((response) => {
            console.log('Post created successfully!', response.data);
            setAddVisible(false);
            form.resetFields();
            window.location.reload(false)
          })
          .catch((error) => {
            console.error('Error editing study plan', error);
          });
      })
    };

    const handleCancel = () => {
      setAddVisible(false);
    };
    const [buttonDisabled, setButtonDisabled] = useState(true);

  
    return (
      <div>
        <Modal 
          wrapClassName="modal-wrap"
          okText="Confirm"
          cancelButtonProps={{ shape: 'round' }}
          okButtonProps={{ shape: 'round' }}
          width={600}
          visible={addVisible}
          title="Create Study Plan" 
          onCancel={handleCancel}
          autoFocusButton="OK" 
          onOk={handleOk}
        >
         <div className="form">
            <Form 
              form={form} 
              labelCol={{ span: 5 }} 
              wrapperCol={{ span: 16 }} 
              onFieldsChange={() =>
                setButtonDisabled(
                  form.getFieldsError().some((field) => field.errors.length > 0)
                )
              }
            >
              <Form.Item
                label="Event Name"
                name="event_name"
                rules={[
                  { required: true, message: 'Please input event name!' },
                  {
                    max: 24,
                    message: "Event name should be less than 25 character",
                  },
                ]}
              >
                <Input maxLength={25}/>
              </Form.Item>
              <Form.Item
                label="Description"
                name="event_description"
                rules={[
                  { required: true, message: 'Please input description!' },
                  {
                    max: 149,
                    message: "Description should be less than 150 character",
                  },
                ]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                label="Capacity"
                name="capacity"
              
              >
                <InputNumber min={1} max={1000} defaultValue={10} onChange={onCapacityChange} />
              </Form.Item>
              <Form.Item
                label="Location"
                name="location"
                rules={[{ required: true, message: 'Please input location!' }]}
              >
                <Input />
              </Form.Item>
             
              <Form.Item
                label="Event time"
                name="event_time"
                rules={[{ required: true, message: 'Please input event time!' }]}
              >
                <RangePicker showTime /> 
              </Form.Item>
            </Form>
          </div>
        </Modal>
      </div>
    )
};

export default AddPopUp;

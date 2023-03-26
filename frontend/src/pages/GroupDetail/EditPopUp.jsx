import { react, useState, useEffect } from 'react';
import { Form, Input, Modal, Select, TimePicker, DatePicker, Button, Space, InputNumber } from 'antd';
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

const EditPopUp = ({ visible, setVisible, data }) => {
    const [form] = Form.useForm();
    const [initialValues, setInitialValues] = useState();
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
    
    // call api get study plan by id
    useEffect(() => {
      const fetchData = async () => {
        const res = await axios.get(
          `${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/group_detail/get_study_plan_by_id/${data.event_id}`,
          config
        );
      };
      data["showDateDefault"] = [dayjs(data.start_time), dayjs(data.end_time)]

      setInitialValues(data);
    }, []); 

    const handleOk = () => {
      // handle form submission here
      form.validateFields().then((values) => {
        // customize post body
        const requestBody = {
          edit_type: 2,
          edit_contents: {
            start_time : values.showDateDefault[0].format(showTimeFormat),
            end_time : values.showDateDefault[1].format(showTimeFormat),
            event_name : values.event_name,
            event_description : values.event_description,
            location : values.location,
            capacity: values.capacity
          }
        }
        console.log(requestBody.sra)
        axios.post(`${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/group_detail/edit_study_plan/${data.event_id}`, requestBody, config)
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
          title="Edit Study Plan" 
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
              initialValues={initialValues} 
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
                  { required: false, message: 'Please input event name!' },
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
                  { required: false, message: 'Please input description!' },
                  {
                    max: 149,
                    message: "Description should be less than 150 character",
                  },
                ]}
              >
                <Input maxLength={50}/>
              </Form.Item>
              <Form.Item
                label="Location"
                name="location"
                rules={[{ required: false, message: 'Please input location!' }]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                label="Capacity"
                name="capacity"
                rules={[{ required: false, message: 'Please input capacity!' }]}
              >
                <InputNumber min={1} max={1000} defaultValue={10} onChange={onCapacityChange} />
              </Form.Item>
              <Form.Item
                label="Event time"
                name="showDateDefault"
                rules={[{ required: false, message: 'Please input event time!' }]}
              >
                <RangePicker showTime /> 
              </Form.Item>
              
            </Form>
          </div>
        </Modal>
      </div>
    )
};

export default EditPopUp;
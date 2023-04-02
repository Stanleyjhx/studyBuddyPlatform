import { react, useState } from 'react';
import { Form, Input, Modal, Select, TimePicker, DatePicker, Button, InputNumber } from 'antd';
import dayjs from 'dayjs'
import customParseFormat from 'dayjs/plugin/customParseFormat';
import timezone from 'dayjs/plugin/timezone'
import axios from 'axios';
import moment from 'moment';
import cookie from 'react-cookies';

const sessionID = cookie.load("session_id")

const RejectPopUp = ({ visible, setVisible, data}) => {
    const [form] = Form.useForm();
    const config = {
      headers: { Authorization: `Bearer ${sessionID}` }
    };
    const handleOk = () => {
      // handle form submission here
      form.validateFields().then((values) => {
        // customize post body
        const requestBody = {
          status: -1
        };
        axios.post(`${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/invitation/approve/${data}`, requestBody, config)
          .then((response) => {
            console.log('Post created successfully!', response.data);
            setVisible(false);
            form.resetFields();
            window.location.reload(false)
          })
          .catch((error) => {
            console.error('Error reject the invitation', error);
          });
      })
    };

    const handleCancel = () => {
      setVisible(false);
    };
    const [buttonDisabled, setButtonDisabled] = useState(true);

    return (
      <div>
        <Modal
        title={`Are you sure you want to reject this invitation?`}
        visible={visible}
        onOk={handleOk}
        onCancel={handleCancel}
        okButtonProps={{ danger: true }}
        >
          <p>This action cannot be undone.</p>
        </Modal>
      </div>
    )
};

export default RejectPopUp;
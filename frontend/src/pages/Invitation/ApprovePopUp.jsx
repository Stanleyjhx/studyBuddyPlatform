import { react, useState } from 'react';
import { Form, Input, Modal, Select, TimePicker, DatePicker, Button, InputNumber } from 'antd';
import dayjs from 'dayjs'
import customParseFormat from 'dayjs/plugin/customParseFormat';
import timezone from 'dayjs/plugin/timezone'
import axios from 'axios';
import moment from 'moment';
import cookie from 'react-cookies';

const sessionID = cookie.load("session_id")

const ApprovePopUp = ({ visible, setVisible, data}) => {
    const [form] = Form.useForm();
    const config = {
      headers: { Authorization: `Bearer ${sessionID}` }
    };
    const handleOk = () => {
      form.validateFields().then((values) => {
        const requestBody = {
          status: 1
        }
        axios.post(`${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/invitation/approve/${data}`, requestBody, config)
          .then((response) => {
            setVisible(false);
            form.resetFields();
            window.location.reload(false)
          })
          .catch((error) => {
            console.error('Error approve the invitation', error);
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
        title={`Are you sure you want to approve this invitation?`}
        visible={visible}
        onOk={handleOk}
        onCancel={handleCancel}
        >
          <p>This action cannot be undone.</p>
        </Modal>
      </div>
    )
};

export default ApprovePopUp;

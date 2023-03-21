import { react, useState } from 'react';
import { Form, Input, Modal, Select, TimePicker, DatePicker, Button } from 'antd';

const AddPopUp = ({ addVisible, setAddVisible }) => {
    const [form] = Form.useForm();

    const handleOk = () => {
      // handle form submission here
      setAddVisible(false);
    };

    const handleCancel = () => {
      setAddVisible(false);
    };
    // // 提交后获取表单数据，请求接口，重置表单并关闭
    const onSubmit = (values) => {
      try {
        const response =  fetch("https://baidu.com", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(values),
        });
        if (response.status != 200) {
          throw new Error('Failed to create study plan');
          alert("Create study plan failed")
        }

        setAddVisible(false);
      } catch (err) {
        console.error(err);
        alert(err);
      }
    };
  
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
            <Form form={form} labelCol={{ span: 5 }} wrapperCol={{ span: 16 }} onFinish={onSubmit}>
              <Form.Item
                label="Event Name"
                name="eventname"
                rules={[{ required: true, message: 'Please input event name!' }]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                label="Description"
                name="eventdesc"
                rules={[{ required: true, message: 'Please input description!' }]}
              >
                <Input />
              </Form.Item>
              <Form.Item
                label="Location"
                name="depart"
                rules={[{ required: true, message: 'Please input location!' }]}
              >
                <Select>
                  <Select.Option value={1}>Science Library</Select.Option>
                  <Select.Option value={2}>Utown</Select.Option>
                  <Select.Option value={3}>Central Library</Select.Option>
                </Select>
              </Form.Item>
              <Form.Item
                label="Date"
                name="end"
                rules={[{ required: true, message: 'Please input end time!' }]}
              >
                <DatePicker />
              </Form.Item>
              <Form.Item
                label="Start-time"
                name="start"
                rules={[{ required: true, message: 'Please input start time!' }]}
              >
                <TimePicker format={'HH:mm'}/>
              </Form.Item>
              <Form.Item
                label="End-time"
                name="end"
                rules={[{ required: true, message: 'Please input end time!' }]}
              >
                <TimePicker format={'HH:mm'}/>
              </Form.Item>
            </Form>
          </div>
        </Modal>
      </div>
    )
};

export default AddPopUp;
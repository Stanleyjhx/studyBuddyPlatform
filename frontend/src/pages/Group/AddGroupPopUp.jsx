import { react, useState, useEffect } from 'react';
import { Form, Input, Modal, Select, TimePicker, DatePicker, Button, Tag } from 'antd';
import axios from 'axios';
import cookie from 'react-cookies';

const AddGroupPopUp = ({ addVisible, setAddVisible }) => {
  const [form] = Form.useForm();
  const sessionID = cookie.load("session_id");
  const config = {
    headers: { Authorization: `Bearer ${sessionID}` }
  };

  const handleOk = () => {
    // handle form submission here
    form.validateFields().then((values) => {
      // customize post body
      const requestBody = {
        group_name: values.group_name,
        group_description: values.group_description,
        module_tags: values.module_tags.toString()
      };

      axios.post(`${process.env.REACT_APP_BACKEND_URL}:${process.env.REACT_APP_BACKEND_PORT}/group/create_group`, requestBody, config)
        .then((response) => {
          console.log('Post created successfully!', response.data);
          setAddVisible(false);
          form.resetFields();
          window.location.reload(false);
        })
        .catch((error) => {
          console.error('Error editing study plan', error);
        });
    })
  };

  const handleCancel = () => {
    setAddVisible(false);
  };

  const courseOptions = [
    {value: 'DSA5101'},
    {value: 'DSA5103'},
    {value: 'DSA5104'},
    {value: 'DSA5201'},
    {value: 'DSA5105'},
    {value: 'CS5224'},
    {value: 'CS4228'},
    {value: 'CS5344'},
  ]

  const tagRender = (props) => {
    const { label, value, closable, onClose } = props;
    const onPreventMouseDown = (event) => {
      event.preventDefault();
      event.stopPropagation();
    };
    return (
      <Tag
        onMouseDown={onPreventMouseDown}
        closable={closable}
        onClose={onClose}
        style={{
          marginRight: 3,
        }}
      >
        {label}
      </Tag>
    );
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
          title="Create Study Group" 
          onCancel={handleCancel}
          autoFocusButton="OK" 
          onOk={handleOk}
      >
        <div className="form">
          <Form form={form} labelCol={{ span: 5 }} wrapperCol={{ span: 16 }}>
            <Form.Item
              label="Group Name"
              name="group_name"
              rules={[
                { required: true, message: 'Please input group name!' },
                {
                  max: 29,
                  message: "Group name should be less than 30 character",
                },
              ]}
            >
              <Input maxLength={30}/>
            </Form.Item>
            <Form.Item
              label="Description"
              name="group_description"
              rules={[
                { required: true, message: 'Please input description!'},
                {
                  max: 149,
                  message: "Group name should be less than 150 character",
                },
              ]}
            >
              <Input maxLength={150}/>
            </Form.Item>
            <Form.Item
              label="Modules"
              name="module_tags"
            >
              <Select 
                mode='multiple' 
                showArrow
                tagRender={tagRender}
                options={courseOptions}
                style={{
                  width: '100%',
                }}
              />
            </Form.Item>
          </Form>
        </div>
      </Modal>
    </div>
  );
};

export default AddGroupPopUp;

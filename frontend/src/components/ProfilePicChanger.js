import React, { useState } from 'react'
import 'antd/dist/antd.css' 
import { Modal, Button } from 'antd';


const ProfilePicChanger = (props) => {
    const [visible, setVisible] = useState(false);
    return (
      <>
      <div classname="d-flex align-items-center justify-content-center">
        <Button type="primary" onClick={() => setVisible(true)}>
            Change Photo
        </Button>
        </div>
        <Modal
          title="Change Photo"
          centered
          visible={visible}
          onOk={() => setVisible(false)}
          onCancel={() => setVisible(false)}
          width={1000}
        >
          <p>some contents...</p>
          <p>some contents...</p>
          <p>some contents...</p>
        </Modal>
      </>
  
    );
}


export default ProfilePicChanger

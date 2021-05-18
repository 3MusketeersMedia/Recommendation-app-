import React, { useState } from 'react';
import 'antd/dist/antd.css' 
import '../pages/profilePage.css'
import { Modal } from 'antd';

const MediaModal = (props) => {
  const [visible, setVisible] = useState(false);
  return (
    <>
      <div className="d-inline-block border border-secondary rounded-top MediaModalImage" style={{height: "100%"}} onClick={() => setVisible(true)}>
        <img src={props.image} alt="Media Card image"
        className="img-responsive img-thumbnail rounded mx-auto" alt="Responsive image" onClick={() => setVisible(true)}/>
        <p className="text-justify text-center font-weight-bold p-3 mb-2 bg-light text-dark">{props.title}</p>
      </div>
      
      <Modal 
        title={props.title}
        centered
        visible={visible}
        onOk={() => setVisible(false)}
        onCancel={() => setVisible(false)}
        width={1500}
        bodyStyle={{maxHeight:"700px", overflow:"scroll", textAlign:"center",}}
        style={{display:"inline-block"}}
      >
         {props.list}
      </Modal>
    </>
  );
};

export default MediaModal
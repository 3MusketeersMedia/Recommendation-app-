import React from 'react'
import 'antd/dist/antd.css' 
import { Avatar } from 'antd'
import { UserOutlined } from '@ant-design/icons';


const ProfilePicture = (props) => {
    return (
        <div className='center m-3 p-3'>
            <Avatar size={128} icon={<UserOutlined />} src={props.picture} />
        </div>
    )
}

export default ProfilePicture

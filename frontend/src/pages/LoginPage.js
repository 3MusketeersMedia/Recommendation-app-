import React from 'react';
import {Container, Jumbotron, Form, Button} from 'react-bootstrap';
import {AppContext} from '../AppContext'; 
import './LoginPage.css';

export default class LoginPage extends React.Component {
  static contextType = AppContext; 
  constructor() {
    super();
    this.state = {
      newUser: false
    };
    this.username = React.createRef();
    this.password = React.createRef();
    this.confirm = React.createRef();
  }
  toggleNewUser = () => {
    this.setState({newUser: !this.state.newUser});
  }
  submitForm = async(e) => {
    e.preventDefault();
    const username = this.username.current.value;
    const password = this.password.current.value;
    if (username === '' || password === '') {
      console.log('please fill out both fields');
      return;
    }
    if (this.state.newUser) {
      const confirm = this.confirm.current.value;
      if (password !== confirm) {
        console.log('passwords must match');
        return;
      }
      console.log(`create user (${username}, ${password})`);
      this.context.actions.signup(username, password); 
    } else {
      console.log(`login user (${username}, ${password})`);
      this.context.actions.login(username, password); 
    }
  }
  render() {
    
    let token = this.context.store.token;
    // Redirects to homepage after token is set.
    if(token && token !== "" && token !== undefined)
      this.props.history.push("/");

    return (
      <Container>
        <Jumbotron className='loginFormHolder'>
          <Form onSubmit={this.submitForm}>
            <Form.Group>
              <Form.Label>username</Form.Label>
              <Form.Control placeholder='username' ref={this.username}/>
            </Form.Group>
            <Form.Group>
              <Form.Label>password</Form.Label>
              <Form.Control placeholder='password' type='password' ref={this.password}/>
            </Form.Group>
            {this.state.newUser ? (
              <Form.Group>
                <Form.Label>confirm password</Form.Label>
                <Form.Control placeholder='confirm password' type='password' ref={this.confirm}/>
              </Form.Group>
            ) : ''}
            <div className='loginButtons'>
              <Button type='submit'>Submit</Button>
              <Button onClick={this.toggleNewUser} type='button'>
                {this.state.newUser ? 'Existing user? Log in' : 'New user? Sign up'}
              </Button>
            </div>
          </Form>
        </Jumbotron>
      </Container>
    );
  }
}

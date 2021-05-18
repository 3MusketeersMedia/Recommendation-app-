import React from 'react';
import {Container, Jumbotron, Form, Button} from 'react-bootstrap';
import {AppContext} from '../AppContext';
import './LoginPage.css';

export default class LoginPage extends React.Component {
  static contextType = AppContext;
  constructor() {
    super();
    this.state = {
      newUser: false,
      errors: {
        username: '',
        password: '',
        confirm: ''
      }
    };
    this.username = React.createRef();
    this.password = React.createRef();
    this.confirm = React.createRef();
  }

  toggleNewUser = () => {
    console.log('toggle new user');
    this.setState({newUser: !this.state.newUser});
  }
  submitForm = async (e) => {
    e.preventDefault();
    await this.checkErrors();
    if (this.hasErrors()) return;
    const username = this.username.current.value;
    const password = this.password.current.value;
    if (this.state.newUser) {
      console.log(`create user (${username}, ${password})`);
      this.context.actions.signup(username, password)
        .then(async () => {
          const token = this.context.store.token;
          // Redirects to homepage after token is set.
          if (token) {
            this.props.history.push("/");
          } else {
            await this.setError('username', 'username taken');
          }
        });
    } else {
      console.log(`login user (${username}, ${password})`);
      this.context.actions.login(username, password)
        .then(async () => {
          const token = this.context.store.token;
          // Redirects to homepage after token is set.
          if (token) {
            this.props.history.push("/");
          } else {
            await this.setError('username', 'invalid username');
            await this.setError('password', 'invalid password');
          }
        })
    }
  }
  checkErrors = async () => {
    await this.resetErrors();
    const username = this.username.current.value;
    const password = this.password.current.value;
    if (username === '') {
      await this.setError('username', 'please fill out field');
    }
    if (password === '') {
      await this.setError('password', 'please fill out field');
    }
    if (this.state.newUser) {
      const confirm = this.confirm.current.value;
      if (password !== confirm) {
        await this.setError('confirm', 'passwords must match');
      }
    }
  }
  hasErrors = () => {
    const {username, password, confirm} = this.state.errors;
    return username !== '' || password !== '' || confirm !== '';
  }
  resetErrors = async () => {
    await this.setState({
      errors: {
        username: '',
        password: '',
        confirm: ''
      }
    });
  }
  setError = async (errorName, errorMsg) => {
    const errors = {...this.state.errors};
    errors[errorName] = errorMsg;
    await this.setState({errors});
  }
  getError = (error) => {
    if (this.state.errors[error] !== '') {
      return (
        <Form.Control.Feedback type='invalid'>
          {this.state.errors[error]}
        </Form.Control.Feedback>
      )
    }
  }
  render() {
    return (
      <Container>
        <Jumbotron className='loginFormHolder'>
          <Form onSubmit={(e) => this.submitForm(e)}>
            <Form.Group>
              <Form.Label>username</Form.Label>
              <Form.Control placeholder='username' ref={this.username}
                isInvalid={this.state.errors.username}/>
              {this.getError('username')}
            </Form.Group>
            <Form.Group>
              <Form.Label>password</Form.Label>
              <Form.Control placeholder='password' type='password' ref={this.password}
                isInvalid={this.state.errors.password}/>
              {this.getError('password')}
            </Form.Group>
            {this.state.newUser ? (
              <Form.Group>
                <Form.Label>confirm password</Form.Label>
                <Form.Control placeholder='confirm password' type='password' ref={this.confirm}
                  isInvalid={this.state.errors.confirm}/>
                {this.getError('confirm')}
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

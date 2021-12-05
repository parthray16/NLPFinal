import React, { Component } from 'react';
import axios from 'axios';
import Extraction from './Extraction';

const headerStyle = {
    color: "black", 
    backgroundColor: "IndianRed",
    textAlign: "center",
    fontSize: "200%",
    fontFamily: "verdana",
    border: "5px solid IndianRed"
  }

class EmailForm extends Component {
    constructor(props) {
      super(props);
      this.state = {
        value: 'Provide text to extract conference',
        data: []
      };
  
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    handleChange(event) {
      this.setState({value: event.target.value, data: this.state.data});
    }
  
    handleSubmit(event) {
      // call python functions here
      axios.post('http://localhost:5000/', {'text': this.state.value})
      .then((response) => {this.setState({value: 'Provide text to extract conference',
                                          data: this.state.data.concat(response.data)});});

      event.preventDefault();
      // reset state to empty after submit
      
    }
  
    render() {
      return (
        <div class='form'
            style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            }}
        >
            <form onSubmit={this.handleSubmit}>
            <h1 style={headerStyle}>Conference Email Extractor</h1>
            <label>
                <textarea align='center' rows='25' cols='75' value={this.state.value} onChange={this.handleChange} />
            </label>
            <br />
            <input type="submit" value="Extract Conference" />
            </form>
            <br />
            <Extraction data={this.state.data}/>
          </div>
      );
    }
  }

  export default EmailForm;
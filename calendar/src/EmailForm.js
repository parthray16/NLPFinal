import React, { Component } from 'react';

const headerStyle = {
    color: "black", 
    backgroundColor: "powderblue",
    textAlign: "center",
    fontSize: "200%",
    fontFamily: "verdana",
    border: "5px solid powderblue"
  }

class EmailForm extends Component {
    constructor(props) {
      super(props);
      this.state = {
        value: 'Provide text to extract conference'
      };
  
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    handleChange(event) {
      this.setState({value: event.target.value});
    }
  
    handleSubmit(event) {
      // call python functions here
      alert('Extracting Conference:\n' + this.state.value);
      event.preventDefault();
      // reset state to empty after submit
      this.setState({value: 'Provide text to extract conference'});
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
        </div>
      );
    }
  }

  export default EmailForm;
import React from 'react';

class Main extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      imageURL: 'https://heyjeffshaw.com/assets/images/about/past/music.jpg',
    };

    this.handleUploadImage = this.handleUploadImage.bind(this);
  }

  handleUploadImage(ev) {
    ev.preventDefault();

    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);
    data.append('filename', this.fileName.value);

    fetch('http://localhost:8000/upload', {
      method: 'POST',
      body: data,
    }).then((response) => {
      response.json().then((body) => {
        this.setState({ imageURL: `http://localhost:8000/${body.file}` });
      });
    });
  }

  render() {
    return (
        <div className="upload-container" >
         <form className="form" onSubmit={this.handleUploadImage}>
            <div>
            <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
            </div>
            <div>
            <input ref={(ref) => { this.fileName = ref; }} type="text" placeholder="Enter the desired name of file" />
            </div>
            <br />
            <div>
            <button>Upload</button>
            </div>
        </form>
            <img src={this.state.imageURL} alt="img" />
        </div>

    );
  }
}

export default Main;
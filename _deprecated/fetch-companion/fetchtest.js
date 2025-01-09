function postDataToRemoteHost(dataString, ipAddress, port) {
    const url = `http://${ipAddress}:${port}/endpoint`;

    // Data to be sent in the POST request
    const postData = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ "asd": "asdas" }),
      mode: 'cors',
    };
  
    // Perform the fetch
    fetch(url, postData)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.text()
      })
      .then(data => {
        console.log('POST request successful:', data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

postDataToRemoteHost("test","127.0.0.1","8080");
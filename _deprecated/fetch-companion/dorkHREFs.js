/*
Purpose:
extract all HREFs from google dorking results.
This can be useful in situations where you want to find folder paths your scanner can't find,
in order to perform a more precise folder/path enumeration

USAGE:
1. paste both functions in the browser console
2. call "dorkHREFs" in the console, specifying the ip and port with double quotes
 example: dorkHREFs("127.0.0.1","8080")

*/
function dorkHREFs(ipAddress, port) {
    const url = `http://${ipAddress}:${port}/dorkHREFs`;

    FILES = getHREFLinks()

    // Data to be sent in the POST request
    const postData = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({"data":FILES}),
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


function getHREFLinks() 
{
    // Get all the "a" tags on the page
    const anchorTags = document.getElementsByTagName('a');

    var hrefList = [];

    // Iterate through each "a" tag
    for (let i = 0; i < anchorTags.length; i++) 
    {
      const href = anchorTags[i].getAttribute('href');
      hrefList.push(href)
    }

    return hrefList;
}
  

/*
USAGE:
1. paste both functions in the browser console
2. call "dorkFiles" in the console, specifying the ip and port with double quotes
 example: dorkFiles("127.0.0.1","8080")

*/
function dorkFiles(ipAddress, port) {
    const url = `http://${ipAddress}:${port}/dorkFiles`;

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

    var extList = ["pdf","docx","doc","txt","xls","xlsx","xsl","xslx"]
    var hrefList = [];
  
    // Iterate through each "a" tag
    for (let i = 0; i < anchorTags.length; i++) 
    {
      const href = anchorTags[i].getAttribute('href');
  
      extList.forEach(element => 
      {
        if(href && href.endsWith(element))
        {
            hrefList.push(href)
        }
      });
    }

    return hrefList;
}
  

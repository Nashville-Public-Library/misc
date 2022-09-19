/* 
fetch "Now Playing" metadata from TL Icecast server
prints to browser console for testing
© Nashville Public Library
© Ben Weddle is to blame for this code
 */

function nowplaying() {

    fetch('http://npl.streamguys1.com/status.xsl') //http is much faster than https
    .then(response => response.text())
    .then(function(html) {
        var dom = new DOMParser();
        var parse = dom.parseFromString(html, "text/html"); 
        var index = 21; //index of 'current song'
        var result = parse.querySelectorAll('td')[index].textContent; //parse page for tag at index position and return textcontext field
        
        console.log(result)
    })
}
nowplaying()
setInterval(nowplaying, 30000) //1000 = 1 second
<h1>Weather Information Rest API</h1>
<p>This Weather Information API provides a bulky pile of information about wind, weather, sun, and air quality in a designated area.</p>
<p>Feel free to use this API, fork the project to deploy on own CGI or enhance the code with a pull requests. </p>
<p>Enjoy! </p>
<h2>Table of Contents</h2>
<ul>
  <li><a href="#getting-started">Getting Started</a></li>
  <li><a href="#endpoints">Endpoints</a></li>
  <li><a href="#error-handling">Error Handling</a></li>
  <li><a href="#authentication">Authentication & Rate Limiting </a></li>
  <li><a href="#version">Version & Changelog</a></li>
  <li><a href="#built-with">Built With</a></li>
  <li><a href="#license">License</a></li>
</ul>
<h2>Getting Started</h2>
<h3>How to use</h3>
<p>Easy to use, just call the API by: https://weatherinformation.info + <a href="#endpoints">Endpoints</a> </br>
</p>
<h3>How to deploy</h3>
<p>Prerequisites & Dependencies: Server should support python3. Furthermore, all needed dependencies are given in the requirements.txt file.
</p>
<h2>Endpoints</h2>
<h3>/api/current?location={LOCATION}&openweathermaps_api_key={APPID}</h3>
<p>Retrieves a list of all weatherinformations.</p>
<h4>methode</h4>
<ul>
  <li><code>GET</code></li>
</ul>
<h5>q-Parameters</h5>
<ul>
  <li><code>location</code> (required): Name of location.</li>
  <li><code>OpenWeatherMaps api key</code> (required): Your personal OpenWeatherMaps API key.</li>
</ul>
<p>Response</p>
<pre>
<code>
{
  "air": {
    "concentration": {
      "CO": 226.97,
      "NH3": 5,
      "NO": 0,
      "NO2": 4.46,
      "O3": 108.72,
      "PM10": 13.64,
      "PM2_5": 12.62,
      "SO2": 3.73
    },
    "humidity": 48,
    "pressure": 1009,
    "quality_index": 3
  },
  "api": {
    "code": 200,
    "msg": null
  },
  "location": {
    "altitute": 82.0,
    "country": "DE",
    "latitude": 52.2647,
    "longitude": 10.5236,
    "name": "Braunschweig",
    "time": {
      "dt": "09.05.2023",
      "simple": "23:46:24",
      "stamp_unix": 1683675984,
      "stamp_utc": "Tue, 09 May 2023 23:46:24 GMT",
      "zone_unix": 7200
    }
  },
  "sun": {
    "azimuth": {
      "deg": 337.98,
      "point": "North"
    },
    "elevation": {
      "deg": -17.74
    },
    "rise": {
      "dt": "09.05.2023",
      "simple": "05:33:24",
      "stamp_unix": 1683610404,
      "stamp_utc": "Tue, 09 May 2023 05:33:24 GMT",
      "zone_unix": 7200
    },
    "set": {
      "dt": "09.05.2023",
      "simple": "20:55:21",
      "stamp_unix": 1683665721,
      "stamp_utc": "Tue, 09 May 2023 20:55:21 GMT",
      "zone_unix": 7200
    }
  },
  "weather": {
    "cloudiness": 97,
    "discription": "overcast clouds",
    "temperatur": {
      "current": 13.89,
      "feel": 12.59,
      "max": 15.77,
      "min": 13.44
    },
    "visibility": 10000
  },
  "wind": {
    "direction": {
      "deg": 110,
      "point": "East"
    },
    "gust": null,
    "speed": 5.66
  }
}
</code>
</pre>

<h2>Error Handling</h2>
<p>API Error Codes:</p>
<p>Errors can be thrown internally by the server or been recieved by calling another api like openweathermaps. All Errors are displayed in the response as followed: </p>
<pre><code>
"api":{
    "code": HTTP Status Code (code),
    "msg":  HTTP Status Message (msg)
    }
</code></pre>
<table>
    <tr>
        <th>HTTP (code) </th>
        <th>HTTP (msg) </th>
        <th>Description </th>
    </tr>
    <tr>
        <td>200</td>
        <td>" "</td>
        <td>No errors occured.</td>
    </tr>
    <tr>
        <td>401</td>
        <td>"OpenWeatherMaps API Error: City not found."</td>
        <td>City not known, check for typos or try another locatiion name. </td>
    </tr>
    <tr>
        <td>402</td>
        <td>"OpenWeatherMaps API Error: API Key not accepted." </td>
        <td> OPM API key not accepted. </td>
    </tr>
</table> 
<h2>Authentication & Rate Limiting</h2>
<p>Requires a openweahtermaps API authentication (see above).</p>
<p>Does not have a rate limiting. Requests are limited to XXX calls per minute.</p>
<h2>Version & Changelog</h2>
<p>V1: 20230401 - Tested & Published </p>
<p>V2: 20230509 - added air quality, altitude & http security header</p>
<h2>Built-with</h2>
<p>flask</p>
<h2>license</h2>

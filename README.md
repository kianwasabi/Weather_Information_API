<h1>Weather Information Rest API</h1>
<p>This Weather Information API provides a bulky pile of information about wind, weather, sun, and air quality in a designated area.</p>
<p>Feel free to use this API, fork the project to deploy on own CGI or enhance the code with a pull requests. </p>
<p>Enjoy! </p>
<h2>Table of Contents</h2>
<ul>
  <li><a href="#getting-started">Getting Started</a></li>
  <li><a href="#endpoints">Endpoints</a></li>
  <li><a href="#error-handling">Error Handling</a></li>
  <li><a href="#authentication">Authentication</a></li>
  <li><a href="#rate-limiting">Rate Limiting</a></li>
  <li><a href="#version">Version</a></li>
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
<h3>/current?location={LOCATION}&openweathermaps_api_key={APPID}</h3>
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
"api":{
    "code":200,
    "msg":null
    },
 "location":{
    "country":"DE",
    "latitude":52.2667,
    "longitude":10.5333,
    "name":"Braunschweig",
    "time":{
        "dt":"07.04.2023",
        "simple":"20:10:21",
        "stamp_unix":1680898221,
        "stamp_utc":"Fri, 07 Apr 2023 20:10:21 GMT",
        "zone_unix":7200
        }
    },
"sun":{
    "azimuth":{
        "deg":284.19,
        "point":"West"
        },
        "elevation":{
            "deg":-1.38
            },
        "rise":{
            "dt":"07.04.2023", 
            "simple":"06:39:26",
            "stamp_unix":1680849566,
            "stamp_utc":"Fri, 07 Apr 2023 06:39:26 GMT",
            "zone_unix":7200
            },
        "set":{
            "dt":"07.04.2023",
            "simple":"20:00:23",
            "stamp_unix":1680897623,
            "stamp_utc":"Fri, 07 Apr 2023 20:00:23 GMT",
            "zone_unix":7200
            }
    },
"weather":{
    "cloudiness":0,
    "discription":"clear sky",
    "humidity":52,
    "pressure":1019,
    "temperatur":{
        "current":8.66,
        "feel":7.58,
        "max":9.35,
        "min":8.38},
    "visibility":10000
    },
"wind":{
    "direction":{
        "deg":60,
        "point":"Norht-East"
        },
    "gust":null,
    "speed":2.06
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
        <th>HTTP Status Code (code) </th>
        <th>HTTP Status Message (msg) </th>
        <th>Description </th>
    </tr>
    <tr>
        <td>200</td>
        <td> </td>
        <td>No errors occured.</td>
    </tr>
    <tr>
        <td>401</td>
        <td>OpenWeatherMaps API Error: City not found. </td>
        <td> </td>
    </tr>
    <tr>
        <td>402</td>
        <td>OpenWeatherMaps API Error: API Key not accepted. </td>
        <td> </td>
    </tr>
</table> 
<h2>Authentication</h2>
<p>V1 requires a openweahtermaps API authentication (see above).</p>
<h2>Rate Limiting</h2>
<p>V1 does not have a rate limiting. Requests are limited to XXX calls per minute.</p>
<h2>Version</h2>
<p>Published V1 20230401</p>
<h2>Built-with</h2>
<p>flask</p>
<h2>license</h2>

# Xmeme - Meme Stream Application

<h2> Introduction</h2>

A Full Stack Application for storing and retrieving memes - <a href="https://mehul-xmeme.netlify.app/">XMeme</a><br>

<h4>Tech Stack:</h4>
<ul>
  <li>FrontEnd - HTML + CSS + BootStrap + JQuery - Deployed on <a href="https://mehul-xmeme.netlify.app/">Netlify</a></li>
  <li>BackEnd - Flask - Deployed on <a href="https://mehul-xmeme-backend.herokuapp.com/memes">Heroku</a></li>
  <li>DataBase - MySql</li>
  <li>Documentation of APIs - Swagger(OpenApi 3)</li>
</ul>

<h2> Ways to run the Application</h2>
<ol>
  <li><code>chmod +x test_server.sh & ./test_server.sh</code> - Will do necessary installations, runs the server and demonstrates basic functionalities using curl requests</li>
  <li>Steps:<br>
    <ol>
      <li><code>chmod +x install.sh & sudo ./install.sh</code> - Will install MySql(<b>On prompted to set MySql Root password - Just press enter</b>) and necessary python packages </li>
      <li><code>chmod +x server_run.sh & ./server_run.sh &</code> - Will run the server in the backend</li>
      <li><code>cd frontend</code> and open index.html - for launching frontend</li>
      <li><code>curl --location --request GET 'http://localhost:8080/swagger-ui/'</code> - Will fetch Swagger API documentation in JSON format - can be used for backend requests</li>
    </ol>
  </li>

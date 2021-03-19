const express = require('express');
const app = express();
const port = 8080;

const mysql = require('mysql');
let connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'platypus_dev',
});

connection.connect(err => {
    if (err) {
        console.log('Error connecting to db: ', err);
        return;
    }
    console.log('Connection established.');
});
connection.query('SELECT * FROM articles', function (err, rows, fields) {
  if (err) throw err;
});
connection.end();

app.use(express.static('public'));

app.get('/search', (req, res) => {
  const q = req.query.q;

  //   console.log('The solution is: ', rows);
  res.status(200).json({ results: [], q });
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});

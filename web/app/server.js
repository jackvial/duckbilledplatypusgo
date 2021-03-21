const dotenv = require('dotenv');
dotenv.config();
const httpClient = require('http');
const express = require('express');
const app = express();
const dbConnectionPool = require('./database/connection');

app.use(express.static('public'));

app.get('/search', (req, res) => {
  const client = httpClient.request(
    {
      hostname: 'platypus_inference',
      port: 80,
      path: '/predict',
      method: 'GET',
    },
    (res) => {
      console.log(`statusCode: ${res.statusCode}`);

      res.on('data', (d) => {
        process.stdout.write(d);
      });
    }
  );

  client.on('error', (error) => {
    console.error(error);
  });

  client.end();

  const q = req.query.q;
  dbConnectionPool.query(
    'SELECT id, body FROM articles WHERE body LIKE ?',
    ['%' + q + '%'],
    (err, rows, fields) => {
      if (err) throw err;
      res.status(200).json({ results: rows, q });
    }
  );
});

app.listen(process.env.NODE_PORT, () => {
  console.log(`Platypus Go! Is listening on port: ${process.env.NODE_PORT}`);
});

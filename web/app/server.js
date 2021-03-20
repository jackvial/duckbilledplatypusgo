const dotenv = require('dotenv');
dotenv.config();
const express = require('express');
const app = express();
const dbConnectionPool = require('./database/connection');

app.use(express.static('public'));

app.get('/search', (req, res) => {
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

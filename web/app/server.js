const dotenv = require('dotenv');
dotenv.config();
const superagent = require('superagent');
const express = require('express');
const app = express();
const dbConnectionPool = require('./database/connection');
app.use(express.static('public'));

app.get('/search', (searchReq, searchRes) => {
  const question = searchReq.query.q;
  dbConnectionPool.query(
    //'SELECT id, body FROM articles WHERE body LIKE ?'
    'SELECT id, body FROM articles WHERE id > 0',
    ['%' + question + '%'],
    (err, rows) => {
      if (err) throw err;

      superagent
        .post('http://platypus_inference/predict')
        .send({ question: question, contexts: rows.map((item) => item.body) })
        .set('accept', 'json')
        .end((err, predictRes) => {
          searchRes.status(200).json({
            results: predictRes.body.results
              .sort((a, b) => {
                return b.score - a.score;
              })
              .filter((item) => item.score > 0.5),
            question,
          });
        });
    }
  );
});

app.listen(process.env.NODE_PORT, () => {
  console.log(`Platypus Go! Is listening on port: ${process.env.NODE_PORT}`);
});

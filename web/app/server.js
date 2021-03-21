const dotenv = require('dotenv');
dotenv.config();
// const httpClient = require('http');
const superagent = require('superagent');
const express = require('express');
const app = express();
const dbConnectionPool = require('./database/connection');

app.use(express.static('public'));

app.get('/search', (searchReq, searchRes) => {
  const query = searchReq.query.q;
  dbConnectionPool.query(
    //'SELECT id, body FROM articles WHERE body LIKE ?'
    'SELECT id, body FROM articles WHERE id > 0',
    ['%' + query + '%'],
    (err, rows, fields) => {
      if (err) throw err;

      superagent
        .post('http://platypus_inference/predict')
        .send({ query: query, contexts: rows.map((item) => item.body) }) // sends a JSON post body
        .set('accept', 'json')
        .end((err, predictRes) => {
          // console.log('superagent err: ', err);
          // console.log('superagent res: ', JSON.stringify(res.body));
          searchRes.status(200).json({
            results: predictRes.body.results.sort((a, b) => {
              return b.score - a.score;
            }).filter(item => item.score > 0.5),
            query,
          });
        });
    }
  );
});

app.listen(process.env.NODE_PORT, () => {
  console.log(`Platypus Go! Is listening on port: ${process.env.NODE_PORT}`);
});

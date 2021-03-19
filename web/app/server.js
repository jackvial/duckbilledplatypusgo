const express = require('express');
const app = express();
const port = 8080;

app.use(express.static('public'));

app.get('/search', (req, res) => {
  const q = req.query.q;
  res.status(200).json({ results: [{ id: 1 }, { id: 2 }, { id: 3 }], q });
});

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});

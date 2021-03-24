const dotenv = require('dotenv');
dotenv.config();
const util = require('util');
const mysql = require('mysql');
const pool = mysql.createPool({
  connectionLimit: 10,
  host: process.env.DB_HOST,
  user: process.env.DB_USERNAME,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_DATABASE,
});

// Ping database to check for common exception errors.
// Give mysql a second to startup.
setTimeout(() => {
  pool.getConnection((err, connection) => {
    if (err) {
      if (err.code === 'PROTOCOL_CONNECTION_LOST') {
        console.error('Database connection was closed.');
      }
      if (err.code === 'ER_CON_COUNT_ERROR') {
        console.error('Database has too many connections.');
      }
      if (err.code === 'ECONNREFUSED') {
        console.error('Database connection was refused.');
      }
    }

    if (connection) connection.release();

    return;
  });
}, 1000);

// Promisify for Node.js async/await.
pool.query = util.promisify(pool.query);

module.exports = pool;

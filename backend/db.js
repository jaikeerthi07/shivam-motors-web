const mysql = require('mysql2');

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'jaikeerthi07a',
  database: 'shivmotors',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

// Create tables if not exists
pool.query(`
  CREATE TABLE IF NOT EXISTS bikes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    badge VARCHAR(255),
    info VARCHAR(255),
    image_url VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  )
`, (err, results) => {
  if (err) {
    console.error('Error creating bikes table:', err);
  } else {
    console.log('Bikes table is ready.');
  }
});

pool.query(`
  CREATE TABLE IF NOT EXISTS valuations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(255) NOT NULL,
    bike_model VARCHAR(255) NOT NULL,
    year VARCHAR(255) NOT NULL,
    kilometers VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  )
`, (err) => {
  if (err) {
    console.error('Error creating valuations table:', err);
  } else {
    console.log('Valuations table is ready.');
  }
});

module.exports = pool.promise();

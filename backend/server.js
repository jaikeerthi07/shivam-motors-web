const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const db = require('./db');
const fs = require('fs');
const crypto = require('crypto');

// Generate a runtime session token exclusively for this boot cycle
// Use a static token for development to avoid session loss on server restart
let currentAdminToken = 'shivadmin_secret_token_2026';

const app = express();
const PORT = 3000;

// Set up static directories
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, '../sm')));

// Ensure upload directory exists
const uploadDir = path.join(__dirname, '../sm/uploads');
if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir, { recursive: true });
}

// Set up Multer for handling file uploads
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, uploadDir);
  },
  filename: function (req, file, cb) {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, uniqueSuffix + path.extname(file.originalname));
  }
});

const upload = multer({ storage: storage });

// API Endpoint to get bikes (optional category filter)
app.get('/api/bikes', async (req, res) => {
  try {
    const category = req.query.category;
    let query = 'SELECT * FROM bikes ORDER BY id DESC';
    let params = [];
    if (category) {
      query = 'SELECT * FROM bikes WHERE category = ? ORDER BY id DESC';
      params = [category];
    }
    const [rows] = await db.query(query, params);
    res.json(rows);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Database error' });
  }
});

app.get('/api/bikes/:category', async (req, res) => {
  try {
    const { category } = req.params;
    const [rows] = await db.query('SELECT * FROM bikes WHERE category = ? ORDER BY id DESC', [category]);
    res.json(rows);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Database error' });
  }
});

// API Endpoint to authenticate admin
app.post('/api/admin/login', (req, res) => {
  const { username, password } = req.body;
  if (username === 'admin' && password === 'shivadmin123') {
    res.json({ token: currentAdminToken });
  } else {
    res.status(401).json({ error: 'Invalid credentials. Access denied.' });
  }
});

// API Endpoint to upload a new bike photo and info
app.post('/api/admin/bikes', upload.single('photo'), async (req, res) => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader || authHeader !== `Bearer ${currentAdminToken}`) {
      return res.status(401).json({ error: 'Unauthorized access. Valid token required.' });
    }

    const { title, price, category, badge, info, description, status } = req.body;
    
    if (!req.file) {
      return res.status(400).json({ error: 'Photo is required' });
    }
    
    const imageUrl = '/uploads/' + req.file.filename;

    const [result] = await db.query(
      'INSERT INTO bikes (title, price, category, badge, info, description, image_url, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
      [title, price, category, badge || null, info || null, description || null, imageUrl, status || 'unsold']
    );

    res.status(201).json({ id: result.insertId, message: 'Bike added successfully' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Database error' });
  }
});

// API Endpoint to delete a bike and its photo
app.delete('/api/admin/bikes/:id', async (req, res) => {
  try {
    console.log(`Attempting to delete bike ID: ${req.params.id}`);
    const authHeader = req.headers.authorization;
    if (!authHeader || authHeader !== `Bearer ${currentAdminToken}`) {
      console.log('Delete failed: Unauthorized');
      return res.status(401).json({ error: 'Unauthorized access. Valid token required.' });
    }

    const bikeId = req.params.id;
    
    const [rows] = await db.query('SELECT image_url FROM bikes WHERE id = ?', [bikeId]);
    if (rows.length === 0) {
      console.log(`Delete failed: Bike ${bikeId} not found`);
      return res.status(404).json({ error: 'Bike not found' });
    }
    
    // Delete from database
    await db.query('DELETE FROM bikes WHERE id = ?', [bikeId]);
    console.log(`Bike ${bikeId} deleted from database`);
    
    // Delete the image file if it exists
    const imagePath = rows[0].image_url;
    if (imagePath && imagePath.startsWith('/uploads/')) {
      const fullPath = path.join(__dirname, '../sm', imagePath);
      if (fs.existsSync(fullPath)) {
        fs.unlinkSync(fullPath);
        console.log(`Image file deleted: ${fullPath}`);
      }
    }
    
    res.json({ message: 'Bike deleted successfully' });
  } catch (error) {
    console.error('Error in DELETE /api/admin/bikes/:id:', error);
    res.status(500).json({ error: 'Database error' });
  }
});

// API Endpoint to receive valuation requests
app.post('/api/valuations', async (req, res) => {
  try {
    const { name, phone, bike_model, year, kilometers, city } = req.body;
    
    if (!name || !phone || !bike_model) {
      return res.status(400).json({ error: 'Name, phone, and bike model are required.' });
    }

    const [result] = await db.query(
      'INSERT INTO valuations (name, phone, bike_model, year, kilometers, city) VALUES (?, ?, ?, ?, ?, ?)',
      [name, phone, bike_model, year || '', kilometers || '', city || '']
    );

    res.status(201).json({ id: result.insertId, message: 'Valuation request received!' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Database error' });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

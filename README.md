# Shivam Moto - Multi-Brand Bike Dealership Platform

A full-stack web application designed for a multi-brand bike dealership containing dynamic listings of New Bikes, Pre-Owned Bikes, and special Offers, powered by a customized administrative dashboard.

## 🚀 Features

- **Dynamic Frontend Displays:** Beautiful, responsive UI displaying New Bikes, Old Bikes, and Today's Offers. 
- **Admin Dashboard:** A dedicated backend integration that allows the shop admin to seamlessly upload photos and specific bike details.
- **Categorized Inventory:** Automatic segregation of uploads into respective public pages (New, Used, Offers).
- **Secure Image Uploads:** Safe, persistent file upload system via Multer binding image routes dynamically. 
- **Database Driven:** Integrated MySQL backing for durable data operations.

## 🛠️ Required Technologies

- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Backend:** Node.js, Express.js
- **Database:** MySQL
- **Other:** Multer (File managing)

## 📁 Project Structure

The codebase is logically split between the client (frontend) and the server (backend):

```text
e:\shivmotors\
│
├── sm/                 # Frontend Website
│   ├── index.html      # Main Landing Page / Homepage
│   ├── new-bikes.html  # Dynamic New Bike Listings
│   ├── old-bikes.html  # Dynamic Pre-Owned Bike Listings
│   └── admin.html      # Administrator Console
│
└── backend/            # Express Server and Database Code
    ├── server.js       # Main server initialization (APIs & Storage)
    ├── db.js           # MySQL Database connection mapping
    └── package.json    # Backend Dependencies list
```

## ⚙️ Local Installation & Setup

Follow these steps to run the application on your local machine:

1. **Install Node.js Dependencies**  
   Navigate to the backend directory and install the necessary npm packages:
   ```bash
   cd e:\shivmotors\backend
   npm install express multer mysql2 cors
   ```

2. **Database Configuration**  
   - Ensure you have a local instance of MySQL Server running (via MySQL Workbench, XAMPP, or WAMP).
   - Ensure the database configuration block in `backend/server.js` or `backend/db.js` accurately matches your local MySQL credentials:
     - **Host:** `localhost`
     - **User:** `root`
     - **Password:** *your_mysql_password* (e.g. `jaikeerthi07a`)
     - **Database:** `shivmotors` (this will automatically configure upon running).

3. **Start the Application Backend**  
   Initiate the node server from your backend directory:
   ```bash
   node server.js
   ```
   *The server runs locally via `http://localhost:3000` or whatever predefined port you have set.*

4. **Access the Public Site**  
   Once the server is running, you can serve or navigate to your frontend by requesting the homepage directly:
   `http://localhost:3000/sm/index.html` *(Ensure your static routing correctly points to your `/sm` path)*.

## 🔒 Accessing the Administrative Dashboard

The administrator platform allows direct oversight of the virtual showroom floor. 
1. Navigate directly to your local target: `http://localhost:3000/sm/admin.html`
2. Prepare a bike offering with a Title, Price, details, categorical tags, and an image utilizing the form.
3. Authenticate the entry operation with the configured Admin Password (**Default:** `admin`).
4. Click `Upload & Save` – the motorcycle will dynamically register and populate directly on your live website. 

---
*Developed & Maintained by Jaikeerthi | 2026*

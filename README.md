# Shivam Moto - Multi-Brand Bike Dealership Platform

A full-stack web application designed for a multi-brand bike dealership containing dynamic listings of New Bikes, Pre-Owned Bikes, and special Offers, powered by a customized administrative dashboard.

## 🚀 Features

- **Dynamic Frontend Displays:** Beautiful, responsive UI displaying New Bikes, Old Bikes, and Today's Offers. 
- **Admin Dashboard:** A dedicated backend integration that allows the shop admin to seamlessly upload photos and specific bike details.
- **Categorized Inventory:** Automatic segregation of uploads into respective public pages (New, Used, Offers).
- **Secure Image Uploads:** Safe, persistent file upload system.
- **Database Driven:** Integrated MySQL backing for durable data operations.

## 🛠️ Required Technologies

- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Backend:** Python, FastAPI, Uvicorn
- **Database:** MySQL
- **Other:** Python-Multipart (File managing)

## 📁 Project Structure

The codebase is split between the client (frontend) and the server (backend-python):

```text
e:\shivmotors\
│
├── sm/                 # Frontend Website
│   ├── index.html      # Main Landing Page / Homepage
│   ├── new-bikes.html  # Dynamic New Bike Listings
│   ├── old-bikes.html  # Dynamic Pre-Owned Bike Listings
│   └── admin.html      # Administrator Console
│
└── backend-python/     # Python FastAPI Server
    ├── main.py         # Main entry point and routing
    ├── database.py     # MySQL Database connection mapping
    ├── bikes.py        # Bikes module (CRUD)
    ├── valuations.py   # Valuations module
    └── requirements.txt # Python Dependencies list
```

## ⚙️ Local Installation & Setup

Follow these steps to run the application on your local machine:

1. **Install Python Dependencies**  
   Navigate to the `backend-python` directory and install the necessary packages:
   ```bash
   cd e:\shivmotors\backend-python
   pip install -r requirements.txt
   ```

2. **Database Configuration**  
   - Ensure you have a local instance of MySQL Server running.
   - The database configuration in `backend-python/database.py` should match your local MySQL credentials:
     - **Host:** `localhost`
     - **User:** `root`
     - **Password:** `jaikeerthi07a`
     - **Database:** `shivmotors`

3. **Start the Application Backend**  
   Initiate the FastAPI server:
   ```bash
   python main.py
   ```
   *The server runs locally via `http://localhost:3000`.*

4. **Access the Public Site**  
   Once the server is running, go to:
   `http://localhost:3000`

## 🔒 Accessing the Administrative Dashboard

The administrator platform allows direct oversight of the virtual showroom floor. 
1. Navigate to: `http://localhost:3000/admin.html`
2. Prepare a bike offering with a Title, Price, details, categorical tags, and an image.
3. Authenticate with the Admin Password (**Default:** `admin`).
4. Click `Upload & Save` – the motorcycle will dynamically register on your live website. 

---
*Developed & Maintained by Jaikeerthi | 2026*

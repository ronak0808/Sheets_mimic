📌 Features
✅ User Authentication (Signup/Login/Logout)
✅ Create, Save, and Load Spreadsheets
✅ Edit Cells, Apply Formulas (SUM, AVERAGE, MAX, etc.)
✅ Bold, Italic, Underline Formatting
✅ Add/Remove Rows & Columns
✅ Remove Duplicates, Find & Replace
✅ Drag and Drop Cell Content
✅ Responsive & Modern UI with Bootstrap
✅ REST API for Saving & Retrieving Sheets

🚀 Tech Stack
🔹 Backend: Django + Django REST Framework (DRF)
🔹 Frontend: JavaScript + Bootstrap
🔹 Database: SQLite (can be extended to PostgreSQL)
🔹 Deployment: Hosted on Circumeo
🔹 Version Control: GitHub

📂 Installation & Setup
🔧 1. Clone the Repository
   git clone https://github.com/ronak0808/Sheets_mimic.git
   cd Sheets_mimic

 📦 2. Create and Activate a Virtual Environment
  python -m venv venv  
  source venv/bin/activate  # On Windows: venv\Scripts\activate


  📜 3. Install Dependencies
     pip install -r requirements.txt

  🛠️ 4. Apply Database Migrations
      python manage.py makemigrations
      python manage.py migrate

  🔑 5. Create a Superuser (For Admin Panel Access)
      python manage.py createsuperuser
      
  🚀 6. Run the Development Server
      python manage.py runserver

    🔒 Security Enhancements
  ✔️ CSRF Protection Enabled
  ✔️ Authentication Required for Sheets Access
  ✔️ User-Specific Data Isolation
  ✔️ Secure Password Hashing using Django Auth
  
  🚀 Performance Enhancements
  ✔️ AJAX-based updates to avoid full-page reloads
  ✔️ Optimized database queries for fast data retrieval
  ✔️ Minified Static Files for Faster Load Times

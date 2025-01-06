# Clinical Management System (CMS)

The Clinical Management System (CMS) is a web-based application designed to streamline and enhance the operations of healthcare facilities. It provides a comprehensive platform for managing clinical workflows, patient records, appointments, and pharmacy operations. Built with Angular for the frontend and Django for the backend, the CMS ensures a seamless and efficient user experience.

## Features

- **User Interface**: A responsive and user-friendly interface designed with Angular, HTML, CSS, and Bootstrap.
- **API Integration**: Seamless data communication using HTTP GET and POST APIs built with Django REST Framework.
- **Database Management**: Optimized MySQL database with joins, CRUD operations, and normalization to ensure scalability and performance.
- **Pharmacy Management Module**: Integrated pharmacy management to streamline medication dispensing and inventory.
- **Testing and Debugging**: Extensive unit testing, debugging, and integration testing to ensure stability and reliability.

## Technology Stack

- **Frontend**: Angular 10
  - Framework: Angular
  - Styling: HTML, CSS, Bootstrap
- **Backend**: Django
  - APIs: HTTP GET and POST APIs using Django REST Framework
- **Database**: MySQL
  - Features: Joins, CRUD operations, Normalization

## Roles and Responsibilities

- **Frontend Development**:
  - Designed responsive and interactive user interfaces using Angular, HTML, CSS, and Bootstrap.
  
- **Database Design**:
  - Created a normalized MySQL database schema to ensure data integrity and efficient queries.

- **API Development**:
  - Developed RESTful APIs with Django REST Framework for seamless frontend-backend communication.

- **Testing and Debugging**:
  - Conducted debugging, unit testing, and integration testing to identify and resolve issues, ensuring system stability.

- **Module Integration**:
  - Integrated the Pharmacy Management Module with other system components to deliver a cohesive user experience.

## Installation and Setup

Follow these steps to set up the CMS project locally:

### Prerequisites
- Node.js (v12 or higher)
- Angular CLI (v10 or higher)
- Python (v3.8 or higher)
- MySQL Server
- pip (Python package installer)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd clinical-management-system
   ```

2. **Backend Setup**:
   - Navigate to the backend folder:
     ```bash
     cd backend
     ```
   - Install Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Set up the database:
     - Create a MySQL database named `cms`.
     - Update the `settings.py` file with your database credentials.
     - Apply migrations:
       ```bash
       python manage.py makemigrations
       python manage.py migrate
       ```
   - Run the Django development server:
     ```bash
     python manage.py runserver
     ```

3. **Frontend Setup**:
   - Navigate to the frontend folder:
     ```bash
     cd frontend
     ```
   - Install Angular dependencies:
     ```bash
     npm install
     ```
   - Start the Angular development server:
     ```bash
     ng serve
     ```

4. **Access the Application**:
   - Open your browser and navigate to `http://localhost:4200`.

## Usage

1. **Login**: Access the system using valid credentials.
2. **Manage Patients**: Add, update, view, or delete patient records.
3. **Schedule Appointments**: Manage and view appointment schedules.
4. **Pharmacy Management**: Handle medication inventory and dispensing.
5. **Reports**: Generate reports for better insights.

## Contribution

If you wish to contribute:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```

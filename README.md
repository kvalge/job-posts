# Job posts app created by Cursor.  
Promt: Create here on job-posts folder small and simple application with flask back-end and vue.js front-end. Functionalities: add, update, delete job post. Job post: title, created, deadline, description. Job requirements: name. Languages: name, level. Location: aadress, location type. Company: name, description, benefits, commitments. Use json file as database bearing in mind, that in future it would be changed to some real db. Use OOP and clean code principles.  
Model: auto  


# Job Posts Manager

A simple and modern job posting application built with Flask backend and Vue.js frontend. This application allows you to manage job posts with comprehensive information including company details, requirements, programming languages, and location information.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete job posts
- **Comprehensive Job Information**:
  - Job title, description, and deadlines
  - Company details (name, description, benefits, commitments)
  - Location information (address and type)
  - Job requirements
  - Programming languages with proficiency levels
- **Modern UI**: Clean, responsive design with smooth animations
- **JSON Database**: Simple file-based storage (easily replaceable with real database)
- **OOP Architecture**: Clean code structure with proper separation of concerns

## Project Structure

```
job-posts/
├── app.py              # Flask backend application
├── requirements.txt    # Python dependencies
├── database.json      # JSON database file
├── index.html         # Vue.js frontend
├── styles.css         # CSS styles
├── app.js            # Vue.js application logic
└── README.md         # This file
```

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- Modern web browser

### Backend Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask server**:
   ```bash
   python app.py
   ```

   The backend will start on `http://localhost:5000`

### Frontend Setup

1. **Open the application**:
   - Simply open `index.html` in your web browser
   - Or serve it using a local server (recommended):
     ```bash
     # Using Python
     python -m http.server 8000
     
     # Using Node.js (if you have it installed)
     npx serve .
     ```

2. **Access the application**:
   - If using a local server: `http://localhost:8000`
   - If opening directly: `file:///path/to/index.html`

## Usage

### Adding a Job Post

1. Click the "Add New Job Post" button
2. Fill in the required information:
   - **Job Title**: The position title
   - **Deadline**: Application deadline
   - **Description**: Detailed job description
   - **Company Information**: Name, description, benefits, and commitments
   - **Location**: Address and location type (Remote/On-site/Hybrid)
   - **Requirements**: Job requirements (one per line)
   - **Languages**: Programming languages with levels (format: `name,level`)
3. Click "Create Job Post"

### Editing a Job Post

1. Click the "Edit" button on any job card
2. Modify the information as needed
3. Click "Update Job Post"

### Deleting a Job Post

1. Click the "Delete" button on any job card
2. Confirm the deletion in the popup dialog

## Data Models

### Job Post
- `id`: Unique identifier
- `title`: Job title
- `created`: Creation timestamp
- `deadline`: Application deadline
- `description`: Job description
- `requirements`: Array of job requirements
- `languages`: Array of programming languages
- `location`: Location information
- `company`: Company information

### Company
- `name`: Company name
- `description`: Company description
- `benefits`: Array of company benefits
- `commitments`: Array of company commitments

### Location
- `address`: Physical address or location description
- `location_type`: Type of work (Remote, On-site, Hybrid)

### Job Requirement
- `name`: Requirement name

### Language
- `name`: Programming language name
- `level`: Proficiency level (Beginner, Intermediate, Advanced, Expert)

## API Endpoints

- `GET /api/job-posts` - Get all job posts
- `GET /api/job-posts/<id>` - Get specific job post
- `POST /api/job-posts` - Create new job post
- `PUT /api/job-posts/<id>` - Update job post
- `DELETE /api/job-posts/<id>` - Delete job post

## Architecture

### Backend (Flask)
- **Models**: OOP classes for data representation
- **Repository Pattern**: Data access layer
- **Service Layer**: Business logic
- **REST API**: Clean endpoints with proper error handling

### Frontend (Vue.js)
- **Component-based**: Modular Vue.js application
- **API Service**: Clean API integration
- **Utility Functions**: Reusable helper functions
- **Responsive Design**: Mobile-friendly interface

## Database

The application currently uses a JSON file (`database.json`) for data storage. This makes it easy to:
- Get started quickly without database setup
- View and edit data directly
- Migrate to a real database in the future

To switch to a real database (e.g., PostgreSQL, MySQL), you would only need to modify the `JobPostRepository` class.

## Future Enhancements

- User authentication and authorization
- Search and filtering capabilities
- File uploads for job attachments
- Email notifications
- Advanced analytics and reporting
- Real-time updates
- Mobile application

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License. 
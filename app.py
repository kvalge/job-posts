from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from dateutil import parser
from typing import List, Dict, Any, Optional

app = Flask(__name__)
CORS(app)

# Database file path
DB_FILE = 'database.json'

class JobRequirement:
    """Model for job requirements"""
    
    def __init__(self, name: str):
        self.name = name
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JobRequirement':
        return cls(data['name'])

class Language:
    """Model for programming languages"""
    
    def __init__(self, name: str, level: str):
        self.name = name
        self.level = level
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'level': self.level
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Language':
        return cls(data['name'], data['level'])

class Location:
    """Model for job location"""
    
    def __init__(self, address: str, location_type: str):
        self.address = address
        self.location_type = location_type
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'address': self.address,
            'location_type': self.location_type
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Location':
        return cls(data['address'], data['location_type'])

class Company:
    """Model for company information"""
    
    def __init__(self, name: str, description: str, benefits: List[str], commitments: List[str]):
        self.name = name
        self.description = description
        self.benefits = benefits
        self.commitments = commitments
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'benefits': self.benefits,
            'commitments': self.commitments
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Company':
        return cls(
            data['name'],
            data['description'],
            data['benefits'],
            data['commitments']
        )

class JobPost:
    """Model for job post"""
    
    def __init__(self, id: str, title: str, created: str, deadline: str, 
                 description: str, requirements: List[JobRequirement], 
                 languages: List[Language], location: Location, company: Company):
        self.id = id
        self.title = title
        self.created = created
        self.deadline = deadline
        self.description = description
        self.requirements = requirements
        self.languages = languages
        self.location = location
        self.company = company
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'created': self.created,
            'deadline': self.deadline,
            'description': self.description,
            'requirements': [req.to_dict() for req in self.requirements],
            'languages': [lang.to_dict() for lang in self.languages],
            'location': self.location.to_dict(),
            'company': self.company.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'JobPost':
        requirements = [JobRequirement.from_dict(req) for req in data['requirements']]
        languages = [Language.from_dict(lang) for lang in data['languages']]
        location = Location.from_dict(data['location'])
        company = Company.from_dict(data['company'])
        
        return cls(
            data['id'],
            data['title'],
            data['created'],
            data['deadline'],
            data['description'],
            requirements,
            languages,
            location,
            company
        )

class JobPostRepository:
    """Repository for managing job posts data"""
    
    def __init__(self, db_file: str):
        self.db_file = db_file
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Ensure database file exists with initial structure"""
        if not os.path.exists(self.db_file):
            self._save_data({'job_posts': []})
    
    def _load_data(self) -> Dict[str, Any]:
        """Load data from JSON file"""
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {'job_posts': []}
    
    def _save_data(self, data: Dict[str, Any]):
        """Save data to JSON file"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_all_job_posts(self) -> List[JobPost]:
        """Get all job posts"""
        data = self._load_data()
        return [JobPost.from_dict(post) for post in data.get('job_posts', [])]
    
    def get_job_post_by_id(self, job_id: str) -> Optional[JobPost]:
        """Get job post by ID"""
        job_posts = self.get_all_job_posts()
        for post in job_posts:
            if post.id == job_id:
                return post
        return None
    
    def create_job_post(self, job_post: JobPost) -> JobPost:
        """Create a new job post"""
        data = self._load_data()
        job_posts = data.get('job_posts', [])
        
        # Check if ID already exists
        existing_ids = [post['id'] for post in job_posts]
        if job_post.id in existing_ids:
            raise ValueError(f"Job post with ID {job_post.id} already exists")
        
        job_posts.append(job_post.to_dict())
        data['job_posts'] = job_posts
        self._save_data(data)
        return job_post
    
    def update_job_post(self, job_id: str, updated_post: JobPost) -> Optional[JobPost]:
        """Update an existing job post"""
        data = self._load_data()
        job_posts = data.get('job_posts', [])
        
        for i, post in enumerate(job_posts):
            if post['id'] == job_id:
                job_posts[i] = updated_post.to_dict()
                data['job_posts'] = job_posts
                self._save_data(data)
                return updated_post
        
        return None
    
    def delete_job_post(self, job_id: str) -> bool:
        """Delete a job post"""
        data = self._load_data()
        job_posts = data.get('job_posts', [])
        
        for i, post in enumerate(job_posts):
            if post['id'] == job_id:
                del job_posts[i]
                data['job_posts'] = job_posts
                self._save_data(data)
                return True
        
        return False

class JobPostService:
    """Service layer for job post business logic"""
    
    def __init__(self, repository: JobPostRepository):
        self.repository = repository
    
    def get_all_job_posts(self) -> List[Dict[str, Any]]:
        """Get all job posts as dictionaries"""
        job_posts = self.repository.get_all_job_posts()
        return [post.to_dict() for post in job_posts]
    
    def get_job_post_by_id(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job post by ID as dictionary"""
        job_post = self.repository.get_job_post_by_id(job_id)
        return job_post.to_dict() if job_post else None
    
    def create_job_post(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new job post"""
        # Generate ID if not provided
        if 'id' not in post_data:
            post_data['id'] = self._generate_id()
        
        # Validate required fields
        self._validate_job_post_data(post_data)
        
        # Create job post object
        job_post = self._create_job_post_from_data(post_data)
        
        # Save to repository
        created_post = self.repository.create_job_post(job_post)
        return created_post.to_dict()
    
    def update_job_post(self, job_id: str, post_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing job post"""
        # Validate required fields
        self._validate_job_post_data(post_data)
        
        # Create job post object
        job_post = self._create_job_post_from_data(post_data)
        
        # Update in repository
        updated_post = self.repository.update_job_post(job_id, job_post)
        return updated_post.to_dict() if updated_post else None
    
    def delete_job_post(self, job_id: str) -> bool:
        """Delete a job post"""
        return self.repository.delete_job_post(job_id)
    
    def _generate_id(self) -> str:
        """Generate a unique ID for job post"""
        import uuid
        return str(uuid.uuid4())
    
    def _validate_job_post_data(self, data: Dict[str, Any]):
        """Validate job post data"""
        required_fields = ['title', 'deadline', 'description', 'requirements', 
                          'languages', 'location', 'company']
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
    
    def _create_job_post_from_data(self, data: Dict[str, Any]) -> JobPost:
        """Create JobPost object from dictionary data"""
        # Set created date if not provided
        if 'created' not in data:
            data['created'] = datetime.now().isoformat()
        
        # Create nested objects
        requirements = [JobRequirement.from_dict(req) for req in data['requirements']]
        languages = [Language.from_dict(lang) for lang in data['languages']]
        location = Location.from_dict(data['location'])
        company = Company.from_dict(data['company'])
        
        return JobPost(
            data['id'],
            data['title'],
            data['created'],
            data['deadline'],
            data['description'],
            requirements,
            languages,
            location,
            company
        )

# Initialize services
repository = JobPostRepository(DB_FILE)
job_post_service = JobPostService(repository)

@app.route('/api/job-posts', methods=['GET'])
def get_job_posts():
    """Get all job posts"""
    try:
        job_posts = job_post_service.get_all_job_posts()
        return jsonify(job_posts), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/job-posts/<job_id>', methods=['GET'])
def get_job_post(job_id):
    """Get job post by ID"""
    try:
        job_post = job_post_service.get_job_post_by_id(job_id)
        if job_post:
            return jsonify(job_post), 200
        else:
            return jsonify({'error': 'Job post not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/job-posts', methods=['POST'])
def create_job_post():
    """Create a new job post"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        created_post = job_post_service.create_job_post(data)
        return jsonify(created_post), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/job-posts/<job_id>', methods=['PUT'])
def update_job_post(job_id):
    """Update an existing job post"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Ensure ID in data matches URL parameter
        data['id'] = job_id
        
        updated_post = job_post_service.update_job_post(job_id, data)
        if updated_post:
            return jsonify(updated_post), 200
        else:
            return jsonify({'error': 'Job post not found'}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/job-posts/<job_id>', methods=['DELETE'])
def delete_job_post(job_id):
    """Delete a job post"""
    try:
        success = job_post_service.delete_job_post(job_id)
        if success:
            return jsonify({'message': 'Job post deleted successfully'}), 200
        else:
            return jsonify({'error': 'Job post not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 
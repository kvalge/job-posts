#!/usr/bin/env python3
"""
Simple test script to verify the Job Posts API functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

def test_api():
    print("Testing Job Posts API...")
    
    # Test data
    test_job = {
        "title": "Senior Python Developer",
        "deadline": "2024-12-31T23:59:59",
        "description": "We are looking for an experienced Python developer to join our team.",
        "company": {
            "name": "TechCorp Inc.",
            "description": "A leading technology company specializing in web applications.",
            "benefits": ["Health insurance", "Remote work", "Flexible hours"],
            "commitments": ["Full-time", "On-site work"]
        },
        "location": {
            "address": "123 Tech Street, Silicon Valley, CA",
            "location_type": "On-site"
        },
        "requirements": [
            {"name": "Bachelor's degree in Computer Science"},
            {"name": "5+ years of Python experience"},
            {"name": "Experience with Flask/Django"}
        ],
        "languages": [
            {"name": "Python", "level": "Advanced"},
            {"name": "JavaScript", "level": "Intermediate"},
            {"name": "SQL", "level": "Advanced"}
        ]
    }
    
    try:
        # Test 1: Create a job post
        print("\n1. Creating a job post...")
        response = requests.post(f"{BASE_URL}/job-posts", json=test_job)
        if response.status_code == 201:
            created_job = response.json()
            job_id = created_job["id"]
            print(f"✅ Job post created successfully with ID: {job_id}")
        else:
            print(f"❌ Failed to create job post: {response.status_code}")
            print(response.text)
            return
        
        # Test 2: Get all job posts
        print("\n2. Getting all job posts...")
        response = requests.get(f"{BASE_URL}/job-posts")
        if response.status_code == 200:
            jobs = response.json()
            print(f"✅ Retrieved {len(jobs)} job posts")
        else:
            print(f"❌ Failed to get job posts: {response.status_code}")
            return
        
        # Test 3: Get specific job post
        print("\n3. Getting specific job post...")
        response = requests.get(f"{BASE_URL}/job-posts/{job_id}")
        if response.status_code == 200:
            job = response.json()
            print(f"✅ Retrieved job post: {job['title']}")
        else:
            print(f"❌ Failed to get specific job post: {response.status_code}")
            return
        
        # Test 4: Update job post
        print("\n4. Updating job post...")
        updated_job = test_job.copy()
        updated_job["title"] = "Senior Python Developer - Updated"
        updated_job["id"] = job_id
        
        response = requests.put(f"{BASE_URL}/job-posts/{job_id}", json=updated_job)
        if response.status_code == 200:
            updated_job_response = response.json()
            print(f"✅ Job post updated: {updated_job_response['title']}")
        else:
            print(f"❌ Failed to update job post: {response.status_code}")
            return
        
        # Test 5: Delete job post
        print("\n5. Deleting job post...")
        response = requests.delete(f"{BASE_URL}/job-posts/{job_id}")
        if response.status_code == 200:
            print("✅ Job post deleted successfully")
        else:
            print(f"❌ Failed to delete job post: {response.status_code}")
            return
        
        # Test 6: Verify deletion
        print("\n6. Verifying deletion...")
        response = requests.get(f"{BASE_URL}/job-posts/{job_id}")
        if response.status_code == 404:
            print("✅ Job post successfully deleted (404 Not Found)")
        else:
            print(f"❌ Job post still exists: {response.status_code}")
            return
        
        print("\n🎉 All tests passed! The API is working correctly.")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    test_api() 
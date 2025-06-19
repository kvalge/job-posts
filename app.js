const { createApp } = Vue;

// API Service
class JobPostAPI {
    constructor(baseURL = 'http://localhost:5000/api') {
        this.baseURL = baseURL;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || `HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    async getAllJobPosts() {
        return this.request('/job-posts');
    }

    async getJobPost(id) {
        return this.request(`/job-posts/${id}`);
    }

    async createJobPost(data) {
        return this.request('/job-posts', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    async updateJobPost(id, data) {
        return this.request(`/job-posts/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    async deleteJobPost(id) {
        return this.request(`/job-posts/${id}`, {
            method: 'DELETE'
        });
    }
}

// Utility functions
const utils = {
    formatDate(dateString) {
        if (!dateString) return 'N/A';
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch (error) {
            return dateString;
        }
    },

    truncateText(text, maxLength) {
        if (!text) return '';
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    },

    parseTextToArray(text) {
        if (!text) return [];
        return text.split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0);
    },

    parseLanguagesText(text) {
        if (!text) return [];
        return text.split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0)
            .map(line => {
                const parts = line.split(',').map(part => part.trim());
                return {
                    name: parts[0] || '',
                    level: parts[1] || 'Beginner'
                };
            });
    },

    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
};

// Vue Application
createApp({
    data() {
        return {
            // API service
            api: new JobPostAPI(),
            
            // State
            jobPosts: [],
            loading: false,
            showAddForm: false,
            editingJob: null,
            
            // Form data
            formData: {
                title: '',
                deadline: '',
                description: '',
                company: {
                    name: '',
                    description: '',
                    benefits: [],
                    commitments: []
                },
                location: {
                    address: '',
                    location_type: ''
                },
                requirements: [],
                languages: []
            },
            
            // Form text inputs (for easier handling)
            benefitsText: '',
            commitmentsText: '',
            requirementsText: '',
            languagesText: '',
            
            // Notifications
            notification: {
                show: false,
                message: '',
                type: 'info'
            }
        };
    },

    mounted() {
        this.loadJobPosts();
    },

    methods: {
        // Data loading
        async loadJobPosts() {
            this.loading = true;
            try {
                this.jobPosts = await this.api.getAllJobPosts();
            } catch (error) {
                this.showNotification('Failed to load job posts: ' + error.message, 'error');
            } finally {
                this.loading = false;
            }
        },

        // Form handling
        resetForm() {
            this.formData = {
                title: '',
                deadline: '',
                description: '',
                company: {
                    name: '',
                    description: '',
                    benefits: [],
                    commitments: []
                },
                location: {
                    address: '',
                    location_type: ''
                },
                requirements: [],
                languages: []
            };
            
            this.benefitsText = '';
            this.commitmentsText = '';
            this.requirementsText = '';
            this.languagesText = '';
        },

        editJob(job) {
            this.editingJob = job;
            this.formData = JSON.parse(JSON.stringify(job));
            
            // Convert arrays to text for form inputs
            this.benefitsText = job.company.benefits.join('\n');
            this.commitmentsText = job.company.commitments.join('\n');
            this.requirementsText = job.requirements.map(req => req.name).join('\n');
            this.languagesText = job.languages.map(lang => `${lang.name},${lang.level}`).join('\n');
        },

        cancelForm() {
            this.showAddForm = false;
            this.editingJob = null;
            this.resetForm();
        },

        prepareFormData() {
            // Parse text inputs back to arrays/objects
            const data = JSON.parse(JSON.stringify(this.formData));
            
            data.company.benefits = utils.parseTextToArray(this.benefitsText);
            data.company.commitments = utils.parseTextToArray(this.commitmentsText);
            data.requirements = utils.parseTextToArray(this.requirementsText).map(name => ({ name }));
            data.languages = utils.parseLanguagesText(this.languagesText);
            
            return data;
        },

        async saveJob() {
            this.loading = true;
            try {
                const data = this.prepareFormData();
                
                if (this.editingJob) {
                    // Update existing job
                    await this.api.updateJobPost(this.editingJob.id, data);
                    this.showNotification('Job post updated successfully!', 'success');
                } else {
                    // Create new job
                    data.id = utils.generateId();
                    await this.api.createJobPost(data);
                    this.showNotification('Job post created successfully!', 'success');
                }
                
                await this.loadJobPosts();
                this.cancelForm();
            } catch (error) {
                this.showNotification('Failed to save job post: ' + error.message, 'error');
            } finally {
                this.loading = false;
            }
        },

        async deleteJob(jobId) {
            if (!confirm('Are you sure you want to delete this job post?')) {
                return;
            }
            
            this.loading = true;
            try {
                await this.api.deleteJobPost(jobId);
                this.showNotification('Job post deleted successfully!', 'success');
                await this.loadJobPosts();
            } catch (error) {
                this.showNotification('Failed to delete job post: ' + error.message, 'error');
            } finally {
                this.loading = false;
            }
        },

        // Utility methods
        formatDate(dateString) {
            return utils.formatDate(dateString);
        },

        truncateText(text, maxLength) {
            return utils.truncateText(text, maxLength);
        },

        // Notifications
        showNotification(message, type = 'info') {
            this.notification = {
                show: true,
                message,
                type
            };
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                this.hideNotification();
            }, 5000);
        },

        hideNotification() {
            this.notification.show = false;
        }
    }
}).mount('#app'); 
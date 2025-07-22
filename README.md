# SPARC-Frontend

Frontend for the SPARC (Shidduch Programming and Relationship Compatibility) matchmaking platform.

## Overview

SPARC-Frontend is a mobile-friendly web interface that connects to the SPARC backend API. It allows Jewish matchmakers to:

- Manage their applicant profiles
- View potential matches from a larger pool of applicants
- Analyze compatibility between potential matches
- Track match progress

## Features

- Responsive mobile-first design
- Secure authentication for matchmakers
- Comprehensive applicant profile management
- Advanced match filtering and sorting
- Compatibility analysis visualization
- Mobile optimizations, including bottom navigation

## Tech Stack

- Flask (Python web framework)
- Bootstrap 5 (Mobile-friendly UI framework)
- Font Awesome (Icons)
- JavaScript (Client-side interactions)
- CSS (Custom styling)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SPARC-Frontend.git
cd SPARC-Frontend
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following configuration:
```
SECRET_KEY=your_secret_key_here
API_URL=http://localhost:5000/api  # URL to your SPARC backend API
```

## Running the Application

```bash
python app.py
```

The frontend will be available at http://localhost:5001

## Backend Connection

This frontend is designed to connect to the SPARC Backend API. Make sure the backend server is running and accessible at the URL specified in your `.env` file.

## Mobile Optimization

The interface is optimized for mobile devices with:
- Responsive layouts
- Touch-friendly controls
- Bottom navigation on small screens
- Minimized data usage

## License

This project is licensed under the MIT License - see the LICENSE file for details.
# Gym Management System

![Gym Management System Banner](https://images.unsplash.com/photo-1558611848-73f7eb4001a5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

Welcome to the **Gym Management System**, a comprehensive web application designed to streamline the operations of a modern gym. Whether you're managing memberships, trainers, workout routines, or gym equipment, this system provides all the tools you need to ensure smooth and efficient gym management.

## Features

- **User Authentication:**
  - Secure login and logout functionalities.
  - Role-based access control to protect sensitive routes.

- **Member Management:**
  - Add, view, edit, and delete gym members.
  - Assign trainers to members.
  - Filter members based on membership type, trainer, and joining dates.

- **Trainer Management:**
  - Manage trainer profiles with detailed information.
  - Assign workout routines to trainers.
  - View trainers along with their assigned workouts.

- **Workout Routine Management:**
  - Create, view, edit, and delete workout routines.
  - Assign workouts to trainers for personalized training programs.

- **Equipment Management:**
  - Track gym equipment with details like quantity, price, manufacturer, and maintenance dates.
  - Add, view, edit, and delete equipment records.

- **Dashboard:**
  - Comprehensive statistics including total members, trainer-wise member distribution, membership type distribution, and trainer-wise workout assignments.

- **Responsive Design:**
  - Mobile-friendly interface ensuring seamless access across all devices.
  - Intuitive navigation with a hamburger menu for smaller screens.

- **Feedback System:**
  - Flash messages to provide real-time feedback on user actions.

## Technology Stack

- **Backend:**
  - [Flask](https://flask.palletsprojects.com/) - A lightweight WSGI web application framework.
  - [SQLite](https://www.sqlite.org/index.html) - A C library that provides a lightweight disk-based database.
  - [Flask-Login](https://flask-login.readthedocs.io/) - User session management for Flask.

- **Frontend:**
  - HTML5 & CSS3 - Markup and styling.
  - [Google Fonts](https://fonts.google.com/) - Typography.
  - [Font Awesome](https://fontawesome.com/) - Icons for enhanced UI.

- **Security:**
  - Password hashing with [Werkzeug](https://werkzeug.palletsprojects.com/).

## Installation

Follow these steps to set up the Gym Management System on your local machine.

### Prerequisites

- Python 3.x installed on your system. You can download it from [here](https://www.python.org/downloads/).
- `pip` package manager.

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/gym-management-system.git
   cd gym-management-system
   ```

2. **Create a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database**

   Ensure you have an `init_db.py` script to set up the SQLite database with necessary tables and an initial admin user.

   ```bash
   python init_db.py
   ```

   *Note: Replace `'ERGETEAMPASS'` in `app.secret_key` with a strong, secure secret key.*

5. **Run the Application**

   ```bash
   python app.py
   ```

6. **Access the Application**

   Open your web browser and navigate to `http://127.0.0.1:5000/` to access the Gym Management System.

## Usage

### Authentication

1. **Login**

   - Navigate to the **Login** page.
   - Enter your username and password.
   - Upon successful login, you'll be redirected to the homepage.

2. **Logout**

   - Click on the **Logout** button located in the navigation bar to end your session.

### Managing Members

- **Add Member:**
  - Click on **Members** in the navigation bar.
  - Select **Add Member** and fill in the required details.

- **View Members:**
  - Click on **Members** to view all registered gym members.
  - Use the **Filter Members** option to search based on specific criteria.

- **Edit/Delete Member:**
  - In the members list, select the **Edit** or **Delete** option next to a member's entry.

### Managing Trainers

- **Add Trainer:**
  - Click on **Trainers** in the navigation bar.
  - Select **Add Trainer** and provide the necessary information.

- **View Trainers:**
  - View all trainers along with their assigned workout routines.

- **Edit/Delete Trainer:**
  - Use the **Edit** or **Delete** options to manage trainer profiles.

### Managing Workouts

- **Add Workout:**
  - Navigate to **Workouts** and select **Add Workout**.
  - Define the workout routine details.

- **View Workouts:**
  - View all workout routines and their details.

- **Edit/Delete Workout:**
  - Manage workout routines using the **Edit** or **Delete** options.

### Managing Equipment

- **Add Equipment:**
  - Go to **Equipment** and select **Add Equipment**.
  - Enter equipment details such as name, quantity, price, etc.

- **View Equipment:**
  - View all gym equipment and their statuses.

- **Edit/Delete Equipment:**
  - Manage equipment records using the **Edit** or **Delete** options.

### Dashboard

- Access the **Dashboard** from the navigation bar to view comprehensive statistics about members, trainers, and workouts.

## Screenshots

*Include relevant screenshots of your application here to give users a visual understanding of the interface.*

![Homepage](screenshots/homepage.png)
*Homepage showcasing navigation and main features.*

![Login Page](screenshots/login.png)
*Login page for user authentication.*

![Dashboard](screenshots/dashboard.png)
*Dashboard displaying key statistics.*

![Member Management](screenshots/members.png)
*Member management interface.*

## Contributing

Contributions are welcome! Follow these steps to contribute to the Gym Management System:

1. **Fork the Repository**

   Click the **Fork** button at the top right of this page.

2. **Clone the Forked Repository**

   ```bash
   git clone https://github.com/yourusername/gym-management-system.git
   cd gym-management-system
   ```

3. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

4. **Make Changes**

   Implement your feature or bug fix.

5. **Commit Changes**

   ```bash
   git commit -m "Add feature: YourFeatureName"
   ```

6. **Push to the Branch**

   ```bash
   git push origin feature/YourFeatureName
   ```

7. **Create a Pull Request**

   Go to the original repository and create a pull request from your forked repository.

## License

Distributed under the GNU License. See `LICENSE` for more information.

## Contact

**Your Name** – [your.email@example.com](mailto:your.email@example.com)

Project Link: [https://github.com/yourusername/gym-management-system](https://github.com/yourusername/gym-management-system), [JeithxEdu.pythonanywhere.com](JeithxEdu.pythonanywhere.com)

---

*Note: Replace placeholder links, images, and contact information with your actual project details.*

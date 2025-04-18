<h1 align="center">🍲 TastyShare - Recipe Sharing Platform</h1>

---

## Overview

TastyShare is a Recipe Sharing Platform built with Streamlit, Python, and SQLite. It allows users to register, login, share their recipes, save their favorite recipes, and leave reviews. The platform enables recipe discovery, management, and interaction in an easy and user-friendly interface.

---

## Features

- **User Authentication**: Users can register, login, and manage their profiles.
- **Recipe Management**: Users can add, edit, and delete recipes.
- **Recipe Categories**: Users can categorize their recipes into Vegetarian, Vegan, and Non-Vegetarian.
- **Image Uploads**: Upload images for recipes.
- **Search Functionality**: Search recipes by title or ingredients.
- **Favourites**: Save your favorite recipes.
- **Reviews**: Rate and review recipes.

---

## Project Structure

<pre><code>
Recipe/
├── App.py              # Main application file
├── database/
│   └── tastyshare.db   # SQLite database file
└── images/             # Folder for storing uploaded images
    └── image_here      # Placeholder for image

</code></pre>

yaml
---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/faisalrafiq031/TastyShare-Using-Python-and-Sqllite3.git
```

### 2. Install Dependencies
You need to install the required Python packages. Install the dependencies.


```bash
# Install dependencies
pip install streamlit pillow werkzeug
```

### 3. Run the App
Start the Streamlit app by running the following command:
```bash
streamlit run App.py
```
Visit the app in your browser at http://localhost:8501.

# Database Schema
Users Table
Stores user information for authentication.

<table border="1" cellpadding="5" cellspacing="0">
  <tr>
    <th>Column</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>id</td>
    <td>INTEGER</td>
    <td>Primary Key</td>
  </tr>
  <tr>
    <td>email</td>
    <td>TEXT</td>
    <td>Unique Email</td>
  </tr>
  <tr>
    <td>password</td>
    <td>TEXT</td>
    <td>Hashed Password</td>
  </tr>
  <tr>
    <td>role</td>
    <td>TEXT</td>
    <td>Role (user/admin)</td>
  </tr>
</table>

<h3>Recipes Table</h3>
<p>Stores recipe details added by users.</p>
<table border="1" cellpadding="5" cellspacing="0">
  <tr>
    <th>Column</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>id</td>
    <td>INTEGER</td>
    <td>Primary Key</td>
  </tr>
  <tr>
    <td>user_id</td>
    <td>INTEGER</td>
    <td>Foreign Key (References Users)</td>
  </tr>
  <tr>
    <td>title</td>
    <td>TEXT</td>
    <td>Recipe Title</td>
  </tr>
  <tr>
    <td>ingredients</td>
    <td>TEXT</td>
    <td>Ingredients</td>
  </tr>
  <tr>
    <td>steps</td>
    <td>TEXT</td>
    <td>Preparation Steps</td>
  </tr>
  <tr>
    <td>category</td>
    <td>TEXT</td>
    <td>Recipe Category</td>
  </tr>
  <tr>
    <td>cooking_time</td>
    <td>TEXT</td>
    <td>Cooking Time</td>
  </tr>
  <tr>
    <td>image_path</td>
    <td>TEXT</td>
    <td>Path to Recipe Image</td>
  </tr>
</table>

<h3>Favourites Table</h3>
<p>Stores user's favorite recipes.</p>
<table border="1" cellpadding="5" cellspacing="0">
  <tr>
    <th>Column</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>user_id</td>
    <td>INTEGER</td>
    <td>Foreign Key (References Users)</td>
  </tr>
  <tr>
    <td>recipe_id</td>
    <td>INTEGER</td>
    <td>Foreign Key (References Recipes)</td>
  </tr>
  <tr>
    <td colspan="3"><strong>Primary Key:</strong> user_id, recipe_id</td>
  </tr>
</table>

<h3>Reviews Table</h3>
<p>Stores user reviews for recipes.</p>
<table border="1" cellpadding="5" cellspacing="0">
  <tr>
    <th>Column</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>user_id</td>
    <td>INTEGER</td>
    <td>Foreign Key (References Users)</td>
  </tr>
  <tr>
    <td>recipe_id</td>
    <td>INTEGER</td>
    <td>Foreign Key (References Recipes)</td>
  </tr>
  <tr>
    <td>review_text</td>
    <td>TEXT</td>
    <td>Review Text</td>
  </tr>
  <tr>
    <td>rating</td>
    <td>INTEGER</td>
    <td>Rating (1-5)</td>
  </tr>
  <tr>
    <td colspan="3"><strong>Primary Key:</strong> user_id, recipe_id</td>
  </tr>
</table>


# Authentication Flow
<li>Register: Users can register with an email and password. If the email already exists, an error message is shown.</li>
<li>Login: Registered users can log in by entering their email and password.</li>
<li>Profile Management: After login, users can update their email and password, or delete their account.</li>
<li>Recipe Management: Logged-in users can add, update, and delete recipes.</li>
<li>Favourites & Reviews: Users can add recipes to their favourites and leave reviews (rating 1-5).</li>

<h2>License</h2>
<p>This project is licensed under the 
  <a href="https://opensource.org/licenses/MIT" target="_blank">MIT License</a> – 
  see the <a href="LICENSE" target="_blank">LICENSE</a> file for details.
</p>

<h2>Acknowledgments</h2>
<ul>
  <li><a href="https://streamlit.io/" target="_blank">Streamlit</a></li>
  <li><a href="https://www.sqlite.org/index.html" target="_blank">SQLite</a></li>
  <li><a href="https://palletsprojects.com/p/werkzeug/" target="_blank">Werkzeug</a></li>
  <li><a href="https://daringfireball.net/projects/markdown/" target="_blank">Markdown</a></li>
</ul>

<h2>📘 README Contents</h2>
<p>This README contains the following sections:</p>
<ul>
  <li><strong>Project Overview</strong>: Description of the application and its features.</li>
  <li><strong>Installation</strong>: Steps to set up the project.</li>
  <li><strong>Database Schema</strong>: Explanation of the database tables.</li>
  <li><strong>Authentication Flow</strong>: Detailed flow for user authentication and profile management.</li>
  <li><strong>License</strong>: Information about the project license.</li>
  <li><strong>Acknowledgments</strong>: Credit to the technologies used in the project.</li>
</ul>



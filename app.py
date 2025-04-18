import streamlit as st
import sqlite3
import os
from PIL import Image
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize DB
conn = sqlite3.connect('database/tastyshare.db', check_same_thread=False)
cursor = conn.cursor()

def column_exists(table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    for col in columns:
        if col[1] == column:
            return True
    return False

def init_db():
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL DEFAULT 'user'
                    )''')
    
    # Only add the columns if they do not exist
    if not column_exists('recipes', 'category'):
        cursor.execute('''ALTER TABLE recipes ADD COLUMN category TEXT''')
    
    if not column_exists('recipes', 'cooking_time'):
        cursor.execute('''ALTER TABLE recipes ADD COLUMN cooking_time TEXT''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS recipes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        title TEXT,
                        ingredients TEXT,
                        steps TEXT,
                        category TEXT,
                        cooking_time TEXT,
                        image_path TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS favourites (
                        user_id INTEGER,
                        recipe_id INTEGER,
                        FOREIGN KEY(user_id) REFERENCES users(id),
                        FOREIGN KEY(recipe_id) REFERENCES recipes(id),
                        PRIMARY KEY(user_id, recipe_id)
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (
                        user_id INTEGER,
                        recipe_id INTEGER,
                        review_text TEXT,
                        rating INTEGER,
                        FOREIGN KEY(user_id) REFERENCES users(id),
                        FOREIGN KEY(recipe_id) REFERENCES recipes(id),
                        PRIMARY KEY(user_id, recipe_id)
                    )''')

    conn.commit()

# Uncomment the following line if you want to drop the recipes table for testing purposes
# cursor.execute("DROP TABLE IF EXISTS recipes")
init_db()

# Auth helpers
def register_user(email, password):
    try:
        cursor.execute("INSERT INTO users (email, password, role) VALUES (?, ?, ?)", 
                       (email, generate_password_hash(password), 'user'))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(email, password):
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    if user and check_password_hash(user[2], password):
        return user
    return None

def update_user_profile(user_id, new_email, new_password):
    hashed_password = generate_password_hash(new_password)
    cursor.execute("UPDATE users SET email = ?, password = ? WHERE id = ?", (new_email, hashed_password, user_id))
    conn.commit()

def delete_user_account(user_id):
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    cursor.execute("DELETE FROM recipes WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM favourites WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM reviews WHERE user_id = ?", (user_id,))
    conn.commit()

def add_recipe(user_id, title, ingredients, steps, category, cooking_time, image_path):
    cursor.execute("INSERT INTO recipes (user_id, title, ingredients, steps, category, cooking_time, image_path) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (user_id, title, ingredients, steps, category, cooking_time, image_path))
    conn.commit()

def update_recipe(recipe_id, title, ingredients, steps, category, cooking_time, image_path):
    cursor.execute("UPDATE recipes SET title = ?, ingredients = ?, steps = ?, category = ?, cooking_time = ?, image_path = ? WHERE id = ?",
                   (title, ingredients, steps, category, cooking_time, image_path, recipe_id))
    conn.commit()

def delete_recipe(recipe_id):
    cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()

def get_all_recipes():
    cursor.execute("SELECT r.id, r.title, r.ingredients, r.steps, r.category, r.cooking_time, r.image_path, u.email FROM recipes r JOIN users u ON r.user_id = u.id")
    return cursor.fetchall()

def get_filtered_recipes(search_query):
    cursor.execute("SELECT r.id, r.title, r.ingredients, r.steps, r.category, r.cooking_time, r.image_path, u.email FROM recipes r JOIN users u ON r.user_id = u.id WHERE r.title LIKE ? OR r.ingredients LIKE ?", 
                   ('%' + search_query + '%', '%' + search_query + '%'))
    return cursor.fetchall()

def add_favourite(user_id, recipe_id):
    cursor.execute("INSERT INTO favourites (user_id, recipe_id) VALUES (?, ?)", (user_id, recipe_id))
    conn.commit()

def add_review(user_id, recipe_id, review_text, rating):
    cursor.execute("INSERT INTO reviews (user_id, recipe_id, review_text, rating) VALUES (?, ?, ?, ?)", 
                   (user_id, recipe_id, review_text, rating))
    conn.commit()

# App State
if "user" not in st.session_state:
    st.session_state.user = None

# Layout
st.set_page_config(page_title="TastyShare", layout="centered")
st.title("🍲 TastyShare - Recipe Sharing Platform")

menu = ["Home", "Login", "Register"]
if st.session_state.user:
    menu = ["Home", "Add Recipe", "Profile", "Logout"]

choice = st.sidebar.selectbox("Menu", menu)

# REGISTER
if choice == "Register":
    st.subheader("Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(email, password):
            st.success("Registration successful! Login now.")
        else:
            st.error("Email already exists!")

# LOGIN
elif choice == "Login":
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state.user = user
            st.success(f"Welcome, {email}!")
        else:
            st.error("Invalid credentials")

# LOGOUT
elif choice == "Logout":
    st.session_state.user = None
    st.success("Logged out successfully!")

# PROFILE MANAGEMENT
elif choice == "Profile" and st.session_state.user:
    st.subheader("Profile Management")
    email = st.text_input("New Email", value=st.session_state.user[1])
    password = st.text_input("New Password", type="password")
    if st.button("Update Profile"):
        update_user_profile(st.session_state.user[0], email, password)
        st.session_state.user = login_user(email, password)
        st.success("Profile updated successfully!")

    if st.button("Delete Account"):
        delete_user_account(st.session_state.user[0])
        st.session_state.user = None
        st.success("Account deleted successfully!")

# ADD RECIPE
elif choice == "Add Recipe" and st.session_state.user:
    st.subheader("Share a New Recipe")
    title = st.text_input("Recipe Title")
    ingredients = st.text_area("Ingredients")
    steps = st.text_area("Preparation Steps")
    category = st.selectbox("Category", ["Vegetarian", "Vegan", "Non-Vegetarian"])
    cooking_time = st.text_input("Cooking Time")
    image = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if st.button("Post Recipe"):
        if title and ingredients and steps:
            image_path = ""
            if image:
                if not os.path.exists("images"):
                    os.makedirs("images")
                image_path = f"images/{image.name}"
                with open(image_path, "wb") as f:
                    f.write(image.getbuffer())
            add_recipe(st.session_state.user[0], title, ingredients, steps, category, cooking_time, image_path)
            st.success("Recipe added!")
        else:
            st.warning("Please fill in all fields.")

# HOME / SHOW RECIPES
# Home / Show Recipes
elif choice == "Home":
    st.subheader("🍛 Latest Recipes")
    search_query = st.text_input("Search Recipes")
    if search_query:
        recipes = get_filtered_recipes(search_query)
    else:
        recipes = get_all_recipes()
    
    for recipe in recipes:
        recipe_id, title, ingredients, steps, category, cooking_time, img_path, email = recipe
        with st.expander(f"🍽️ {title} by {email}"):

            # Display image
            if img_path and os.path.exists(img_path):
                st.image(img_path, use_container_width=True)

            st.markdown(f"**Ingredients:**\n{ingredients}")
            st.markdown(f"**Steps:**\n{steps}")
            st.markdown(f"**Category:** {category} | **Cooking Time:** {cooking_time}")

            # Fetch reviews for this recipe
            cursor.execute("SELECT u.email, r.review_text, r.rating FROM reviews r JOIN users u ON r.user_id = u.id WHERE r.recipe_id = ?", (recipe_id,))
            reviews = cursor.fetchall()

            # Display reviews
            if reviews:
                st.markdown("**Reviews:**")
                for review in reviews:
                    reviewer_email, review_text, rating = review
                    st.markdown(f"**{reviewer_email}** rated it {rating}/5")
                    st.markdown(f"{review_text}")
                    st.markdown("---")
            else:
                st.markdown("No reviews yet for this recipe.")

            # Favourites and Reviews
            if st.session_state.user:
                if st.button(f"Add to Favourites", key=f"fav_{recipe_id}"):
                    add_favourite(st.session_state.user[0], recipe_id)
                    st.success("Recipe added to favourites!")

                rating = st.slider("Rate this recipe", 1, 5, key=f"rating_{recipe_id}")
                review_text = st.text_area("Leave a review", key=f"review_{recipe_id}")
                if st.button(f"Submit Review", key=f"submit_review_{recipe_id}"):
                    add_review(st.session_state.user[0], recipe_id, review_text, rating)
                    st.success("Review added!")

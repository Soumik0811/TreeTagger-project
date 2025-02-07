# Tree Tagger: Tree Classification and Climate-Based Afforestation Tool

Tree Tagger is a Flask-based web platform that aids afforestation efforts by utilizing machine learning to classify tree species based on uploaded leaf images. The platform integrates geolocation data, soil and climate analysis, and real-world user feedback to provide tree planting recommendations.

## Features

- **Tree Species Classification**: Uses a machine learning model to analyze uploaded leaf images and determine the tree species.
- **Geolocation-Based Tagging**: Identifies tree locations and maps them interactively.
- **Soil & Climate Data Integration**: Fetches data based on user location to recommend suitable trees if no tagged trees are found nearby.
- **Tree Tagging & Feedback System**: Allows users to tag trees and receive upvotes/downvotes for credibility.
- **Chatbot Assistance**: Provides tree care tips and planting recommendations.
- **Tree Conservation News**: Displays the latest updates on afforestation and conservation efforts.

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: Supabase (PostgreSQL)
- **Machine Learning**: TensorFlow/Keras (CNN-based leaf classification model)
- **APIs**: OpenWeather API (climate data), Supabase API (database integration)

---

## Installation and Setup

### 1. Clone the Repository

### 2. Create and Activate Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Set Up Supabase Database
Create a project on [Supabase](https://supabase.com/) and configure the following tables:

#### **Tables and Schema**

1. **users**
   - `id` (UUID, primary key)
   - `username` (VARCHAR, unique)
   - `email` (VARCHAR, unique)
   - `password_hash` (TEXT)
   - `created_at` (TIMESTAMP, default now())

2. **tree_tags**
   - `id` (UUID, primary key)
   - `user_id` (UUID, foreign key -> users.id)
   - `species` (VARCHAR)
   - `latitude` (FLOAT)
   - `longitude` (FLOAT)
   - `image_url` (TEXT)
   - `tagged_at` (TIMESTAMP, default now())

3. **tree_votes**
   - `id` (UUID, primary key)
   - `tag_id` (UUID, foreign key -> tree_tags.id)
   - `user_id` (UUID, foreign key -> users.id)
   - `vote` (INTEGER, 1 for upvote, -1 for downvote)
   - `voted_at` (TIMESTAMP, default now())

4. **conservation_news**
   - `id` (UUID, primary key)
   - `title` (TEXT)
   - `content` (TEXT)
   - `published_at` (TIMESTAMP, default now())

### 5. Configure Environment Variables
Create a `.env` file and add:
```sh
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_api_key
SECRET_KEY=your_flask_secret_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

### 6. Run the Flask Application
```sh
python app.py
```
By default, the app runs on `http://127.0.0.1:5000/`.

### 7. Access the Web App
- Visit `http://127.0.0.1:5000/` to start using Tree Tagger.
- Upload a leaf image to classify tree species.
- Explore the interactive tree map and get conservation news updates.


##UI images:
![image](https://github.com/user-attachments/assets/8e13a4d9-7f44-496f-8306-2c91a3f4bba9)

![image](https://github.com/user-attachments/assets/02e9b56f-4a2c-43ef-8b69-100824295310)

Link: https://tree-tagger.onrender.com/

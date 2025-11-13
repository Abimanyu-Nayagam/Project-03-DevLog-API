CREATE DATABASE IF NOT EXISTS devlog_db;

USE devlog_db;
-- Drop tables if they exist (for a clean start)
DROP TABLE IF EXISTS snippets;
DROP TABLE IF EXISTS entries;
DROP TABLE IF EXISTS users;

-- Create the users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(150) NOT NULL UNIQUE,
    password_hashed VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create the entries table
CREATE TABLE entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    tags VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create the snippets table
CREATE TABLE snippets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    code TEXT NOT NULL,
    description VARCHAR(255) NOT NULL,
    language VARCHAR(50) NOT NULL,
    tags VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert dummy users
INSERT INTO users (email, username, password_hashed) VALUES
('test@gmail.com', 'yshnyk', 'yshnyk@321'),
('john@example.com', 'john_doe', 'john123'),
('alice@example.com', 'alice_w', 'alice@456'),
('mark@example.com', 'markus', 'mark@789'),
('sara@example.com', 'sara_k', 'sara@999');

-- Insert dummy entries
INSERT INTO entries (title, content, tags, user_id) VALUES
('Daily Journal', 'Wrote some Flask APIs today.', 'flask,python,api', 1),
('Grocery List', 'Milk, Bread, Eggs, Butter', 'personal,list', 2),
('Travel Notes', 'Visited Goa. Amazing beaches!', 'travel,goa', 3),
('Workout Log', 'Pushups: 30, Squats: 40', 'fitness,health', 1),
('Book Summary', 'Summarized "Deep Work" by Cal Newport', 'books,productivity', 4);

-- Insert dummy snippets
INSERT INTO snippets (title, code, description, language, tags, user_id) VALUES
('Hello World in Python', 'print("Hello, World!")', 'Basic Python print example', 'Python', 'beginner,python', 1),
('Flask Route Example', '@app.route("/home")\ndef home():\n    return "Welcome!"', 'Simple Flask route example', 'Python', 'flask,api', 1),
('Bubble Sort', 'def bubble_sort(arr):\n    ...', 'Sorting algorithm using bubblesort', 'Python', 'algorithm,sorting', 2),
('Basic HTML Page', '<!DOCTYPE html><html><body><h1>Hello!</h1></body></html>', 'Simple HTML structure', 'HTML', 'frontend,html', 3),
('SQL Select', 'SELECT * FROM users WHERE id=1;', 'Fetch data from users table', 'SQL', 'database,mysql', 4),
('JS Alert', 'alert("Hello!");', 'Simple JavaScript alert example', 'JavaScript', 'frontend,js', 5);

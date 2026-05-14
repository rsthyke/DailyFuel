CREATE TABLE IF NOT EXISTS users (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT    NOT NULL,
    email        TEXT    NOT NULL UNIQUE,
    password     TEXT    NOT NULL,
    height       REAL,
    weight       REAL,
    age          INTEGER,
    gender       TEXT,
    calorie_goal REAL DEFAULT 2000
);

CREATE TABLE IF NOT EXISTS meals (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER NOT NULL REFERENCES users(id),
    date      TEXT    NOT NULL,
    meal_name TEXT    NOT NULL,
    calories  INTEGER NOT NULL
);

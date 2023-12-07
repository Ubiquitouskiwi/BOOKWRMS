/* OLD DB CREANUP */
DROP TABLE IF EXISTS author;

DROP TABLE IF EXISTS book;

DROP TABLE IF EXISTS user;

DROP TABLE IF EXISTS checkout_log;

DROP TABLE IF EXISTS login;

DROP TABLE IF EXISTS library;

DROP TABLE IF EXISTS library_book;

DROP TABLE IF EXISTS patron;

DROP TRIGGER IF EXISTS user_username_default_value;

/* TABLE CREATION */
/* table that has author information. OLID is ID for open library */
CREATE TABLE author (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    middle_name TEXT,
    last_name TEXT NOT NULL,
    olid TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE
);

/* table that holds book info. OLID is ID for open library */
CREATE TABLE book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    isbn INTEGER NOT NULL,
    illustration_url TEXT NOT NULL,
    olid TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (author_id) REFERENCES author (id),
    UNIQUE(isbn)
);

/* table that has user info. All users are admins who can add/edit/checkout books */
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (email)
);

/* table that holds login info. used for login */
CREATE TABLE login (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE(email)
);

CREATE TABLE checkout_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    patron_name TEXT NOT NULL,
    checkout_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    checkout_duration INTEGER NOT NULL,
    checkin_date TIMESTAMP,
    renew_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (book_id) REFERENCES book (id)
);

/* NOT USED: table that adds ability for more that one person to have a library */
CREATE TABLE library (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSe,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

/* NOT USED: table that marries books to the library */
CREATE TABLE library_book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    library_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE
);

/* NOT USED: table that holds patron data (people who use library) */
CREATE TABLE patron (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_Name TEXT NOT NULL,
    email TEXT NOT NULL,
    library_card_number INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE
);

/* TRIGER CREATION 
 CREATE TRIGGER user_username_default_value
 AFTER
 INSERT
 ON user FOR EACH ROW
 WHEN NEW.username IS NULL BEGIN
 UPDATE
 user
 SET
 username = NEW.first_name || NEW.last_name;
 
 END;*/
INSERT INTO login (username, password) VALUES ('admin', 'pass');
INSERT INTO user (username, first_name, last_name, library_card_number, is_admin) VALUES ('admin', 'test', 'account', 0, true);
INSERT INTO author (first_name, middle_name, last_name, olid) VALUES ('Alice', NULL, 'Hoffman', 'OL25149A');
INSERT INTO book (title, author_id, isbn, illustration_url, olid) VALUES ('The Museum Of Extraordinary Things A Novel', 1, 9781451693560, 'https://covers.openlibrary.org/b/id/7863421-L.jpg', 'OL26184511M');
INSERT INTO checkout_log (book_id, user_id, checkout_duration) VALUES (1, 2, 30);
INSERT INTO library (name, user_id) VALUES ('Test Library', 1);
INSERT INTO library_book (library_id, book_id) VALUES (1, 1);
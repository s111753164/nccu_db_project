CREATE TABLE books (
    `ISBN` INTEGER PRIMARY KEY,
    `title` TEXT,
    `author` TEXT,
    `category` TEXT,
    `version` TEXT
);

CREATE TABLE readers (
    `rname` TEXT,
    `ssn` TEXT PRIMARY KEY,
    `address` TEXT,
    `mail` TEXT,
    `phone` TEXT,
    `password` password
);

CREATE TABLE staffs (
    `sname` TEXT,
    `empid` TEXT PRIMARY KEY
);

-- CREATE TABLE publishers (
--     `publisher_id` INTEGER PRIMARY KEY ASC AUTOINCREMENT,
--     `pname` TEXT,
--     `YearOfPublication` TEXT
-- );

CREATE TABLE reports (
    `Reg_no` INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    `User_id` TEXT,
    `book_no` TEXT,
    `issue` DATETIME DEFAULT (datetime('now', 'localtime')),
    `return` DATETIME DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY(`User_id`) REFERENCES `readers`(`ssn`)
    FOREIGN KEY(`book_no`) REFERENCES `books`(`ISBN`)
);
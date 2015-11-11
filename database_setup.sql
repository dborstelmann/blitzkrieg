CREATE TABLE users (
    "id" serial PRIMARY KEY,
    "first_name" varchar(50) NOT NULL,
    "last_name" varchar(50) NOT NULL,
    "email" varchar(50) NOT NULL,
    "password" varchar(50) NOT NULL,
    CONSTRAINT unique_email UNIQUE (email)
);

CREATE TABLE instagram_user (
    "id" serial PRIMARY KEY,
    "user_id" serial NOT NULL,
    "username" varchar(50) NOT NULL,
    "full_name" varchar(50) NOT NULL
);

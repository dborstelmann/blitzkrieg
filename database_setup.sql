CREATE TABLE users (
    "id" serial PRIMARY KEY,
    "first_name" text NOT NULL,
    "last_name" text NOT NULL,
    "email" text NOT NULL,
    "password" text NOT NULL,
    "has_instagram" boolean NOT NULL DEFAULT FALSE,
    "has_facebook" boolean NOT NULL DEFAULT FALSE,
    "has_twitter" boolean NOT NULL DEFAULT FALSE,
    CONSTRAINT unique_email UNIQUE (email)
);

CREATE TABLE instagram_user (
    "id" varchar(50) PRIMARY KEY,
    "user_id" serial NOT NULL,
    "username" text NOT NULL,
    "full_name" text NOT NULL,
    "profile_picture" text,
    "access_token" text NOT NULL
);

CREATE TABLE twitter_user (
    "id" varchar(50) PRIMARY KEY,
    "user_id" serial NOT NULL,
    "screen_name" text NOT NULL,
    "access_token" text NOT NULL,
    "access_token_secret" text NOT NULL
);

CREATE TABLE single_day_instagram (
    "created_datetime" text PRIMARY KEY
)

CREATE TABLE feed_data (
    "id" serial PRIMARY KEY,
    "created_datetime" text NOT NULL,
    "user_id" serial NOT NULL,
    "api_service" text
)

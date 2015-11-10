CREATE TABLE "user" (
    "id" serial PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "email" varchar(50) NOT NULL,
    "password" varchar(50) NOT NULL
);

CREATE TABLE "instagram_user" (
    "id" serial PRIMARY KEY,
    "user_id" serial NOT NULL,
    "username" varchar(50) NOT NULL,
    "full_name" varchar(50) NOT NULL
);

DROP TABLE IF EXISTS staging_events_table;
DROP TABLE IF EXISTS staging_songs_table;
DROP TABLE IF EXISTS songplay_table;
DROP TABLE IF EXISTS user_table;
DROP TABLE IF EXISTS song_table;
DROP TABLE IF EXISTS artist_table;
DROP TABLE IF EXISTS time_table;


CREATE TABLE staging_events_table (
    "artist" VARCHAR(255),
    "auth" VARCHAR(25),
    "firstName" VARCHAR(50),
    "gender" VARCHAR(2),
    "itemInSession" INTEGER,
    "lastName" VARCHAR(50),
    "length" DOUBLE PRECISION,
    "level" VARCHAR(10),
    "location" VARCHAR(255),
    "method" VARCHAR(10),
    "page" VARCHAR(25),
    "registration" BIGINT,
    "sessionId" INTEGER,
    "song" VARCHAR(255),
    "status" INTEGER,
    "ts" BIGINT,
    "userAgent" VARCHAR(255),
    "userId" INTEGER
);



CREATE TABLE staging_songs_table (
    num_songs INTEGER,
    artist_id VARCHAR(255),
    artist_latitude FLOAT,
    artist_longitude FLOAT,
    artist_location VARCHAR(255),
    artist_name VARCHAR(255),
    song_id VARCHAR(255),
    title VARCHAR(255),
    duration FLOAT,
    year INTEGER
);


CREATE TABLE songplay_table (
    songplay_id INTEGER IDENTITY(0,1) PRIMARY KEY,
    start_time TIMESTAMP NOT NULL sortkey,
    user_id INTEGER NOT NULL,
    level VARCHAR(10),
    song_id VARCHAR(255) distkey,
    artist_id VARCHAR(255),
    session_id INTEGER,
    location VARCHAR(255),
    user_agent VARCHAR(255)
);



CREATE TABLE user_table (
    userid INTEGER NOT NULL PRIMARY KEY sortkey,
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    gender VARCHAR(2),
    level VARCHAR(10)
);



CREATE TABLE song_table (
    song_id VARCHAR(255) NOT NULL PRIMARY KEY  sortkey,
    title VARCHAR(255),
    artist_id VARCHAR(255),
    year INTEGER,
    duration FLOAT
);



CREATE TABLE artist_table (
    artist_id VARCHAR(255) NOT NULL PRIMARY KEY sortkey,
    artist_name VARCHAR(255) NOT NULL,
    artist_location VARCHAR(255),
    artist_latitude FLOAT,
    artist_longitude FLOAT
);



CREATE TABLE time_table (
    start_time TIMESTAMP NOT NULL PRIMARY KEY sortkey,
    hour INTEGER NOT NULL,
    day INTEGER NOT NULL,
    week INTEGER NOT NULL,
    month INTEGER NOT NULL,
    year INTEGER NOT NULL,
    weekday INTEGER NOT NULL
);

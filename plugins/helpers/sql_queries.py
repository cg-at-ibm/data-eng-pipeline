class SqlQueries:

    # DROP TABLES

    staging_events_table_drop = "DROP TABLE IF EXISTS staging_events_table;"
    staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs_table;"
    songplay_table_drop = "DROP TABLE IF EXISTS songplay_table;"
    user_table_drop = "DROP TABLE IF EXISTS user_table;"
    song_table_drop = "DROP TABLE IF EXISTS song_table;"
    artist_table_drop = "DROP TABLE IF EXISTS artist_table;"
    time_table_drop = "DROP TABLE IF EXISTS time_table;"


    LOG_DATA =''
    DWH_ROLE_ARN =''
    LOG_JSON =''
    SONG_DATA = ''

    # CREATE TABLES
    staging_events_table_create= ("""
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
    """)

    staging_songs_table_create = ("""
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
    """)

    songplay_table_create = ("""
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
    """)

    user_table_create = ("""
    CREATE TABLE user_table (
        userid INTEGER NOT NULL PRIMARY KEY sortkey,
        firstname VARCHAR(50),
        lastname VARCHAR(50),
        gender VARCHAR(2),
        level VARCHAR(10)
    );
    """)

    song_table_create = ("""
    CREATE TABLE song_table (
        song_id VARCHAR(255) NOT NULL PRIMARY KEY  sortkey,
        title VARCHAR(255),
        artist_id VARCHAR(255),
        year INTEGER,
        duration FLOAT
    );
    """)

    artist_table_create = ("""
    CREATE TABLE artist_table (
        artist_id VARCHAR(255) NOT NULL PRIMARY KEY sortkey,
        artist_name VARCHAR(255) NOT NULL,
        artist_location VARCHAR(255),
        artist_latitude FLOAT,
        artist_longitude FLOAT
    );
    """)

    time_table_create = ("""
    CREATE TABLE time_table (
        start_time TIMESTAMP NOT NULL PRIMARY KEY sortkey,
        hour INTEGER NOT NULL,
        day INTEGER NOT NULL,
        week INTEGER NOT NULL,
        month INTEGER NOT NULL,
        year INTEGER NOT NULL,
        weekday INTEGER NOT NULL
    );
    """)

    # STAGING TABLES

    staging_events_copy = ("""
    copy staging_events_table from '{}'
    credentials 'aws_iam_role={}'
    JSON '{}'
    region 'us-west-2';
    """).format(LOG_DATA, DWH_ROLE_ARN, LOG_JSON)

    staging_songs_copy = ("""
    copy staging_songs_table from '{}'
    credentials 'aws_iam_role={}'
    FORMAT AS JSON 'auto'
    region 'us-west-2';
    """).format(SONG_DATA, DWH_ROLE_ARN)

    # FINAL TABLES


    songplay_table_insert = ("""
    INSERT INTO songplay_table (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT timestamp 'epoch' + "ts"/1000 * interval '1 second', "userId", "level", song_id, artist_id, "sessionId", "location", "userAgent"
    FROM staging_events_table
    LEFT JOIN staging_songs_table 
    ON staging_events_table."song" = staging_songs_table.title AND staging_events_table."artist" = staging_songs_table.artist_name
    WHERE "page" = 'NextSong';
    """)


    user_table_insert = ("""
    INSERT INTO user_table (userid, firstname, lastname, gender, level)
    SELECT DISTINCT "userId", "firstName", "lastName", "gender", "level"
    FROM staging_events_table
    WHERE "userId" is NOT NULL;
    """)

    song_table_insert = ("""
    INSERT INTO song_table (song_id, title, artist_id, year, duration)
    SELECT DISTINCT song_id, title, artist_id, year, duration
    FROM staging_songs_table
    WHERE "song_id" is NOT NULL;
    """)

    artist_table_insert = ("""
    INSERT INTO artist_table (artist_id, artist_name, artist_location, artist_latitude, artist_longitude)
    SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
    FROM staging_songs_table
    WHERE "artist_id" is NOT NULL;
    """)

    time_table_insert = ("""
    INSERT INTO time_table (start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT
        timestamp 'epoch' + ts/1000 * interval '1 second' as start_time, 
        EXTRACT(HOUR FROM start_time), 
        EXTRACT(DAY FROM start_time),
        EXTRACT(WEEK FROM start_time), 
        EXTRACT(MONTH FROM start_time),
        EXTRACT(YEAR FROM start_time), 
        EXTRACT(DOW FROM start_time)
    FROM staging_events_table;
    """)

    # QUERY LISTS

    create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
    drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
    copy_table_queries = [staging_events_copy, staging_songs_copy]
    insert_table_queries = [user_table_insert, song_table_insert, artist_table_insert, time_table_insert,songplay_table_insert]
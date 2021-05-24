import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
        
        CREATE TABLE staging_events (
                event_id INT IDENTITY(0,1),
                artist_name VARCHAR(255),
                auth VARCHAR(50),
                first_name VARCHAR(255),
                gender  VARCHAR(1),
                item_in_session	INTEGER,
                last_name VARCHAR(255),
                length DOUBLE PRECISION,
                level VARCHAR(50),
                location VARCHAR(255),
                method VARCHAR(25),
                page VARCHAR(35),
                registration VARCHAR(50),
                session_id INTEGER,
                song_title VARCHAR(255),
                status INTEGER,
                ts VARCHAR(50),
                user_agent TEXT,
                user_id VARCHAR(100),
                PRIMARY KEY (event_id)
        );
    
""")

staging_songs_table_create = ("""
        CREATE TABLE staging_songs (
            song_id VARCHAR(100),
            num_songs INTEGER,
            artist_id VARCHAR(100),
            artist_latitude FLOAT,
            artist_longitude FLOAT,
            location VARCHAR(255),
            artist_name VARCHAR(255),
            title VARCHAR(255),
            duration FLOAT,
            year INTEGER,
            PRIMARY KEY (song_id)
        );
        
""")

songplay_table_create = ("""
            
        CREATE TABLE songplays (
                songplay_id        INTEGER IDENTITY(0,1) PRIMARY KEY,
                start_time         TIMESTAMP,
                user_id            VARCHAR(100),
                level              VARCHAR(100),
                song_id            VARCHAR(100),
                artist_id          VARCHAR(100),
                session_id         INTEGER,
                location           VARCHAR(100),
                user_agent         TEXT
        
        )

""")

user_table_create = ("""

        CREATE TABLE users (
                user_id    VARCHAR(100) PRIMARY KEY,
                first_name VARCHAR(255),
                last_name  VARCHAR(255),
                gender     VARCHAR(1),
                level      VARCHAR(5)
        )
        
        
""")

song_table_create = ("""
            
            CREATE TABLE songs (
                song_id    VARCHAR(100) NOT NULL PRIMARY KEY,
                title      VARCHAR(255),
                artist_id  VARCHAR(100),
                year       INTEGER,
                duration   FLOAT 
            );
   
""")

artist_table_create = ("""
                
                CREATE TABLE artists (
                    artist_id VARCHAR(100) PRIMARY KEY,
                    artist_name VARCHAR(255),
                    location VARCHAR(255),
                    artist_latitude FLOAT,
                    artist_longitude FLOAT
                );

""")

time_table_create = ("""

            CREATE TABLE time(
                    
                    start_time    TIMESTAMP,
                    hour          INTEGER,
                    day           INTEGER,
                    week          INTEGER,
                    month         INTEGER,
                    year          INTEGER,
                    weekday       INTEGER
            );
""")

# STAGING TABLES

staging_events_copy = ("""
            
        copy staging_events from {} iam_role {} json {};

""").format(config.get('S3', 'LOG_DATA'), config.get('IAM_ROLE', 'ARN'), config.get('S3', 'LOG_JSONPATH'))

staging_songs_copy = ("""

        copy staging_songs from {} iam_role {} json 'auto'

""").format(config.get('S3', 'SONG_DATA', ), config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES

songplay_table_insert = ("""

        INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
        SELECT
            TIMESTAMP 'EPOCH' + SE.ts/1000 * interval '1 second' as start_time,
            SE.user_id,
            SE.level,
            SS.song_id,
            SS.artist_id,
            SE.session_id,
            SE.location,
            SE.user_agent
    
        FROM
            staging_events SE, staging_songs SS
        WHERE 
            SE.artist_name = SS.artist_name
            AND SE.song_title = SS.title
            AND SE.page ='NextSong'
        
""")

user_table_insert = ("""
        INSERT INTO users (user_id, first_name, last_name, gender, level)
            SELECT 
                DISTINCT user_id, first_name, last_name, gender, level
            FROM staging_events
            WHERE page = 'NextSong'
            
""")

song_table_insert = ("""

        INSERT INTO songs (song_id, title, artist_id, year, duration)
            SELECT 
                DISTINCT song_id, title, artist_id, year, duration
            FROM staging_songs
                
""")

artist_table_insert = ("""

        INSERT INTO artists (artist_id, artist_name, location, artist_latitude, artist_longitude)
            SELECT 
                DISTINCT artist_id, artist_name, location, artist_latitude, artist_longitude
            FROM staging_songs
        
""")

time_table_insert = ("""

        INSERT INTO time (start_time, hour, day, week, month, year, weekday)
            SELECT 
                start_time, 
                extract(hour from start_time),
                extract(day from start_time),
                extract(week from start_time),
                extract(month from start_time),
                extract(year from start_time),
                extract(dayofweek from start_time)
            FROM songplays
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

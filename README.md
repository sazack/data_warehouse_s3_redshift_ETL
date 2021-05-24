# Udacity Data Warehouse Project

### Introduction
<p> This project is a part of Udacity's Data Engineering Nanodegree program where we are impersonating a data engineer at a music streaming company called __*Sparkify*__. Sparkify has been growing rapidly amongst in terms of their userbase and are looking to migrare their data into cloud. In this project we build an ETL Piple line that reads the data from an __Amazon S3 bucket__ and stages it before storing them to a database hosted on __AWS RedShift__.
<br>

### Data

Our datasets are stored in two different categories: <br>
<ul>
    <li> Song data: s3://udacity-dend/song_data </li>
    <li> Log data: s3://udacity-dend/log_data </li>
</ul>

> __Here's an example of JSON song data__:

> {"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

> __ Here's an example of log data__:
> <img src="https://video.udacity-data.com/topher/2019/February/5c6c3ce5_log-data/log-data.png" alt="logs dataframe screenshot">

 
 ### Database Design & Schema
 
 Before doing anything else we'd need to copy the data from our S3 buckets and store it into the staging table from which we can fill our fact and dimennsion tables. <br>
 
 We'd create following two staging tables
 
 __staging_events__
 
 Column | DataType | Constraint
 --- | --- | ---
 event_id | Integer | PRIMARY, IDENTITY
 artist_name | VARCHAR
 auth | VARCHAR |
 first_name | VARCHAR
 gender | VARCHAR
 item_in_session | Integer,
 last_name | VARCHAR
 length | Double
 level | VARCHAR
 location | VARCHAR
 method | VARCHAR
 page | VARCHAR
 registration | VARCHAR
 session_id | Integer
 song_title | VARCHAR
 status | INTEGER
 ts | VARCHAR
 user_agent | VARCHARR
 user_id | VARCHAR
 
 __staging_songs__
 
 Column | DataType | Constraint
 --- | --- | ---
 song_id | INTEGER | PRIMARY, IDENTITY
 num_songs | INTEGER | 
 artist_id | VARCHAR
 artist_latitude | FLOAT |
 artist_longitude | FLOAT | 
 location | VARCHAR
 artist_name | VARCHAR | 
 title | VARCHAR
 duration | FLOAT
 year | INTEGER
 
 user_agent | VARCHAR
 

 
 Next up we'd have to develope a database on a star schema. We'd have a Fact table *songplays* and  dimension <br/>
 tables *users*, *artists*, *songs*, *time*. 
 
 Songplays
 
 Column | DataType | Constraint
 --- | --- | ---
 songplay_id | INTEGER | PRIMARY, IDENTITY
 start_time | TIMESTAMP | 
 user_id | VARCHAR |
 level | VARCHAR
 song_id | VARCHAR
 artist_id | VARCHAR
 session_id | INTEGER
 location | VARCHAR
 user_agent | VARCHAR
 
 
 Dimesion Tables:
 
 users
 
  Column | DataType | Constraint
 --- | --- | ---
 user_id | VARCHAR | PRIMARY
 first_name | VARCHAR
 last_name | VARCHAR
 gender | VARCHAR
 level | VARCHAR
 
 
 Songs
 
  Column | DataType | Constraint 
 --- | --- | ---
 song_id | VARCHAR | NOT NULL, PRIMARY
 title | VARCHAR
 artist_id | VARCHAR | 
 year | INTEGER
 duration | FLOAT
 
 Artists
 
  Column | DataType | Constraint
 --- | --- | ---
 artist_id | VARCHAR | PRIMARY
 artist_name | VARCHAR
 location | VARCHAR
 artist_latitude | FLOAT
 artist_longitude | FLOAT
 
 Time
 
  Column | DataType | Constraint
 --- | --- | ---
 start_time | TIMESTAMP | PRIMARY
 hour | INTEGER
 day | INTEGER
 week | INTEGER
 month | INTEGER
 year | INTEGER
 weekday | INTEGER


## Executing the Script

<ul>

<li> Update Dwh.cfg file with the configuration for your redis cluster, roles and other aws config </li>
<li> Run create_tables.py to create the tables in the cluster </li>
<li> Run etl.py to load the data into the respective tables </li>

</ul>




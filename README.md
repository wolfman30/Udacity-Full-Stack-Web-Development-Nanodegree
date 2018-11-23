
Python 3 used in this project 

Setup Steps: 

(1) Make sure newsdata.sql is in current working directory

(2) Run 'psql -d news -f newsdata.sql' to create news database

(3) Run 'psql -d news' to connect to news database

(4) Create the two views below:

       Creates View titled 'authors_articles':

       CREATE VIEW authors_articles AS
       SELECT authors.name, articles.title 
       FROM authors, articles
       WHERE articles.author=authors.id; 


Creates View titled 'articles_views":

       CREATE VIEW articles_views AS
       SELECT CASE
              WHEN path LIKE '%bad-things%' THEN 'Bad things gone, say good people' 
              WHEN path LIKE '%balloon-goons%' THEN 'Balloon goons doomed' 
              WHEN path LIKE '%bears-love-berries%' THEN 'Bears love berries, alleges bear' 
              WHEN path LIKE '%candidate%' THEN 'Candidate is jerk, alleges rival' 
              WHEN path LIKE '%goats-eat%' THEN 'Goats eat Google''s lawn' 
              WHEN path LIKE'%media-obsessed%' THEN 'Media obsessed with bears' 
              WHEN path LIKE '%trouble-for%' THEN 'Trouble for troubled troublemakers' 
              WHEN path LIKE '%there-are%' THEN 'There are a lot of bears' END AS article_title, count(*) number_of_views 
       FROM log 
       GROUP BY 1 
       ORDER BY number_of_views DESC;

(5)Run 'python newer_newsdata_to_be_graded.py' in terminal assuming the file is in the current working directory  

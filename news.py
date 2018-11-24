#!/usr/bin/env python3

import psycopg2 as psy

q1 = '--What are the most popular three articles of all time?--'

query1 = """
            SELECT FORMAT('---->%s: %s views', title, count(*)) 
            FROM articles, log 
            WHERE CONCAT('/article/', articles.slug) = log.path 
            GROUP BY title
            ORDER BY count(*) DESC
            LIMIT 3;
        """

q2 = '--Who are the most popular article authors of all time?--'

query2 = """
            SELECT 
                FORMAT('---->%s: %s views', authors.name, sum(num_of_views))
            FROM authors
            JOIN articles
            ON authors.id = articles.author
            JOIN 
                (SELECT title, count(*) num_of_views 
                 FROM articles, log 
                 WHERE CONCAT('/article/', articles.slug) = log.path 
                 GROUP BY 1) AS articles_views
            ON articles.title = articles_views.title
            GROUP BY authors.name
            ORDER BY sum(num_of_views) DESC;
        """

q3 = '--On which days did more than 1% of requests lead to errors?--'

query3 = """
        SELECT 
            FORMAT('---->%s: %s%% errors', day1, 
                ROUND(num_errs/cast(total_requests as decimal)*100, 2)) 
        FROM 
            (SELECT TO_CHAR(time, 'Mon DD, YYYY') 
                AS day1, count(status) num_errs 
            FROM log                                                        
            WHERE status = '404 NOT FOUND'                                   
            GROUP BY 1) AS errors_per_day, 
            (SELECT TO_CHAR(time, 'Mon DD, YYYY') AS day2, 
                                        count(*) total_requests 
            FROM log 
            GROUP BY 1) AS requests_by_day 
        WHERE day1 = day2 
        GROUP BY day1, num_errs/cast(total_requests as decimal)*100
        HAVING num_errs/cast(total_requests as decimal)*100 > 1.0;
        """


class Newsdata():

    def __init__(self):

        #connects to database "news"
        try:
            self.db = psy.connect(database="news")
        execpt psy.DatabaseError, e: 
            print("Could not connect to the database 'news'")

        #sets up the database for executing queries and fetching the output 
        self.c = self.db.cursor() 

    def execute_fetch(self, query):
        self.c.execute(query)
        output = self.c.fetchall()
        for i in output:
            print(i[0])
        print('\n')
        return output
    
    def close(self):
        return self.db.close()


if __name__ == '__main__':
    
    #creates class instance on which we can call the three defined methods
    news_crunchor = Newsdata()
        
    #three calls to three separate methods of the Newsdata 
    # class to get the desired output
    print(q1)
    news_crunchor.execute_fetch(query1)
    
    print(q2)
    news_crunchor.execute_fetch(query2)
    
    print(q3)
    news_crunchor.execute_fetch(query3)

    #closes the database
    news_crunchor.close()

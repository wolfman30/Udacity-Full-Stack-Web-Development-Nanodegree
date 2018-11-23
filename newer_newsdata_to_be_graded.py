#python 3

#author_views() only works after creating views articles_views and authors_articles detailed in the README.md

import psycopg2 as psy

"""1. What are the most popular three articles of all time? """

class Newsdata():
    
    def __init__(self):
        self.db = psy.connect(database = "news") #connects to database "news"
        self.c = self.db.cursor() #sets up the database for executing queries and fetching the output
        
    def top3_articles(self):

        query = "SELECT CASE \
                        WHEN path LIKE '%bad-things%' THEN 'Bad things gone, say good people' \
                        WHEN path LIKE '%balloon-goons%' THEN 'Balloon goons doomed' \
                        WHEN path LIKE '%bears-love-berries%' THEN 'Bears love berries, alleges bear' \
                        WHEN path LIKE '%candidate%' THEN 'Candidate is jerk, alleges rival' \
                        WHEN path LIKE '%goats-eat%' THEN 'Goats eat Google''s lawn' \
                        WHEN path LIKE'%media-obsessed%' THEN 'Media obsessed with bears' \
                        WHEN path LIKE '%trouble-for%' THEN 'Trouble for troubled troublemakers' \
                        WHEN path LIKE '%there-are%' THEN 'There are a lot of bears' END AS article_title, count(*) number_of_views \
                FROM log \
                GROUP BY 1 \
                ORDER BY number_of_views DESC \
                LIMIT 4;"

        self.c.execute(query)#executes the query in the database
        output = self.c.fetchall()[1:] #the first and largest proportion of logs have only a root path,  
                                #where people only visited the home page without viewing any articles
        output = ["'" + str(i) + "'" + "--" + str(int(j)) + " views" for i, j in output]
        print(output)
        print('\n')

    """2. Who are the most popular article authors of all time? """

    def author_views(self):

        query = "SELECT name, sum(number_of_views) total_article_views \
                FROM articles_views, authors_articles \
                WHERE articles_views.article_title = authors_articles.title \
                GROUP BY name \
                ORDER BY total_article_views DESC;"
        self.c.execute(query)
        output = self.c.fetchall()
        #python post-processing that converts list of tuples into list of strings
        output = [i + " -- " + str(int(j)) + ' views' for i, j in output]
        print(output)
        print('\n')
        
    """3. On which days did more than 1% of requests lead to errors? """

    def erroneous_days(self):

        query = """
                SELECT day1, num_errs/cast(total_requests as decimal)*100 AS daily_err_pct 
                FROM 
                    (SELECT DATE_TRUNC('day', time) AS day1, count(status) num_errs 
                    FROM log                                                        
                    WHERE status = '404 NOT FOUND'                                   
                    GROUP BY DATE_TRUNC('day', time)) AS errors_per_day, 
                    (SELECT DATE_TRUNC('day', time) AS day2, count(*) total_requests 
                    FROM log 
                    GROUP BY DATE_TRUNC('day', time)) AS requests_by_day 
                WHERE day1 = day2 
                GROUP BY 1, 2 
                HAVING num_errs/cast(total_requests as decimal)*100 > 1.0;
                """

        self.c.execute(query)
        output = self.c.fetchall()
        output = [i.strftime('%m-%d-%Y') + " -- " + str(round(float(j), 2)) + "% errors" for i, j in output]#converts to list of strings
        print(output)
        print('\n')

    def close(self):
        return self.db.close()

news_crunchor = Newsdata()#creates class instance on which we can call the three defined methods
    
#three calls to three separate methods of the Newsdata class to get the desired output
news_crunchor.top3_articles()
news_crunchor.author_views()
news_crunchor.erroneous_days()

#closes the database
news_crunchor.close()

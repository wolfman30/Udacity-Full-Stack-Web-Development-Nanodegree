import psycopg2 as psy

def top3_articles():
    db = psy.connect(database = "news")
    c = db.cursor()
    query = "SELECT CASE \
                    WHEN path LIKE '%bad-things%' THEN 'Bad things gone, say good people' \
                    WHEN path LIKE '%balloon-goons%' THEN 'Balloon goons doomed' \
                    WHEN path LIKE '%bears-love-berries%' THEN 'Bears love berries, alleges bear' \
                    WHEN path LIKE '%candidate%' THEN 'Candidate is jerk, alleges rival' \
                    WHEN path LIKE '%goats-eat%' THEN 'Goats eat Googles lawn' \
                    WHEN path LIKE'%media-obsessed%' THEN 'Media obsessed with bears' \
                    WHEN path LIKE '%trouble-for%' THEN 'Trouble for troubled troublemakers' \
                    WHEN path LIKE '%there-are%' THEN 'There are a lot of bears' END AS article_title, count(*) number_of_views \
            FROM log \
            GROUP BY 1 \
            ORDER BY number_of_views DESC \
            LIMIT 4;"
    c.execute(query)
    output = c.fetchall()[1:] #the first and largest proportion of logs have only a root path,  
                              #where people only visited the home page without viewing any articles
    output = [(i, str(int(j)) + ' views') for i, j in output]
    print(output)
    db.close()
    return output


top3_articles()


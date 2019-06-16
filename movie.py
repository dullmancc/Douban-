class movie_info:
    def __init__(self,movie_id,movie_title,actors,regions,release_date,cover_url,score,rating,vote_count,url,synopsis=''):
        self.movie_id = movie_id,
        self.movie_title = movie_title
        self.actors = actors
        self.regions = regions
        self.release_date = release_date
        self.cover_url = cover_url
        self.score = score
        self.rating = rating
        self.vote_count = vote_count
        self.url =url
        self.synopsis = synopsis
        self.movie_id = self.movie_id[0]

    def set_synopsis(self,synopsis):
        self.synopsis = synopsis

    def insert(self):
        sql = "INSERT INTO `movie_info`(`movie_id`,`movie_title`,`actors`,`regions`,`release_date`,`synopsis`,`cover_url`,`score`,`rating`,`vote_count`,`url`)" \
              " VALUES('%s','%s','%s','%s','%s','%s','%s','%f','%d','%ld','%s')"%\
              (self.movie_id,self.movie_title,self.actors,self.regions,self.release_date,self.synopsis,self.cover_url,self.score,self.rating,self.vote_count,self.url)

        return sql
    
    def update_synopsis(self):
        sql = "UPDATE `movie_info` SET synopsis = \"%s\" WHERE movie_id = '%s'"%(self.synopsis,self.movie_id)
        return sql

class movie_type:
    def __init__(self,type_id,movie_id,rank):
        self.type_id = type_id
        self.movie_id = movie_id
        self.rank = rank

    def insert(self):
        sql  = "INSERT INTO `movie_type`(`type_id`,`movie_id`,`rank`)" \
               "VALUES('%d','%s','%d')"%\
               (self.type_id,self.movie_id,self.rank)
        return sql

class type_info:
    def __init__(self,type_id,type_name):
        self.type_id = type_id
        self.type_name = type_name

    def insert(self):
        sql = "INSERT INTO `type_info`(`type_id`,`type_name`)" \
              "VALUES('%d','%s')"%\
              (self.type_id,self.type_name)
        return sql

class hot_topic:
    def __init__(self,topic_id,topic_name,label,card_subtitle,participant_count,post_count,subscription_count,url,movie_id):
        self.topic_id =topic_id
        self.topic_name =topic_name
        self.label =label
        self.card_subtitle =card_subtitle
        self.participant_count =participant_count
        self.post_count =post_count
        self.subscription_count = subscription_count
        self.url = url
        self.movie_id = movie_id

    def insert(self):
        sql  = "INSERT INTO `hot_topic`" \
               "(`topic_id`,`topic_name`,`label`,`card_subtitle`,`participant_count`,`post_count`,`subscription_count`,`url`,`movie_id`)" \
               "VALUES ('%d','%s','%s','%s','%d','%d','%d','%s','%s')"%\
               (self.topic_id,self.topic_name,self.label,self.card_subtitle,self.participant_count,self.post_count,self.subscription_count,self.url,self.movie_id)
        return sql

class hot_comment:
    def __init__(self,comment_id,content,totalcount,useful_count,useless_count,movie_id):
        self.comment_id =comment_id
        self.content =content
        self.totalcount = totalcount
        self.useful_count =useful_count
        self.useless_count =useless_count
        self.movie_id =movie_id

    def insert(self):
        sql = "INSERT INTO `hot_comment`" \
              "(`comment_id`,`content`,`totalcount`,`useful_count`,`useless_count`,`movie_id`)" \
              "VALUES ('%ld','%s','%d','%d','%d','%s')"%\
              (self.comment_id,self.content,self.totalcount,self.useful_count,self.useless_count,self.movie_id)
        return sql


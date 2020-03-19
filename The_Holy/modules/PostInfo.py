class PostInfo:
    def __init__(self):
        self.group_id          = ""
        self.post_id           = ""
        self.post_owner_id     = ""
        self.post_content      = ""
        self.is_share          = False              # True: if this post shares an another post, False: otherwise
        self.post_comment_num  = 0
        self.post_reaction_num = 0
        self.post_share_num    = 0
        self.score             = 0
        self.date_crawl        = None
        self.date_post         = None
        self.post_comments     = []
        '''
        the structure of comment:
        {
            comment_owner_id:       a string
            comment_content:        a string
            comment_tags:           a list of tagged users
            comment_replies: [
                {
                    reply_user: 
                    reply_comment:
                    reply_tag:
                }
            ]
        }
        '''


    def get_group_id(self):
        return self.group_id

    def get_post_id(self):
        return self.post_id

    def get_post_owner_id(self):
        return self.post_owner_id

    def get_post_content(self):
        return self.post_content
    
    def get_is_share(self):
        return self.is_share

    def get_post_comment_num(self):
        return self.post_comment_num

    def get_post_reaction_num(self):
        return self.post_reaction_num

    def get_post_share_num(self):
        return self.post_share_num

    def get_score(self):
        self.score = self.post_comment_num + self.post_reaction_num + self.post_share_num
        return self.score

    def get_date_crawl(self):
        return self.date_crawl

    def get_date_post(self):
        return self.date_post



    def get_post_comments(self):
        return self.post_comments

    def set_group_id(self, group_id):
        self.group_id = group_id

    def set_post_id(self, post_id):
        self.post_id = post_id

    def set_post_owner_id(self, post_owner_id):
        self.post_owner_id = post_owner_id

    def set_post_content(self, post_content):
        self.post_content = post_content

    def set_is_share(self, is_share):
        self.is_share = is_share

    def set_post_comment_num(self, post_comment_num):
        self.post_comment_num = post_comment_num

    def set_post_reaction_num(self, post_reaction_num):
        self.post_reaction_num = post_reaction_num

    def set_post_share_num(self, post_share_num):
        self.post_share_num = post_share_num    

    def set_date_crawl(self, date_crawl):
        self.date_crawl = date_crawl

    def set_date_post(self, date_post):
        self.date_post = date_post


    
    def add_comment(self, comment_owner_id, comment_content, comment_tags, comment_replies):
        self.post_comments.append({
            'comment_owner_id': comment_owner_id,
            'comment_content' : comment_content,
            'comment_tags'    : comment_tags,
            'comment_replies' : comment_replies
        })
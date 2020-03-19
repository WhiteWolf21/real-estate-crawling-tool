# -*- coding: utf-8 -*-

from re import findall
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from datetime import datetime

from modules.PostInfo import PostInfo
from modules.data_backup.store_data import store_data

re_group_member  = r"member_id="                        # regex string to find whether the post's owner is group member
re_post_owner_id = r"member_id=(\d+)"                   # regex string to find the id of post's owner

re_group_post_id = r"groups\/(.+)\/permalink\/(.+)\/"   #regex string to find the group name and post id

re_comm_user_id  = r"id=(.+)"


def crawl_comm(signin_driver, links):
    """Crawl users' post and comment

    :Args:
     - links - link of posts found

    :Returns:
   """

    # this list contains info of posts
    posts_info = []


    for link in links:       
        signin_driver.get(link)


        # ############## TESTING MODULE ###############
        # print(signin_driver.page_source)
        # signin_driver.quit()
        # exit(1)
        # ############## TESTING MODULE ###############

        test = signin_driver.find_elements_by_xpath("//h5//a[1]")
        if test == []:
            continue

        # user_ajax = signin_driver.find_element_by_tag_name('h5').find_element_by_tag_name('a').get_attribute('ajaxify')
        user_ajax = signin_driver.find_element_by_xpath("//h5//a[1]").get_attribute("ajaxify")

        if user_ajax == None:
            continue

        if len(findall(re_group_member, user_ajax)) == 0:
            # the user is not group member
            continue

        # check if this post is sharing another post which is not available
        try:
            signin_driver.find_element_by_xpath("//div[@class='mbs _6m6 _2cnj _5s6c']").text
            continue
        except NoSuchElementException:
            pass

        # check if the post shares another post or link
        # if post shares a link, ignore the post
        # if post share another post which is useful (the shared post has infomation extracted by API NLP)
        is_share = False
        try:
            check_share = signin_driver.find_element_by_xpath("//span[@class='fcg']").get_attribute('innerHTML')
            if len(findall(r"shared", check_share)) > 0:
                if len(findall(r"\>(post)\<", check_share)) > 0:
                    # this post is sharing another post
                    is_share = True
                else:
                    # this post shares nonsense thing
                    continue
        except NoSuchElementException:
            pass


        post_info = PostInfo()


        # ############### TESTING MODULE ###############
        # print(signin_driver.page_source)
        # signin_driver.quit()
        # exit(1)
        # ############### TESTING MODULE ###############


        # assign basic info for post
        try:
            tmp = findall(re_group_post_id, link)[0]
        except IndexError:
            # link is not valid
            continue
            
        post_info.set_group_id(tmp[0])
        post_info.set_post_id(tmp[1])
        post_info.set_post_owner_id(findall(re_post_owner_id, user_ajax)[0])
        post_info.set_date_crawl(datetime.now().isoformat())


        # assign date the post is published
        try:
            datetime_str = signin_driver.find_element_by_xpath("//a[@class='_5pcq']/abbr").get_attribute('title')
            post_info.set_date_post(get_datetime(str(datetime_str)))
        except NoSuchElementException:
            pass


        # assign number of reactions, comments and shares of posts

        try:
            post_info.set_post_comment_num(int(findall(r"\d{1,4}", signin_driver.find_element_by_xpath("//a[@class='_3hg- _42ft']").get_attribute("innerHTML"))[0]))
        except NoSuchElementException:
            pass
        try:
            post_info.set_post_reaction_num(int(findall(r"\d{1,4}", signin_driver.find_element_by_xpath("//span[@class='_81hb']").get_attribute("innerHTML"))[0]))
        except NoSuchElementException:
            pass
        # try:
        #     post_info.set_post_share_num(int(signin_driver.find_element_by_xpath("//a[@class='_3rwx _42ft").get_attribute("innerHTML")))
        # except NoSuchElementException:
        #     pass

        # assign post content for post
        # there are in fact 3 cases of post content:
        #   - plain text enclosed in                    <p></p>
        #   - text decorated by a frame of Facebook: in <span class="_4a6n _a5_">
        #   - from a shared post

        # the first case of post content
        post_content = signin_driver.find_elements_by_tag_name('p')
        tmp = ''
        for element in post_content:
            tmp += element.text

        # the second case of post content
        if tmp == '':
            # tmp = signin_driver.find_element_by_class_name("_4a6n _a5_").text
            # tmp = signin_driver.find_element_by_class_name("_4a6n").text
            try:
                tmp = signin_driver.find_element_by_xpath("//span[@class='_4a6n _a5_']").get_attribute('innerHTML')
            except NoSuchElementException:
                pass

        # the third case of post content
        if tmp == '' and is_share is True:
            post_info.set_is_share(True)
            # if the post is sharing antoher post, take shared post's post content as the sharing one's content
            link_share = signin_driver.find_element_by_xpath("//span[@class='fcg']/a").get_attribute('href')
            # get that shared post's link and crawl its content
            signin_driver.get(link_share)
            post_content = signin_driver.find_elements_by_tag_name('p')
            tmp = ''
            for element in post_content:
                tmp += element.text

            # back to the sharing post
            signin_driver.get(link)

        
        # if reaches this far and tmp == '', we can ignore this post
        if tmp == '':
            continue

        print("Content: ", tmp)

        print("nLike  = ", post_info.get_post_reaction_num())
        print("nComm  = ", post_info.get_post_comment_num())
        print("nShare = ", post_info.get_post_share_num())

        post_info.set_post_content(tmp)
        
        # Show all comments and replies
        while True:
            try:
                a_tag = signin_driver.find_element_by_xpath("//a[@class='_4sxc _42ft']")
                a_tag.click()
                sleep(0.75)
            except NoSuchElementException:
                break
        
        # assign comment for post
        #comments = signin_driver.find_elements_by_class_name('_72vr')
        comments_replies = signin_driver.find_elements_by_xpath("//div[@aria-label='Comment' or @aria-label='Comment reply']")        
      
        if len(comments_replies) > 0:
            # if post has comment(s)           
            

            # For comment or reply, we do:
            #   if the current is comment:
            #       append to post_info.post_comments if the current comment is not the first comment of the post
            #   then get owner id, tagged user and content of the current
            
            comm_count = 0
            flag_comment_reply = True                       # True: the current is comment, False: otherwise
            comm_replies = []

            
            for comment_reply in comments_replies:
                
                comm_count += 1

                # this is comment
                if comment_reply.get_attribute('aria-label') == "Comment":
                    # print("This is comment")
                    flag_comment_reply = True
                    # if this is not first comment
                    if comm_count > 1:
                        post_info.add_comment(comm_rep_user, comm_rep_content, comm_rep_tag, comm_replies)
                        comm_replies = []

                # this is reply of comment
                else:
                    # print("This is reply")
                    flag_comment_reply = False                

                
                # extract data of reply or comment

                ## get comment's or reply's owner ID

                tmp = comment_reply.find_element_by_class_name('_6qw4').get_attribute('data-hovercard')


                comm_rep_user = findall(re_comm_user_id, tmp)[0]

                # print("Comm user id: ", comm_rep_user)
                
                
                ## get content and (or) tagged user of comment or reply
                comm_rep_content = ""
                comm_rep_tag     = []
                try:
                    comment_class = comment_reply.find_element_by_class_name('_3l3x')

                    # get text in comment
                    try:
                        comm_rep_content = comment_class.find_element_by_tag_name('span').text
                        # print("Text: ", comm_rep_content)
                    except NoSuchElementException:
                        pass

                    # get tag in comment
                    try:

                        tag = comment_class.find_element_by_tag_name('a').get_attribute('data-hovercard')

                        comm_rep_tag.append(findall(re_comm_user_id, tag)[0])

                        # print("Tag id: ", comm_rep_tag)
                    except NoSuchElementException:
                        pass
                    except TypeError:
                        pass
                
                except NoSuchElementException:
                    pass

                
                # if the current is reply, add reply to list comm_replies
                if flag_comment_reply is False:
                    comm_replies.append({
                        'reply_user'   : comm_rep_user,
                        'reply_comment': comm_rep_content,
                        'reply_tag'    : comm_rep_tag
                    })

        # append to posts_info        
        posts_info.append(post_info)
    
            
    store_data(posts_info)

    signin_driver.quit()


re_datetime = r"(\d{1,2})\/(\d{1,2})\/(\d{1,2}),\s(\d{1,2}):(\d{1,2})\s(AM|PM)"

def get_datetime(datetime_str):

    return datetime.strptime(datetime_str, '%H:%M, %d/%m/%Y')

    # result = findall(re_datetime, datetime_str)
    # if result[0][5] == "AM":
    #     return datetime(int(result[0][2]) + 2000, int(result[0][0]), int(result[0][1]), int(result[0][3]), int(result[0][4])).isoformat()
    # else:
    #     hour = int(result[0][3])
    #     if hour != 12:
    #         hour += 12
    #     return datetime(int(result[0][2]) + 2000, int(result[0][0]), int(result[0][1]), hour, int(result[0][4])).isoformat()
import pandas as pd
import settings
from modules.data_backup.api_NLP_communicate import get_from_api

# def store_data(posts_info):
#     df_dict = {
#         'Link': [],
#         'Contents': [],
#         'User': [],
#         'Type': [],
#         'Intent': [],
#         'PIC': [],
#     }
    
#     for post_info in posts_info:        
#         for comment in post_info.get_post_comments():
#             df_dict['Link'].append(settings.GROUP + "permalink/" + post_info.get_post_id())
#             df_dict['Contents'].append(comment['comment_content'])
#             df_dict['User'].append(settings.URL + comment['comment_owner_id'])
#             df_dict['Type'].append("comment")
#             df_dict['Intent'].append("")
#             df_dict['PIC'].append("")

#     df = pd.DataFrame(df_dict)
#     writer = pd.ExcelWriter('result1.xlsx', engine='xlsxwriter')
#     df.to_excel(writer, sheet_name='Sheet1')

#     # Close the Pandas Excel writer and output the Excel file.
#     writer.save()

def store_data(posts_info):

    df_dict = {
            "Link_post": [],
            "Post_owner_id": [],
            "Content_post": [],
            "Time_post": [],
            "Num_react": [],
            "Num_comment": [],
            "Num_share": [],
            "addr_street"       : [],
            "addr_ward"         : [],
            "addr_district"     : [],
            "surrounding_name"  : [],
            "transaction_type"  : [],
            "realestate_type"   : [],
            "position"          : [],
            "potential"         : [],
            "area"              : [],
            "price"             : [],
            "phone"             : [],
        }

    for post in posts_info:
        df_dict["Link_post"].append(settings.GROUP + "permalink/" + post.get_post_id())
        df_dict["Post_owner_id"].append(settings.URL + post.get_post_owner_id())
        df_dict["Content_post"].append(post.get_post_content())
        df_dict["Time_post"].append(post.get_date_post())
        data_attrs = get_from_api(post.get_post_content())
        df_dict["Num_react"].append(post.get_post_reaction_num())
        df_dict["Num_comment"].append(post.get_post_comment_num())
        df_dict["Num_share"].append(post.get_post_share_num())
        df_dict["addr_street"].append(data_attrs["addr_street"])
        df_dict["addr_ward"].append(data_attrs["addr_ward"])
        df_dict["addr_district"].append(data_attrs["addr_district"])
        df_dict["surrounding_name"].append(data_attrs["surrounding_name"])
        df_dict["transaction_type"].append(data_attrs["transaction_type"])
        df_dict["realestate_type"].append(data_attrs["realestate_type"])
        df_dict["position"].append(data_attrs["position"])
        df_dict["potential"].append(data_attrs["potential"])
        df_dict["area"].append(data_attrs["area"])
        df_dict["price"].append(data_attrs["price"])
        df_dict["phone"].append(data_attrs["phone"])

    df = pd.DataFrame(df_dict)
    writer = pd.ExcelWriter('result4.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

        # print("*********************************************")
        # print("group_id     : ", post.get_group_id())
        # print("post_id      : ", post.get_post_id())
        # print("post_owner_id: ", post.get_post_owner_id())
        # print("post_content : ", post.get_post_content())
        # print("date_crawl   : ", post.get_date_crawl())
        # print("date_post    : ", post.get_date_post())
        # print("no. comments : ", post.get_post_comment_num())
        # print("no. reactions: ", post.get_post_reaction_num())
        # print("no. shares   : ", post.get_post_share_num())
        # print("score        : ", post.get_score())
        # print("post_comments: ")
        # for comment in post.get_post_comments():
        #     print("    ------------")
        #     print("    comment_owner_id: ", comment['comment_owner_id'])
        #     print("    comment_content : ", comment['comment_content'])
        #     print("    comment_tags    : ", comment['comment_tags'])
        #     print("    comment_replies : ")
        #     for reply in comment['comment_replies']:
        #         print("      reply_user   :", reply['reply_user'])
        #         print("      reply_comment:", reply['reply_comment'])
        #         print("      reply_tag    :", reply['reply_tag'])
            

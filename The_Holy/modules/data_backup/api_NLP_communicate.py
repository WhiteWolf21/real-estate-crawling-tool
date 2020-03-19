import requests

url = "http://35.240.240.251/api/v1/real-estate-extraction"

data = 'Chính chủ 02 lô đất Củ Chi , liền kề nhau.  Dt: 1.000m2 giá 770 triệu/ 1.000m2 , ' \
       'sổ còn thơm mùi giấy chưa qua kinh doanh , ' \
       'không dính quy hoạch gi cả . Liên Hệ : 0948881115 để đặt cọc nhanh lẹ.'

def get_from_api(post_content):
    request = requests.Session()
    data_list = [post_content]
    headers = {}

    response = request.post(url=url, headers=headers, json=data_list)

    data_attrs = {
        "addr_street"       : "",
        "addr_ward"         : "",
        "addr_district"     : "",
        "surrounding_name"  : "",
        "transaction_type"  : "",
        "realestate_type"   : "",
        "position"          : "",
        "potential"         : "",
        "area"              : "",
        "price"             : "",
        "phone"             : "",
    }
    json_response = response.json()

    import re

    regex = r"\d{3}.?\d{4}.?\d{3}"

    test_str = "Liên hệ Zalo : 088.6666.736"

    matches = re.finditer(regex, post_content, re.MULTILINE)
    num_phone = ''
    for matchNum, match in enumerate(matches, start=1):
        num_phone = match.group()
        # print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))

    for content in json_response[0]["tags"]:
        if content["type"] == "addr_district":
            data_attrs["addr_district"] = content["content"]
        if content["type"] == "addr_street":
            data_attrs["addr_street"] = content["content"]
        if content["type"] == "addr_ward":
            data_attrs["addr_ward"] = content["content"]
        if content["type"] == "surrounding_name":   
            data_attrs["surrounding_name"] = content["content"]
        if content["type"] == "transaction_type":
            data_attrs["transaction_type"] = content["content"]
        if content["type"] == "realestate_type":
            data_attrs["realestate_type"] = content["content"]
        if content["type"] == "position":
            data_attrs["position"] = content["content"]
        if content["type"] == "potential":
            data_attrs["potential"] = content["content"]
        if content["type"] == "area":
            data_attrs["area"] = content["content"]
        if content["type"] == "price":
            data_attrs["price"] = content["content"]

        data_attrs['phone'] = num_phone
    return data_attrs

    # ------------- FOR DEBUGGING PURPOSE -----------------
    # print("\n\n")
    # print("*********************************")
    # print('RESPONSE_DATA:\n %s' % json.dumps(response.json(), ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ': ')))


# get_from_api(data)

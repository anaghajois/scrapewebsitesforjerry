import re
def sanitize_item(item):
    item_text = item.get_attribute("textContent")
    item_text = re.sub('\s+', ' ', item_text)
    #print item_text
    return item_text

def sanitize_item_list(lst):
    sanitized_lst = []
    for item in lst:
        item_text = sanitize_item(item)
        sanitized_lst.append(item_text)
    #print sanitized_lst
    return sanitized_lst

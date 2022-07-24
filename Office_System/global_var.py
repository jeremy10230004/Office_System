def init():
    global global_dict
    global_dict = {}


def set_value(key, value):
    global_dict[key] = value


def get_value(key, value=None):
    try:
        return global_dict[key]
    except KeyError:
        return value


def radio_code_clear(a):
    a["software"] = ""
    a["first"] = "否"
    a["custom"] = "無訂製單"
    a["package"] = ""
    a["currency"] = ""
    a["help_pay"] = "否"
    a["direct"] = ""
    a["sample"] = ""
    a["software_ff"] = ""


def dict_clear(d):
    for i in d:
        d[i] = ""


search_customer_title_list = {"by姓名": ["姓名", "國家"], "by國家": ["姓名", "國家"], "by麥頭": ["姓名", "麥頭"],
                              "已寄樣品": ["姓名", "有無寄樣品"], "未成交": ["姓名", "是否成交"]}
search_customer_key = {"by姓名": "name", "by國家": "country", "by麥頭": "market", "已寄樣品": "sample", "未成交": "first"}
search_ff_title_list = {"by姓名": ["姓名", "國家"], "by國家": ["姓名", "國家"], "by客戶": ["貨代姓名", "客戶姓名"]}
search_ff_key = {"by姓名": "name", "by國家": "country", "by客戶": "customer"}
radio_code = {"software": "", "first": "否", "custom": "無訂製單", "package": "", "currency": "", "help_pay": "否",
              "direct": "", "sample": "", "software_ff": ""}

table_data_customer = {'客戶名稱': '', '國家': '', '通訊軟體': '', '軟體ID': '', '是否已成交': '',
                       '有無訂製單': '', '幣別': '', '價格等級': '', '包裝方式': '', '付款方式': '',
                       '目前麥頭': '', '客戶電話': '', '客戶地址': '',
                       '貨代姓名': '', '貨代電話': '', '貨代地址': '', '是否代付': '', '貨代通訊軟體': '', '貨代軟體ID': ''}
table_data_ff = {'貨代姓名': '', '貨代電話': '', '貨代地址': '', '是否代付': '', '貨代通訊軟體': '', '貨代軟體ID': ''}

label_key = ["name", "country", "software", "sf_id",
             "first", "custom", "currency", "level", "package", "pay_way",
             "market", "phone", "address"]

label_key_ff = ["name", "phone", "address", "help_pay", 'software', 'sf_id']
# -------------order----------------
level_list = (2, 2.5, 3, 3.5, 4, 4.5)
country_spread = {"RMB": 0, "USD": 0.5}
# -------------to_do-----------------
todo_key = {"by關係人": "person", "by內容": "content", "by備註": "remark"}
"""
# 舊石器-----------------------------
software_list = {"詢盤": "AL", "TM": "TM", "WhatsApp": "WA", "WeChat": "WC", "LINE": "LN", "E-mail": "EM"}
software_list_show = {"": "", "AL": "詢盤", "TM": "TM", "WA": "WhatsApp", "WC": "WeChat", "LN": "LINE", "EM": "E-mail"}
first_list = {"是": "是", "否": "否"}
custom_list = {"有訂製單": "有", "無訂製單": "無"}
currency_list = {"RMB": "RMB", "USD": "USD"}
package_list = {"編織袋": "w1", "編織袋+雙頭套": "w2", "紙箱": "b1", "紙箱+編織袋": "bw"}
package_list_show = {"": "", "w1": "編織袋", "w2": "編織袋+雙頭套", "b1": "紙箱", "bw": "紙箱+編織袋"}


price_list = ["2", "2.5", "3", "3.5", "4", "4.5"]
order_e = ["左方數值出現錯誤!", "圖片的地方出現錯誤!", "價格表填寫出現錯誤!"]
"""

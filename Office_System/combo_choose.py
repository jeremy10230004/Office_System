import firestore_command as fc


def ic_country_get():
    ans = fc.find_all_db("customer", "country")

    return ans


# customer_main----------------
cm_search_customer = ["by姓名", "by國家", "by麥頭", "未成交", "已寄樣品"]
cm_search_ff = ["by姓名", "by國家", "by客戶"]

# insert_customer--------------
ic_country = ic_country_get()
ic_level = ["", "2", "2.5", "3", "3.5", "4", "4.5"]
ic_pay_way = {"", "國際站", "1688", "支付寶", "淘寶", "中國T/T", "台灣T/T", "代付"}

# function---------------------
todo_level = ["一般", "優先處理", "追追追", "已完成"]
todo_serach = ["by關係人", "by內容", "by備註"]

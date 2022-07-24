from firebase_admin import firestore
import config

config.firebase_init()


def set_db(path, id, doc, replace=False):
    db = firestore.client()
    id = tran_word(id, "/", "|")
    doc_way = db.collection(path).document(id)
    doc_way.set(doc, merge=replace)


def delete_db(path, id):
    db = firestore.client()
    id = tran_word(id, "/", "|")
    db.collection(path).document(id).delete()


def get_db(path, id):
    db = firestore.client()

    id = tran_word(id, "|", "/")
    doc_way = db.collection(path).document(id)

    try:
        ans = doc_way.get()
    except:
        return {}

    return ans.to_dict()


def find_all_db(path, position, filter_same=True):  # 找出一個屬性的所有可能(例如窮舉所有國家
    db = firestore.client()

    doc_way = db.collection(path)
    ans_list = doc_way.where(position, '!=', "").get()
    ans = [""]
    if filter_same:
        for a in ans_list:
            temp = a.to_dict()[position]
            if temp not in ans:
                ans.append(temp)
        return ans
    else:

        return [a.to_dict() for a in ans_list]


def select_db(path, title, position):
    db = firestore.client()

    doc_way = db.collection(path)
    ans_list = doc_way.where(title, '==', position).get()
    if ans_list:
        ans = ans_list[0].to_dict()
    else:
        ans = {}

    return ans


def select_all_db(path, title, position):
    # 在想到新的模糊搜尋方法前將就用一下
    db = firestore.client()

    doc_way = db.collection(path)
    ans_list = doc_way.where(title, '!=', "").get()
    ans = []
    for a in ans_list:
        if position.upper() in a.to_dict()[title].upper():
            ans.append(a.to_dict())
    return ans


def delete_list_contain(path, person, list_name, item):
    db = firestore.client()

    person = tran_word(person, "/", "|")
    doc_way = db.collection(path).document(person)
    temp_list = doc_way.get().to_dict()[list_name]
    if item in temp_list:
        if len(temp_list) <= 1:
            temp_list = [""]
        else:
            temp_list = temp_list.remove(item)

        doc_way.set({list_name: temp_list}, merge=True)

    # print dictionary keys

    # ans_list = x.collection('ff').where('name', '==', "sample").get()


def tran_word(text, removed, used):
    while removed in text:
        i = text.index(removed)
        if i == len(text) - 1:
            text = f"{text[:-1]}{used}"
        else:
            text = f"{text[:i]}{used}{text[i + 1:]}"
    return text

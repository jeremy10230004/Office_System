from firebase_admin import firestore
import config

config.firebase_init()


def all_add_attribute(path, person, attribute, attribute_init):
    db = firestore.client()

    doc_way = db.collection(path).document(person)
    doc_way.set({attribute: attribute_init}, merge=True)


def show_all_people(path, attribute):
    db = firestore.client()

    doc_way = db.collection(path)
    ans_list = doc_way.where(attribute, '!=', "").get()
    ans = []
    for a in ans_list:
        ans.append(a.to_dict()['name'])

    return ans


if __name__ == '__main__':
    """
    customer_list = show_all_people('ff', 'name')
    for a in customer_list:
        all_add_attribute('ff', a, 'software', '')
    """
    pass

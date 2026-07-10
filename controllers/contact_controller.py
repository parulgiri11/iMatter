from database.db import get_all_contacts, insert_contact, update_contact, delete_contact

MAX_CONTACTS = 5

def add_contact(user_id, name, phone):
    if not name or not phone:
        return False, "Name and phone are required."
    if not name.strip():
        return False, "Name cannot be empty."
    if not phone.strip().lstrip("+").isdigit():
        return False, "Phone must contain digits only."
    if len(phone.strip()) < 7 or len(phone.strip()) > 15:
        return False, "Phone must be between 7 and 15 digits."
    if len(get_all_contacts(user_id)) >= MAX_CONTACTS:
        return False, f"Maximum {MAX_CONTACTS} contacts allowed."
    insert_contact(user_id, name.strip(), phone.strip())
    return True, "Contact saved."

def remove_contact(contact_id):
    delete_contact(contact_id)

def modify_contact(contact_id, name, phone):
    if not name.strip():
        return False, "Name cannot be empty."
    if not phone.strip().lstrip("+").isdigit():
        return False, "Phone must contain digits only."
    if len(phone.strip()) < 7 or len(phone.strip()) > 15:
        return False, "Phone must be between 7 and 15 digits."
    update_contact(contact_id, name.strip(), phone.strip())
    return True, "Contact updated."

def fetch_contacts(user_id):
    return get_all_contacts(user_id)
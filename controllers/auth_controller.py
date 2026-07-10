import hashlib
from database.db import get_user_by_mobile, create_user, update_user_password


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login(mobile, password):
    user = get_user_by_mobile(mobile)
    if not user:
        return False, "Mobile number not registered.", None
    if user[2] != hash_password(password):
        return False, "Incorrect password.", None
    return True, "Login successful.", user[0]  


def register(mobile, password, confirm_password, security_question, security_answer):
    if not mobile or not password or not confirm_password:
        return False, "All fields are required."

    if password != confirm_password:
        return False, "Passwords do not match."

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    if not security_question or not security_answer.strip():
        return False, "Security question and answer are required."

    existing = get_user_by_mobile(mobile)
    if existing:
        return False, "Mobile number already registered."

    create_user(
        mobile,
        hash_password(password),
        security_question,
        security_answer.strip().lower(), 
    )
    return True, "Account created successfully!"


def verify_security_answer(mobile, answer=None, fetch_only=False):
    user = get_user_by_mobile(mobile)

    if not user:
        return False, "No account found with this mobile number."

    if fetch_only:
        # Step 1: just return the security question
        question = user[3]  # user[3] = security_question
        if not question:
            return False, "This account has no security question set."
        return True, question

    # Step 2: validate the answer
    if answer.strip().lower() == user[4]: 
        return True, "Verified."
    return False, "Incorrect answer. Please try again."


def reset_password(mobile, new_password, confirm):
    if not new_password or not confirm:
        return False, "All fields are required."

    if new_password != confirm:
        return False, "Passwords do not match."

    if len(new_password) < 6:
        return False, "Password must be at least 6 characters."

    user = get_user_by_mobile(mobile)
    if not user:
        return False, "Account not found."

    update_user_password(mobile, hash_password(new_password))
    return True, "Password reset successfully."

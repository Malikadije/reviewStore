from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

# Inisialisasi MySQL
db = MySQL()

def init_db(app):
    db.init_app(app)

# Model untuk User
class User:
    def __init__(self, id, username, email, password_hash, role):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role

    @staticmethod
    def create_user(username, password, email, role='user'):
        cur = db.connection.cursor()
        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, %s)",
                    (username, password_hash, email, role))
        db.connection.commit()
        cur.close()

    @classmethod
    def get_user_by_email(cls, email):
        cur = db.connection.cursor()
        cur.execute("SELECT id, username, email, password, role FROM users WHERE email = %s", [email])
        user_data = cur.fetchone()
        cur.close()
        if user_data:
            # Mengonversi tuple menjadi objek User
            user = cls(id=user_data[0], username=user_data[1], email=user_data[2], password_hash=user_data[3], role=user_data[4])
            return user
        return None

    @classmethod
    def get_user_by_id(cls, user_id):
        cur = db.connection.cursor()
        cur.execute("SELECT id, username, email, password, role FROM users WHERE id = %s", [user_id])
        user_data = cur.fetchone()
        cur.close()
        if user_data:
            # Mengonversi tuple menjadi objek User
            user = cls(id=user_data[0], username=user_data[1], email=user_data[2], password_hash=user_data[3], role=user_data[4])
            return user
        return None

    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email}, role={self.role})>"

    def __str__(self):
        return f"User {self.username} with email {self.email}"

    @staticmethod
    def get_all_users():
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        return users
    @staticmethod
    def delete_user(user_id):
        cur = db.connection.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", [user_id])
        db.connection.commit()
    @staticmethod
    def update_user(user_id, username, email, role, password):
        cur = db.connection.cursor()
        cur.execute("UPDATE users SET username = %s, email = %s, password = %s, role = %s WHERE id = %s", 
                    (username, email, password, role, user_id))
        db.connection.commit()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

# Model untuk Review
class Review:
    @staticmethod
    def create_review(email, content, rating):
        cur = db.connection.cursor()
        cur.execute("INSERT INTO reviews (email, deskripsi, rating) VALUES (%s, %s, %s)", 
                    (email, content, rating))
        db.connection.commit()

    @staticmethod
    def get_all_reviews():
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM reviews")
        reviews = cur.fetchall()
        return reviews

    @staticmethod
    def get_review_by_id(review_id):
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM reviews WHERE id = %s", [review_id])
        review = cur.fetchone()
        return review

    @staticmethod
    def update_review(review_id, content, rating):
        cur = db.connection.cursor()
        cur.execute("UPDATE reviews SET deskripsi = %s, rating = %s WHERE id = %s", 
                    (content, rating, review_id))
        db.connection.commit()

    @staticmethod
    def delete_review(review_id):
        cur = db.connection.cursor()
        cur.execute("DELETE FROM reviews WHERE id = %s", [review_id])
        db.connection.commit()

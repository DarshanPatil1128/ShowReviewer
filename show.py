from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash


class Show:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.network = data['network']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        #self.user_id = data['user_id']
        self.maker = None

    @classmethod
    def create(cls, data):
        query = "INSERT INTO tvs (name, network, date, description, user_id) VALUES (%(name)s, %(network)s, %(date)s, %(description)s, %(user_id)s);"
        results = connectToMySQL('shows').query_db(query, data)
        print(results)
        return results

    @classmethod
    def all_shows(cls):
        query = "SELECT * FROM tvs JOIN users ON users.id = tvs.user_id "
        results = connectToMySQL('shows').query_db(query)
        print(results)
        all_shows = []
        for one in results: 
            one_show = cls(one)
            user_data = {
                "id" : one['users.id'],
                "first_name" : one['first_name'],
                "last_name" : one['last_name'],
                "email" : one['email'],
                "name" : one['name'],
                "password" : one['password'],
                "created_at" : one['users.created_at'],
                "updated_at" : one['users.updated_at']
            }
            user_obj = user.User(user_data)
            one_show.creater = user_obj
            all_shows.append(one_show)
        return all_shows


    @classmethod
    def get_by_id(cls, show_id):
        query = "SELECT * FROM tvs WHERE id = %(show_id)s;"
        results = connectToMySQL("shows").query_db(query,show_id)
        print(results)
        return results

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM tvs WHERE id = %(id)s;"
        results = connectToMySQL("shows").query_db(query,data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE tvs set name = %(name)s, description = %(description)s, network = %(network)s, date = %(date)s WHERE id = %(id)s;"
        result = connectToMySQL('shows').query_db(query,data)
        print(result)
        return result

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM tvs WHERE id = %(id)s;"
        results = connectToMySQL('shows').query_db(query, data)
        print(results)
        return results

    @classmethod
    def get_by_id(cls, show_id):
        print(f"get show by id {show_id}")
        data = {
            "id" : show_id
        }
        query = "SELECT tvs.id, tvs.name, tvs.network, tvs.date, tvs.description, tvs.created_at, tvs.updated_at, users.id as user_id, first_name, last_name, email, password, users.created_at as uc, users.updated_at as uu FROM tvs JOIN users on users.id = tvs.user_id WHERE tvs.id = %(id)s;"
        results = connectToMySQL('shows').query_db(query, data)
        print(results)
        results = results[0]
        show = cls(results)

        show.user = user.User(
                {
                    "id" : results['user_id'],
                    "first_name" : results['first_name'],
                    "last_name" : results['last_name'],
                    "email" : results['email'],
                    "password" : results['password'],
                    "created_at" : results['uc'],
                    "updated_at" : results['uu'],
                }
        )
        return show

    @staticmethod
    def validate_new(user):
        is_valid = True 
        if len(user['name']) < 3:
            flash("Title must be minimum 3 character")
            is_valid = False
        if len(user['description']) < 3:
            flash("Description Must be minimum 3 character")
            is_valid = False
        if len(user['network']) < 3:
            flash("Network Must be minimum 3 character")
            is_valid = False
        return is_valid 
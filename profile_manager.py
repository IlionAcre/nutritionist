from db_manager import personal_data_collection, notes_collection

def get_values(_id):
    return {
        "_id": _id, 
        "general": {
            "name": "",
            "age": 30,
            "weight": 60,
            "height": 165,
            "activity_level": "Moderately Active",
            "gender": "Male"
        },
        "goals": ["Muscle gain"],
        "nutrition": {
            "calories": 2000,
            "protein": 140,
            "fat": 20,
            "carbs": 100,
            },
    }
    
def create_profile(_id):
    profile_values = get_values(_id)
    new_profile = personal_data_collection.insert_one(profile_values)
    return new_profile.inserted_id, new_profile

def get_profile(_id):
    return personal_data_collection.find_one({"_id": {"$eq":_id}})

def get_notes(_id):
    return list(notes_collection.find({"user_id":{"$eq":_id}}))
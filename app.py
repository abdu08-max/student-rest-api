from flask import Flask, request, jsonify

app = Flask(__name__)

students = {
    1: {
        "name": "Arun",
        "roll_number": "23AD001",
        "department": "AI & DS",
        "year": 3
    },
    2: {
        "name": "Rahul",
        "roll_number": "23AD002",
        "department": "CSE",
        "year": 3
    }
}
def validate_student(data):
    required_fields = ["name", "roll_number", "department", "year"]
    for field in required_fields:
        if field not in data:
            return f"Missing field: {field}"

    for field in required_fields:
        if data[field] == "" or data[field] is None:
            return f"{field} cannot be empty"
    if not isinstance(data["year"], int):
        return "Year must be an integer"
    if data["year"] < 1 or data["year"] > 4:
        return "Year must be between 1 and 4"
    return None
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Student REST API is running"
    }
@app.route("/students", methods=["POST"])
def create_student():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body cannot be empty"
        }), 400

    error = validate_student(data)

    if error:
        return jsonify({
            "error": error
        }), 400

    for student in students.values():
        if student["roll_number"] == data["roll_number"]:
            return jsonify({
                "error": "Roll number already exists"
            }), 40
    new_id = max(students.keys(), default=0) + 1

    students[new_id] = {
        "name": data["name"],
        "roll_number": data["roll_number"],
        "department": data["department"],
        "year": data["year"]
    }

    return jsonify({
        "message": "Student created successfully",
        "id": new_id,
        "student": students[new_id]
    }), 201
@app.route("/students", methods=["GET"])
def get_students():

    result = []

    for student_id, student in students.items():
        student_data = {
            "id": student_id,
            **student
        }

        result.append(student_data)

    return jsonify(result), 200
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):

    if student_id not in students:
        return jsonify({
            "error": "Student not found"
        }), 404

    return jsonify({
        "id": student_id,
        **students[student_id]
    }), 200
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):

    if student_id not in students:
        return jsonify({
            "error": "Student not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body cannot be empty"
        }), 400

    error = validate_student(data)

    if error:
        return jsonify({
            "error": error
        }), 400
    for sid, student in students.items():
        if sid != student_id and student["roll_number"] == data["roll_number"]:
            return jsonify({
                "error": "Roll number already exists"
            }), 409

    students[student_id] = {
        "name": data["name"],
        "roll_number": data["roll_number"],
        "department": data["department"],
        "year": data["year"]
    }

    return jsonify({
        "message": "Student updated successfully",
        "id": student_id,
        "student": students[student_id]
    }), 200

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):

    if student_id not in students:
        return jsonify({
            "error": "Student not found"
        }), 404

    deleted_student = students.pop(student_id)

    return jsonify({
        "message": "Student deleted successfully",
        "student": deleted_student
    }), 200
if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, jsonify, request

application = Flask(__name__)

tasks = [
    {"id": 1, "title": "Learn AWS Elastic Beanstalk", "completed": False},
    {"id": 2, "title": "Deploy a Flask application", "completed": False},
]


@application.route("/", methods=["GET"])
def home():
    return jsonify(
        {
            "message": "Welcome to the Task Management API",
            "project": "AWS Elastic Beanstalk",
            "status": "success",
        }
    )


@application.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)


@application.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}

    if not data.get("title"):
        return jsonify({"error": "Task title is required"}), 400

    task = {
        "id": max((t["id"] for t in tasks), default=0) + 1,
        "title": data["title"],
        "completed": False,
    }

    tasks.append(task)
    return jsonify(task), 201


@application.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json(silent=True) or {}

    if "title" in data:
        task["title"] = data["title"]

    if "completed" in data:
        task["completed"] = bool(data["completed"])

    return jsonify(task)


@application.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    tasks.remove(task)
    return jsonify({"message": "Task deleted successfully"})


if __name__ == "__main__":
    application.run(host="127.0.0.1", port=5000, debug=True)

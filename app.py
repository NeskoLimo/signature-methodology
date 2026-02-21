from flask import Flask, request, jsonify, render_template
import datetime

app = Flask(__name__)

# Mock database for maintaining the last working model
projects = []

@app.route('/')
def index():
    return "Project Management System API"

@app.route('/projects/upload', methods=['POST'])
def mass_upload():
    """
    Handles the mass upload template. 
    Expects a list of project objects.
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    for item in data:
        project = {
            "id": len(projects) + 1,
            "name": item.get("name"),
            "start_date": item.get("start_date"),
            "projected_end_date": item.get("projected_end_date"),
            "actual_end_date": item.get("actual_end_date", None),
            "attachment_path": item.get("attachment_path", None), # Sign-off scope
            "status": item.get("status")
        }
        projects.append(project)
        
    return jsonify({"message": f"Successfully uploaded {len(data)} projects"}), 201

@app.route('/projects/filter', methods=['GET'])
def get_projects():
    """
    Filters projects based on criteria to enrich analytics.
    """
    status_filter = request.args.get('status')
    
    if status_filter:
        filtered_list = [p for p in projects if p['status'] == status_filter]
        return jsonify(filtered_list)
    
    return jsonify(projects)

if __name__ == '__main__':
    # Set debug=True for development, False for production
    app.run(debug=True)

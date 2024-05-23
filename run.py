from flask import Flask, request, jsonify, render_template_string
import json
import os

app = Flask(__name__)

# Load the JSON data
with open(os.path.join('static', 'dynmodb_problems.json'), 'r') as f:
    dynamodb_data = json.load(f)

with open(os.path.join('static', 'postgres_ranking.json'), 'r') as f:
    postgres_rankings = json.load(f)

@app.route('/ranking/<contest_id>', methods=['GET'])
def get_ranking(contest_id):
    # Get the contest problems from DynamoDB data
    contest = next((c for c in dynamodb_data['contests'] if c['id'] == contest_id), None)
    if not contest:
        return jsonify({"error": "Contest not found"}), 404

    # Get the user rankings from the PostgreSQL-like data
    rankings = [r for r in postgres_rankings if r['contest_id'] == contest_id]
    if not rankings:
        return jsonify({"error": "No rankings found for this contest"}), 404

    # Aggregate scores per user
    user_scores = {}
    for ranking in rankings:
        user = ranking['user']
        if user not in user_scores:
            user_scores[user] = {
                'total_speed': 0,
                'total_correctness': 0,
                'total_edge_cases': 0,
                'total_penalty': 0,
                'total_submissions': 0,
                'final_score': 0
            }
        user_scores[user]['total_speed'] += ranking['speed']
        user_scores[user]['total_correctness'] += ranking['correctness']
        user_scores[user]['total_edge_cases'] += ranking['edge_cases']
        user_scores[user]['total_penalty'] += ranking['penalty'] * ranking['submissions']
        user_scores[user]['total_submissions'] += ranking['submissions']
        user_scores[user]['final_score'] += ranking['speed'] + ranking['correctness'] + ranking['edge_cases'] - (ranking['penalty'] * ranking['submissions'])

    # Sort users by final_score in descending order
    sorted_user_scores = sorted(user_scores.items(), key=lambda x: x[1]['final_score'], reverse=True)

    # Generate HTML table
    html_table = """
    <html>
    <head>
        <title>Contest Rankings</title>
    </head>
    <body>
        <h1>Rankings for Contest {{contest_id}}</h1>
        <table border="1">
            <tr>
                <th>User</th>
                <th>Total Speed</th>
                <th>Total Correctness</th>
                <th>Total Edge Cases</th>
                <th>Total Penalty</th>
                <th>Total Submissions</th>
                <th>Final Score</th>
            </tr>
            {% for user, scores in sorted_user_scores %}
                <tr>
                    <td>{{user}}</td>
                    <td>{{scores.total_speed}}</td>
                    <td>{{scores.total_correctness}}</td>
                    <td>{{scores.total_edge_cases}}</td>
                    <td>{{scores.total_penalty}}</td>
                    <td>{{scores.total_submissions}}</td>
                    <td>{{scores.final_score}}</td>
                </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    return render_template_string(html_table, contest_id=contest_id, sorted_user_scores=sorted_user_scores)

if __name__ == '__main__':
    app.run(debug=True)

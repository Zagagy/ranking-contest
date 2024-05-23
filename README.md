
# Contest Ranking System

This project is a simple Flask application that aggregates and displays contest rankings for coding problems. It calculates the final scores for users based on their performance across multiple problems within a contest and displays the results in an HTML table.

## Project Structure

```
your_project/
│
├── app.py
├── README.md
└── static/
    ├── dynamodb_data.json
    └── postgres_rankings.json
```

## Description

- **app.py**: The main Flask application that loads contest data and user rankings, calculates the final scores, and displays the results in an HTML table.
- **dynamodb_data.json**: Contains contest information and problem descriptions. This simulates the data stored in DynamoDB.
- **postgres_rankings.json**: Contains user performance data for each problem in each contest. This simulates the data stored in PostgreSQL.

## How the Scores Work

Each user's performance is evaluated based on the following criteria:
- **Speed**: The time taken to solve the problem.
- **Correctness**: The accuracy of the solution.
- **Edge Cases**: The ability to handle edge cases correctly.
- **Penalty**: A penalty score that increases with the number of submissions.

The final score for each user is calculated using the formula:

```
final_score = total_speed + total_correctness + total_edge_cases - (total_penalty * total_submissions)
```

## How to Run

1. **Clone the repository and navigate to the project directory**:
    ```bash
    git clone <repository_url>
    cd your_project
    ```

2. **Create a virtual environment and activate it**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:
    ```bash
    pip install Flask
    ```

4. **Ensure the JSON files are in the `static` folder**:
    ```
    your_project/
    ├── app.py
    └── static/
        ├── dynamodb_data.json
        └── postgres_rankings.json
    ```

5. **Run the Flask application**:
    ```bash
    python app.py
    ```

6. **Access the rankings for a contest by navigating to**:
    ```
    http://127.0.0.1:5000/ranking/<contest_id>
    ```
    Replace `<contest_id>` with the ID of the contest you want to view, e.g., `contest1`.

## Example

To view the rankings for "contest1", navigate to:
```
http://127.0.0.1:5000/ranking/contest1
```

The rankings will be displayed in a table, showing the total speed, correctness, edge cases, penalty, number of submissions, and final score for each user.

## License

This project is licensed under the MIT License.

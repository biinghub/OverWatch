from flask import Flask, request, render_template
from mylibrary import actions

app = Flask(__name__)

# PRESETS
PRESET_1 = "database_query, non-sensitive"
PRESET_2 = "database_query, sensitive"
PRESET_3 = "financial_data, PII"


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':

        data = request.form
        if data['query'] == 'query':
            # Example 1: Developer can just specify the certain events
            actions.monitor_event("critical", "user_event", tags=[
                                  "database_query", "sensitive", "PII"])
            # Example 2: Developer can use a common preset
            actions.monitor_event("major", "user_event", tags=[PRESET_1])
            # Example 3: Developer can combine presets
            actions.monitor_event("minor", "machine_event",
                                  tags=[PRESET_2, PRESET_3])

            return render_template('success.html')
        else:
            return render_template('error.html')


if __name__ == '__main__':
    app.run(port=6969, debug=True)

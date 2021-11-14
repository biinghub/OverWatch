"""
Developer/User will call the monitor event function and input the types of actions being performed.
severity:   - how important this action may be to security of the company
            - could be classified as critical, major, minor, etc... This could affect how sensitive our rules/alerts may
                need to be. However we need to identify a set of criteria for our priority matrix.
event:      - Define what behaviour it is. It could be a user event or machine event.
                ie. User makes a database query -> user_event.
                    Service account/m2m account performs a certain action which the user did not specify it to do.
                        (isn't limited to this but in general we are just looking to define different behaviours which could potentially 
                            affect how our rules are formulated) 
action:     - speaks for itself
"""


def monitor_event(severity, event, tags):
    # perform severity logic
    if severity == "critical":
        pass
    elif severity == "major":
        pass
    elif severity == "minor":
        pass
    else:
        pass

    # perform severity logic
    if event == "user_event":
        pass
    elif event == "machine_event":
        pass
    else:
        pass

    # perform action logic
    for tag in tags:
        if tag == "database_query":
            pass
        elif tag == "sensitive":
            pass
        elif tag == "PII":
            pass
        elif tag == "financial_data":
            pass
        else:
            pass


def test_action():
    print("action taken")

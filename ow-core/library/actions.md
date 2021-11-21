# Table of Contents

* [actions](#actions)
  * [OverWatch\_Logger](#actions.OverWatch_Logger)
    * [monitor\_event](#actions.OverWatch_Logger.monitor_event)

<a id="actions"></a>

# actions

<a id="actions.OverWatch_Logger"></a>

## OverWatch\_Logger Objects

```python
class OverWatch_Logger()
```

<a id="actions.OverWatch_Logger.monitor_event"></a>

#### monitor\_event

```python
def monitor_event(priority: Priority, application: str, eventPrefix: str, message: str)
```

Send Activity Log to OverWatch

priority: Priority - priority of event (enum from SDK)\
application: str - application name\
eventPrefix: str - unique prefix to identify specific event type\
message: str - message for log\

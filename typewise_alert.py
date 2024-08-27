# Constants for cooling types and breach types
PASSIVE_COOLING = 'PASSIVE_COOLING'
HI_ACTIVE_COOLING = 'HI_ACTIVE_COOLING'
MED_ACTIVE_COOLING = 'MED_ACTIVE_COOLING'

TOO_LOW = 'TOO_LOW'
TOO_HIGH = 'TOO_HIGH'
NORMAL = 'NORMAL'

# Limits dictionary to avoid duplication
TEMPERATURE_LIMITS = {
    PASSIVE_COOLING: (0, 35),
    HI_ACTIVE_COOLING: (0, 45),
    MED_ACTIVE_COOLING: (0, 40)
}

# Email messages dictionary to avoid duplication
EMAIL_MESSAGES = {
    TOO_LOW: 'Hi, the temperature is too low',
    TOO_HIGH: 'Hi, the temperature is too high'
}

def infer_breach(value, lower_limit, upper_limit):
    if value < lower_limit:
        return TOO_LOW
    if value > upper_limit:
        return TOO_HIGH
    return NORMAL

def classify_temperature_breach(cooling_type, temperature_in_c):
    lower_limit, upper_limit = TEMPERATURE_LIMITS.get(cooling_type, (0, 0))
    return infer_breach(temperature_in_c, lower_limit, upper_limit)

def check_and_alert(alert_target, battery_char, temperature_in_c):
    breach_type = classify_temperature_breach(battery_char['coolingType'], temperature_in_c)
    alert_functions = {
        'TO_CONTROLLER': send_to_controller,
        'TO_EMAIL': send_to_email
    }
    alert_function = alert_functions.get(alert_target)
    if alert_function:
        alert_function(breach_type)

def send_to_controller(breach_type):
    header = 0xfeed
    print(f'{header}, {breach_type}')

def send_to_email(breach_type):
    recipient = "a.b@c.com"
    message = EMAIL_MESSAGES.get(breach_type, 'Temperature is normal')
    print(f'To: {recipient}')
    print(message)

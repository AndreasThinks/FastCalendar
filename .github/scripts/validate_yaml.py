import yaml
from datetime import datetime

def validate_event(event):
    required_fields = ['title', 'date', 'description', 'location']
    for field in required_fields:
        if field not in event:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate date format
    try:
        datetime.strptime(event['date'], '%Y-%m-%d')
    except ValueError:
        raise ValueError(f"Invalid date format for event '{event['title']}'. Use YYYY-MM-DD.")
    
    # Validate location (single word, no spaces)
    if ' ' in event['location'] or not event['location'].isalnum():
        raise ValueError(f"Invalid location for event '{event['title']}'. Location must be a single word with no spaces.")
    

def main():
    with open('events.yaml', 'r') as file:
        try:
            events = yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML: {e}")
            exit(1)
    
    if not isinstance(events, list):
        print("Error: events.yaml should contain a list of events")
        exit(1)
    
    for event in events:
        try:
            validate_event(event)
        except ValueError as e:
            print(f"Validation error: {e}")
            exit(1)
    
    print("YAML validation successful")

if __name__ == "__main__":
    main()
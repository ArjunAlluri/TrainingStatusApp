import json
from collections import Counter
from datetime import datetime, timedelta

# Helper function to load the JSON data from a file
def load_data(filename):
    """Load JSON data from a file."""
    with open(filename, 'r') as file:
        return json.load(file)

# Helper function to get the most recent completion for each training
def get_most_recent_completions(completions):
    """Return a dictionary with the most recent completion for each training."""
    most_recent = {}
    for completion in completions:
        training_name = completion['name']
        completion_date = datetime.strptime(completion['timestamp'], "%m/%d/%Y")
        
        # Only keep the most recent completion for each training
        if training_name not in most_recent or completion_date > most_recent[training_name]['date']:
            most_recent[training_name] = {
                'timestamp': completion['timestamp'],
                'expires': completion.get('expires', None),
                'date': completion_date
            }
    return most_recent

# Task 1: Count completions for each training
def task1(training_data):
    """Count how many people have completed each training (only the most recent completion per person)."""
    training_counts = Counter()
    
    for person in training_data:
        most_recent_completions = get_most_recent_completions(person['completions'])
        for training_name, completion in most_recent_completions.items():
            training_counts[training_name] += 1
    
    # Prepare output as a list of dictionaries for better readability
    output = [{'training': name, 'count': count} for name, count in training_counts.items()]
    
    # Write output to a JSON file
    with open('task1_output.json', 'w') as file:
        json.dump(output, file, indent=4)
    
    print("Task 1 completed! See task1_output.json for the results.")

# Helper function to check if a training was completed in a given fiscal year
def is_in_fiscal_year(completion_date, fiscal_year):
    """Check if a given date falls within a fiscal year."""
    date = datetime.strptime(completion_date, "%m/%d/%Y")
    fiscal_year_start = datetime(fiscal_year - 1, 7, 1)
    fiscal_year_end = datetime(fiscal_year, 6, 30)
    return fiscal_year_start <= date <= fiscal_year_end

# Task 2: Find people who completed specific trainings in a given fiscal year
def task2(training_data):
    """List people who completed specified trainings in the fiscal year 2024 (only the most recent completion per person)."""
    fiscal_year = 2024
    relevant_trainings = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]
    
    # Dictionary to store results, where the keys are training names
    training_results = {training: [] for training in relevant_trainings}
    
    for person in training_data:
        most_recent_completions = get_most_recent_completions(person['completions'])
        for training_name, completion in most_recent_completions.items():
            # Check if the training is one we're interested in and was completed in fiscal year 2024
            if training_name in relevant_trainings and is_in_fiscal_year(completion['timestamp'], fiscal_year):
                training_results[training_name].append(person['name'])
    
    # Write output to a JSON file
    with open('task2_output.json', 'w') as file:
        json.dump(training_results, file, indent=4)
    
    print("Task 2 completed! Check task2_output.json for details.")

# Helper function to check whether a training has expired or will expire soon
def check_expiry(expiration_date, reference_date):
    """Determine if a training has expired or is about to expire soon."""
    if expiration_date is None:
        return None
    expiration = datetime.strptime(expiration_date, "%m/%d/%Y")
    
    if expiration < reference_date:
        return 'expired'
    elif expiration <= reference_date + timedelta(days=30):
        return 'expires soon'
    return None

# Task 3: Find expired or soon-to-expire trainings
def task3(training_data):
    """Find trainings that have expired or are expiring within one month of October 1st, 2023 (only the most recent completion per person)."""
    reference_date = datetime(2023, 10, 1)
    expiring_results = []
    
    for person in training_data:
        person_result = {'name': person['name'], 'expiring_trainings': []}
        
        most_recent_completions = get_most_recent_completions(person['completions'])
        for training_name, completion in most_recent_completions.items():
            if completion['expires']:
                status = check_expiry(completion['expires'], reference_date)
                if status:
                    person_result['expiring_trainings'].append({
                        'training': training_name,
                        'status': status
                    })
        
        # Only include people who have expiring or expired trainings
        if person_result['expiring_trainings']:
            expiring_results.append(person_result)
    
    # Write output to a JSON file
    with open('task3_output.json', 'w') as file:
        json.dump(expiring_results, file, indent=4)
    
    print("Task 3 completed! Results are saved in task3_output.json.")

def main():
    
    data = load_data('trainings.json')
    
    print("Running Task 1: Counting completed trainings...")
    task1(data)

    print("Running Task 2: Listing completions for fiscal year 2024...")
    task2(data)

    print("Running Task 3: Finding expired or expiring soon trainings...")
    task3(data)
    

if __name__ == "__main__":
    main()

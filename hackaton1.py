import json

# Load the data from the JSON file
with open('data/providers.json', 'r') as file:
    data = json.load(file)

def find_best_plan(plans, required_data, required_minutes):
    """
    This function finds the best mobile plan based on the user's required data and minutes.
    It also returns a list of other available plans for additional options.
    """
    best_plan = None
    smallest_diff = float('inf')  # Initialize to infinity to ensure finding the closest plan
    other_plans = []
    
    for plan in plans:
        # Calculate the difference between the user's needs and the available plan
        data_diff = abs(int(plan['Data'].replace('GB', '')) - required_data)
        minutes_diff = abs(int(plan['Minutes'].replace('min', '').replace('Unlimited', str(required_minutes))) - required_minutes)
        total_diff = data_diff + minutes_diff
        
        # Update the best plan if the current plan is closer to the user's requirements
        if total_diff < smallest_diff:
            smallest_diff = total_diff
            if best_plan:
                other_plans.append(best_plan)  # Add the previous best plan to the other options
            best_plan = plan
        else:
            other_plans.append(plan)  # Add other non-best plans to the list of other options
        
    return best_plan, other_plans

def get_recommendations(countries):
    """
    This function takes a list of countries and returns recommendations for mobile plans 
    based on the user's data and call requirements.
    """
    recommendations = []

    for country in countries:
        country = country.strip().capitalize()
        
        if country in data:
            print(f"\nFor {country}:")
            # Get user input for the required data and minutes for each country
            required_data = int(input(f"How many GB of data do you need in {country}? "))
            required_minutes = int(input(f"How many minutes of calls do you need in {country}? "))
            
            # Find the best plan and other options using the function defined above
            best_plan, other_plans = find_best_plan(data[country]["Operators"], required_data, required_minutes)
            
            if best_plan:
                recommendation = {
                    "country": country,
                    "best_plan": best_plan,
                    "other_options": other_plans
                }
                recommendations.append(recommendation)
            else:
                recommendations.append(f"No suitable plan found for {country}.")
        else:
            recommendations.append(f"No information available for {country}.")
    
    return recommendations

# Main program
countries = input("Enter the countries you will visit (separated by commas): ").split(',')
recommendations = get_recommendations(countries)

# Display all the recommendations to the user
print("\nYour travel recommendations:")
for recommendation in recommendations:
    if isinstance(recommendation, dict):
        print(f"\nRecommendation for {recommendation['country']}:")
        best_plan = recommendation['best_plan']
        print(f"Best Plan: {best_plan['Name']} - {best_plan['Plan']} (Data: {best_plan['Data']}, Minutes: {best_plan['Minutes']}, Price: {best_plan['Price']})")
        print("Other Options:")
        for plan in recommendation['other_options']:
            print(f"{plan['Name']} - {plan['Plan']} (Data: {plan['Data']}, Minutes: {plan['Minutes']}, Price: {plan['Price']})")
    else:
        print(recommendation)

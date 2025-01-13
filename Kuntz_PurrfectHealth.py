git config --global user.email "alessandra.kuntz@med.uni-goettingen.de"
git config --global user.name "Alessandra Kuntz"

import matplotlib.pyplot as plt
import os

# Set the output folder path to the current working directory
output_folder = os.path.join(os.getcwd(), "purrfecthealth_output")

# Create the output folder if it does not exist
os.makedirs(output_folder, exist_ok=True)

# Function to evaluate weight status and provide recommendations
def evaluate_cat(name, age, weight, gender, activity, food_quantity, food_type):
    # Define thresholds based on age group, activity level, and gender
    if age < 1:
        # Thresholds for kittens (more lenient)
        thresholds = {"low": 1.0, "medium": 2.0, "high": 3.0}  # Kittens
    else:
        if gender == "M":  # Males generally have a slightly higher threshold
            thresholds = {"low": 4.5, "medium": 5.5, "high": 6.5}  # Adult males
        else:  # Females
            thresholds = {"low": 4.0, "medium": 5.0, "high": 6.0}  # Adult females
    
    # Now, we evaluate the weight relative to the thresholds
    if weight < thresholds[activity] - 0.5:
        status = "underweight"
        diet_recommendation = f"Increase food intake by 10-15%. Consider switching to a higher-calorie diet."
        activity_advice = "Engage in more playtime to build muscle mass." if activity == "low" else ""
    elif weight >= thresholds[activity] - 0.5 and weight <= thresholds[activity] + 0.5:
        status = "normal"
        diet_recommendation = f"Maintain current diet."
        
        # Activity advice based on activity level
        if activity == "low":
            activity_advice = "Increase activity level with more playtime or exercise to improve health."
        elif activity == "high":
            activity_advice = "Maintain current activity level."
        else:
            activity_advice = ""
    else:
        status = "overweight"
        diet_recommendation = f"Reduce food intake by 10-15%. Consider switching to a lighter diet."
        activity_advice = "Increase playtime or engage in more physical activities to promote weight loss." if activity == "low" else ""
    
    return status, diet_recommendation, activity_advice

# Read input data from file and process it
cats = []
input_file_path = os.path.join(output_folder, "cat_data.txt")
with open(input_file_path, "r") as file:
    for line in file:
        # Split the data by commas and strip any unwanted spaces
        name, age, weight, gender, activity, food_quantity, food_type = line.strip().split(",")
        
        # Convert the data to appropriate types
        age = float(age)  # Convert age to float
        weight = float(weight)  # Convert weight to float
        food_quantity = float(food_quantity)  # Convert food_quantity to float
        
        # Append the processed data as a tuple to the cats list
        cats.append((name, age, weight, gender, activity, food_quantity, food_type))

# Process each cat and store results
results = []
for cat in cats:
    name, age, weight, gender, activity, food_quantity, food_type = cat
    status, diet_recommendation, activity_advice = evaluate_cat(name, age, weight, gender, activity, food_quantity, food_type)
    
    # Determine gender symbol
    gender_symbol = "♂" if gender == "M" else "♀"
    
    # Append the result with the activity advice
    results.append((name, age, gender_symbol, status, activity, diet_recommendation, activity_advice, weight))

# Write results to an output file in tabular format with UTF-8 encoding
output_file_path = os.path.join(output_folder, "cat_results.txt")
with open(output_file_path, "w", encoding="utf-8") as file:  # Set encoding to UTF-8
    file.write(f"{'Name':<10}{'Age':<5}{'Sex':<7}{'Status':<15}{'Activity Level':<20}{'Diet Recommendation':<80}{'Activity Advice':<40}\n")
    file.write("-" * 180 + "\n")
    for name, age, gender_symbol, status, activity, diet_recommendation, activity_advice, weight in results:
        file.write(f"{name:<10}{age:<5}{gender_symbol:<7}{status:<15}{activity:<20}{diet_recommendation:<80}{activity_advice:<40}\n")

# Separate the cats into kittens and adults based on age
kittens = [cat for cat in results if cat[1] < 1]  # Filter for kittens where age is less than 1
adults = [cat for cat in results if cat[1] >= 1]  # Filter for adults where age is 1 or greater

# Create charts for kittens and adults separately with gender information on top

# Function to create a bar chart for weight status
def create_weight_chart(cats, title, chart_output_path):
    names = [cat[0] for cat in cats]
    weights = [cat[7] for cat in cats]  # Use the actual weights from results (index 7)
    statuses = [cat[3] for cat in cats]  # Use the weight status (index 3)
    genders = [cat[2] for cat in cats]  # Male/Female for name coloring (index 2)

    # Darker color adjustments
    status_colors = ['#6BCB77' if status == 'normal' else '#F2D37A' if status == 'underweight' else '#FF4F58' for status in statuses]
    
    # Assign name colors based on gender
    name_colors = ['#5F9FFF' if gender == '♂' else '#F48CBB' for gender in genders]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(names, weights, color=status_colors)

    ax.set_xlabel("Cat Name", fontsize=12)
    ax.set_ylabel("Weight (kg)", fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # Change name colors (x-ticks) based on sex (blue for males, pink for females)
    for tick, label in zip(range(len(names)), ax.get_xticklabels()):
        label.set_color(name_colors[tick])

    # Add a legend to explain the color coding
    legend_labels = ["Normal Weight", "Underweight", "Overweight"]
    legend_colors = ["#6BCB77", "#F2D37A", "#FF4F58"]
    for color, label in zip(legend_colors, legend_labels):
        ax.bar(0, 0, color=color, label=label)  # Dummy bars for legend
    ax.legend(title="Weight Status", loc="upper right")

    # Save and display the chart
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(chart_output_path)
    plt.show()

# Create separate charts for kittens and adults
kittens_chart_path = os.path.join(output_folder, "kittens_weight_chart.png")
adults_chart_path = os.path.join(output_folder, "adults_weight_chart.png")

create_weight_chart(kittens, "Kittens Weight Status", kittens_chart_path)
create_weight_chart(adults, "Adults Weight Status", adults_chart_path)
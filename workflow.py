import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 8))

# Define the positions of the boxes
positions = {
    "User Input": (0.5, 0.9),
    "Description Provided?": (0.5, 0.75),
    "Check Vector DB": (0.25, 0.6),
    "Retrieve Document & Answer": (0.25, 0.45),
    "Data Not Available": (0.75, 0.6),
    "No Description": (0.75, 0.75),
    "Parse Document": (0.5, 0.3),
    "Parsed Correctly?": (0.5, 0.15),
    "Check Hallucination Flag?": (0.5, 0.05),
}

# Define the connections
connections = [
    ("User Input", "Description Provided?"),
    ("Description Provided?", "Check Vector DB"),
    ("Description Provided?", "No Description"),
    ("Check Vector DB", "Retrieve Document & Answer"),
    ("Check Vector DB", "Data Not Available"),
    ("No Description", "Retrieve Document & Answer"),
    ("Retrieve Document & Answer", "Parse Document"),
    ("Parse Document", "Parsed Correctly?"),
    ("Parsed Correctly?", "Check Hallucination Flag?"),
    ("Parsed Correctly?", "Data Not Available"),
]

# Draw boxes
for label, (x, y) in positions.items():
    ax.add_patch(mpatches.Rectangle((x - 0.15, y - 0.05), 0.3, 0.1, edgecolor='black', facecolor='lightblue'))
    ax.text(x, y, label, ha="center", va="center", fontsize=10)

# Draw arrows
arrow_style = dict(facecolor='black', width=0.005, head_width=0.03)
for start, end in connections:
    start_x, start_y = positions[start]
    end_x, end_y = positions[end]
    ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                arrowprops=dict(arrowstyle='->', color='black'))

# Set limits and remove axes
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

output_path = 'workflow_diagram.png'  # Path in the current repo or desired location
plt.title("Workflow Diagram", fontsize=14)
plt.savefig(output_path, dpi=300, bbox_inches='tight')

plt.title("Workflow Diagram", fontsize=14)
plt.show()

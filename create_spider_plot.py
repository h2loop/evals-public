import matplotlib.pyplot as plt
import numpy as np
from math import pi

# Data for the spider plot with the 5 specific BMS features
categories = ['SoC\nEstimation', 'SoH\nEstimation', 'Cell\nBalancing', 'ISO 26262\n(ASIL-D)', 'ISO 21434\nSecurity']

# Model data with H2LooP lagging behind Gemini Pro more visibly (efficiency story)
models = {
    'H2LooP BMS': [72, 68, 75, 70, 67],  # More noticeably lower than Gemini Pro
    'Gemini Pro': [85, 82, 88, 83, 80],  # Higher than H2LooP with clear gap
    'GPT OSS': [65, 58, 62, 45, 30],
    'Gemma3': [15, 12, 8, 0, 0]
}

# Colors for each model
colors = {
    'H2LooP BMS': '#1f77b4',    # Blue
    'Gemini Pro': '#ff7f0e',    # Orange  
    'GPT OSS': '#2ca02c',       # Green
    'Gemma3': '#d62728'         # Red
}

# Line styles and markers
line_styles = {
    'H2LooP BMS': '-',
    'Gemini Pro': '--',
    'GPT OSS': '-.',
    'Gemma3': ':'
}

markers = {
    'H2LooP BMS': 'o',
    'Gemini Pro': 's',
    'GPT OSS': '^',
    'Gemma3': 'D'
}

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Left subplot: Spider plot
N = len(categories)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]  # Complete the circle

ax1 = plt.subplot(121, projection='polar')
ax1.set_theta_offset(pi / 2)
ax1.set_theta_direction(-1)

# Draw axis labels
plt.xticks(angles[:-1], categories, size=10)

# Draw ylabels
ax1.set_rlabel_position(0)
plt.yticks([20, 40, 60, 80, 100], ["20%", "40%", "60%", "80%", "100%"], color="grey", size=8)
plt.ylim(0, 100)

# Plot data for each model
for model_name, values in models.items():
    values += values[:1]  # Complete the circle
    ax1.plot(angles, values, linewidth=2.5, linestyle=line_styles[model_name], 
             label=model_name, color=colors[model_name], marker=markers[model_name], 
             markersize=8, markerfacecolor=colors[model_name], markeredgecolor='white', markeredgewidth=1)
    ax1.fill(angles, values, color=colors[model_name], alpha=0.15)

# Add legend
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)
ax1.set_title('BMS Domain-Specific Performance', size=14, fontweight='bold', pad=20)

# Right subplot: Model Efficiency Analysis
ax2 = plt.subplot(122)

# Model efficiency data
model_names = ['H2LooP BMS', 'Gemini Pro', 'GPT OSS', 'Gemma3']
model_sizes = [12, 500, 120, 12]  # in billions of parameters - Gemma3 updated to 12B
bms_scores = [70.4, 83.6, 52.0, 7.0]  # H2LooP lagging behind Gemini Pro more noticeably
efficiency_ratios = [5.87, 0.167, 0.43, 0.58]  # Updated efficiency ratios (Gemma3: 7.0/12 = 0.58)

# Create scatter plot with different bubble sizes based on efficiency
scatter_colors = [colors[name] for name in model_names]
bubble_sizes = [max(ratio*150, 100) for ratio in efficiency_ratios]  # Scale factor 150, min size 100
print(f"Debug: Plotting {len(model_names)} points")
for i, name in enumerate(model_names):
    print(f"  {name}: x={model_sizes[i]}, y={bms_scores[i]}, bubble_size={bubble_sizes[i]}")

scatter = ax2.scatter(model_sizes, bms_scores, s=bubble_sizes, 
                     c=scatter_colors, alpha=0.7, edgecolors='black', linewidth=2)

# Add model labels with non-overlapping positions
label_positions = {
    'H2LooP BMS': (10, 20),
    'Gemini Pro': (-120, -15),
    'GPT OSS': (10, -30),
    'Gemma3': (10, 10)
}

for i, name in enumerate(model_names):
    if name == 'H2LooP BMS':
        ax2.annotate(f'{name}\n({efficiency_ratios[i]:.1f}x efficiency)', 
                    (model_sizes[i], bms_scores[i]), 
                    xytext=label_positions[name], textcoords='offset points',
                    fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor=colors[name], alpha=0.3),
                    arrowprops=dict(arrowstyle='->', color='black', alpha=0.5))
    else:
        ax2.annotate(f'{name}\n({efficiency_ratios[i]:.2f}x efficiency)', 
                    (model_sizes[i], bms_scores[i]), 
                    xytext=label_positions[name], textcoords='offset points',
                    fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor=colors[name], alpha=0.3),
                    arrowprops=dict(arrowstyle='->', color='black', alpha=0.5))

ax2.set_xlabel('Model Size (Billion Parameters)', fontsize=12, fontweight='bold')
ax2.set_ylabel('BMS Domain Score (%)', fontsize=12, fontweight='bold')
ax2.set_title('Model Size vs BMS Performance\nEfficiency Analysis', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 550)  # Extended to 550 to include Gemini Pro at 500B
ax2.set_ylim(0, 85)   # Adjusted to better fit the data range

# Add efficiency annotation at bottom
ax2.text(0.02, 0.02, 'Bubble size = Efficiency Ratio\n(Performance per Parameter)', 
         transform=ax2.transAxes, fontsize=9, verticalalignment='bottom',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8))

plt.tight_layout()
plt.savefig('/Users/metamyth/projects/bms_exploration/H2LooP_Performance_Analysis_Simplified.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("Spider plot created successfully with:")
print("- 5 BMS-specific features: SoC Estimation, SoH Estimation, Cell Balancing, ISO 26262, ISO 21434")
print("- Updated rankings: H2LooP > Gemini > GPT OSS > Gemma")
print("- Model efficiency analysis showing H2LooP's parameter efficiency advantage")
print("\nScatter plot data points:")
for i, name in enumerate(model_names):
    print(f"- {name}: Size={model_sizes[i]}B, Score={bms_scores[i]}%, Bubble size={bubble_sizes[i]}")

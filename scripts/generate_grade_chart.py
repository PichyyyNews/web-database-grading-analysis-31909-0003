import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path

# Load TH SarabunPSK
font_path = Path(r'C:\Users\Newsk\.gemini\config\skills\matplotlib-creator\fonts\THSarabun.ttf')
bold_font_path = Path(r'C:\Users\Newsk\.gemini\config\skills\matplotlib-creator\fonts\THSarabun Bold.ttf')
fm.fontManager.addfont(str(font_path))
fm.fontManager.addfont(str(bold_font_path))
font_prop = fm.FontProperties(fname=str(font_path))
bold_prop = fm.FontProperties(fname=str(bold_font_path))

# Base RC Settings
mpl.rcParams.update({
    'figure.constrained_layout.use': True,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': False,
    'axes.axisbelow': True,
    'font.family': font_prop.get_name(),
    'font.size': 18,
    'font.weight': 'normal',
    'axes.titlesize': 22,
    'axes.titleweight': 'bold',
    'axes.labelsize': 20,
    'axes.labelweight': 'bold',
    'xtick.labelsize': 18,
    'ytick.labelsize': 18,
    'legend.frameon': False,
    'legend.fontsize': 18,
    'axes.unicode_minus': False,
})

# Data definition
grades = ['0.0', '1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0']
counts = [0, 6, 1, 1, 2, 3, 1, 5]
total_students = sum(counts)
percentages = [(c / total_students) * 100 for c in counts]

# Create Figure & Axes
fig, ax = plt.subplots(figsize=(10, 6.2), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

# Spines styling
ax.spines['left'].set_color('#CBD5E1')
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_color('#CBD5E1')
ax.spines['bottom'].set_linewidth(1.2)

# Grid styling: Horizontal only
ax.yaxis.grid(True, linestyle='--', linewidth=0.7, alpha=0.85, color='#E2E8F0')
ax.xaxis.grid(False)

# Bar chart
bar_width = 0.52
x_pos = list(range(len(grades)))

# Color scheme: Academic Document primary (#1D4ED8)
colors = ['#DC2626' if c == 0 else '#1D4ED8' for c in counts]

bars = ax.bar(x_pos, counts, width=bar_width, color=colors, edgecolor='#1E3A8A', linewidth=1.0, alpha=0.92)

# Floor marker for 0.0
floor_x = x_pos[0]
ax.plot([floor_x - bar_width/2, floor_x + bar_width/2], [0, 0], color='#DC2626', linewidth=2.5)

# Labels above bars
for i, (rect, count, pct) in enumerate(zip(bars, counts, percentages)):
    x = rect.get_x() + rect.get_width() / 2.0
    if count > 0:
        y = rect.get_height()
        label_text = f'{count} คน\n({pct:.1f}%)'
        ax.text(x, y + 0.15, label_text, ha='center', va='bottom',
                fontproperties=font_prop, fontsize=17, color='#111827',
                linespacing=1.1)
    else:
        # Zero-count representation
        label_text = '0 คน\n(0.0%)'
        ax.text(x, 0.15, label_text, ha='center', va='bottom',
                fontproperties=font_prop, fontsize=17, color='#DC2626',
                linespacing=1.1)

# Axis configuration
ax.set_xticks(x_pos)
ax.set_xticklabels(grades, fontproperties=bold_prop, fontsize=18)
ax.set_xlabel('ระดับผลการเรียน (เกรด)', fontproperties=bold_prop, fontsize=20, labelpad=10, color='#111827')

ax.set_yticks(range(0, 8))
ax.set_yticklabels([str(y) for y in range(0, 8)], fontproperties=font_prop, fontsize=18)
ax.set_ylabel('จำนวนนักเรียน (คน)', fontproperties=bold_prop, fontsize=20, labelpad=10, color='#111827')
ax.set_ylim(0, 7.6)

# Title
ax.set_title('การแจกแจงระดับผลการเรียน 8 ระดับ รายวิชา 31909-0003 (1 สทค 2)',
             fontproperties=bold_prop, fontsize=22, pad=16, color='#111827')

# Save outputs
output_png = Path('charts/grade_distribution_bar.png')
output_svg = Path('charts/grade_distribution_bar.svg')
output_png.parent.mkdir(parents=True, exist_ok=True)

fig.savefig(output_png, dpi=300, bbox_inches='tight', pad_inches=0.2)
fig.savefig(output_svg, bbox_inches='tight', pad_inches=0.2)
plt.close(fig)

print(f'Generated {output_png} and {output_svg} successfully.')

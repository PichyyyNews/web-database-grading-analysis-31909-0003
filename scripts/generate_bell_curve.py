import numpy as np
import scipy.stats as stats
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pathlib import Path

# Load TH SarabunPSK
font_path = Path(r'C:\Users\Newsk\.gemini\config\skills\mathplot\fonts\THSarabun.ttf')
bold_font_path = Path(r'C:\Users\Newsk\.gemini\config\skills\mathplot\fonts\THSarabun Bold.ttf')

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

scores = np.array([
    79.53, 80.50, 53.43, 82.30, 55.23, 82.63, 68.67, 59.33, 52.97,
    57.73, 52.83, 74.27, 52.77, 84.30, 75.57, 73.23, 72.40, 70.17, 53.87
])


mean_val = float(np.mean(scores))
std_val = float(np.std(scores, ddof=1))
n_students = len(scores)

# X range for curve
x = np.linspace(25, 105, 600)
pdf = stats.norm.pdf(x, mean_val, std_val)

fig, ax = plt.subplots(figsize=(10.5, 6.4), facecolor='#FFFFFF')
ax.set_facecolor('#FFFFFF')

# Spines styling
ax.spines['left'].set_color('#CBD5E1')
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_color('#CBD5E1')
ax.spines['bottom'].set_linewidth(1.2)

# Grid styling: Horizontal only
ax.yaxis.grid(True, linestyle='--', linewidth=0.7, alpha=0.85, color='#E2E8F0')
ax.xaxis.grid(False)

# Shading: passing area (>= 50) and failing area (< 50)
x_pass = x[x >= 50]
pdf_pass = pdf[x >= 50]
ax.fill_between(x_pass, 0, pdf_pass, color='#2563EB', alpha=0.18)

x_fail = x[x < 50]
pdf_fail = pdf[x < 50]
ax.fill_between(x_fail, 0, pdf_fail, color='#DC2626', alpha=0.10)

# Bell curve line
ax.plot(x, pdf, color='#1D4ED8', linewidth=2.6)

# Cutoff threshold line at 50 (Seamless, stopping neatly at curve)
y_50 = float(stats.norm.pdf(50, mean_val, std_val))
ax.vlines(50, 0, y_50, color='#DC2626', linestyle='--', linewidth=2.0)
ax.plot(50, y_50, marker='o', markersize=6, color='#DC2626')
ax.text(48.5, y_50 + 0.0018, 'เกณฑ์ผ่าน 50 คะแนน', color='#DC2626',
        fontproperties=bold_prop, fontsize=17, ha='right', va='bottom')

# Mean line
y_mean = float(stats.norm.pdf(mean_val, mean_val, std_val))
ax.vlines(mean_val, 0, y_mean, color='#0D9488', linestyle='--', linewidth=2.0)
ax.plot(mean_val, y_mean, marker='o', markersize=6, color='#0D9488')
ax.text(mean_val, y_mean + 0.0018, f'คะแนนเฉลี่ย ({mean_val:.2f})\nS.D. = {std_val:.2f}',
        color='#0D9488', fontproperties=bold_prop, fontsize=17, ha='center', va='bottom',
        linespacing=1.1)

# Individual student score scatter with vertical jitter for zero occlusion
np.random.seed(42)
y_jitter = 0.0008 + np.random.uniform(0, 0.0016, size=len(scores))
ax.scatter(scores, y_jitter, color='#1D4ED8', edgecolor='#1E3A8A', s=55, alpha=0.85, zorder=5)

# Axis configuration
ax.set_xlim(25, 105)
ax.set_xticks(range(30, 110, 10))
ax.set_xticklabels([str(val) for val in range(30, 110, 10)], fontproperties=font_prop, fontsize=18)
ax.set_xlabel('คะแนนรวมสุทธิ (100 คะแนน)', fontproperties=bold_prop, fontsize=20, labelpad=10, color='#111827')

ax.set_ylim(0, 0.041)
ax.set_ylabel('ความหนาแน่นของความน่าจะเป็น (Density)', fontproperties=bold_prop, fontsize=20, labelpad=10, color='#111827')

# Legend in upper right (frameless, compact, consistent Thai typography)
legend_elements = [
    plt.Line2D([0], [0], color='#1D4ED8', lw=2.5, label='เส้นโค้งปกติ (Normal Distribution)'),
    plt.Line2D([0], [0], color='#0D9488', lw=2, linestyle='--', label=f'คะแนนเฉลี่ย = {mean_val:.2f} (S.D. = {std_val:.2f})'),
    plt.Line2D([0], [0], color='#DC2626', lw=2, linestyle='--', label='เกณฑ์ผ่าน = 50.00 คะแนน'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#1D4ED8', markeredgecolor='#1E3A8A', markersize=8, label=f'คะแนนนักเรียนจริง (n = {n_students} คน)')
]
ax.legend(handles=legend_elements, loc='upper right', frameon=False, fontsize=16.5,
          handlelength=1.4, handletextpad=0.5, labelspacing=0.45)

# Title
ax.set_title('การแจกแจงคะแนนรวมสุทธิแบบโค้งปกติ รายวิชา 31909-0003 (1 สทค 2)',
             fontproperties=bold_prop, fontsize=22, pad=16, color='#111827')

# Save outputs
output_png = Path('charts/bell_curve_score_distribution.png')
output_svg = Path('charts/bell_curve_score_distribution.svg')
fig.savefig(output_png, dpi=300, bbox_inches='tight', pad_inches=0.2)
fig.savefig(output_svg, bbox_inches='tight', pad_inches=0.2)
plt.close(fig)

print(f'Generated {output_png} and {output_svg} successfully.')

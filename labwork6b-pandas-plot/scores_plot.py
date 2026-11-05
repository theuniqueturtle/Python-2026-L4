import os

import pandas as pd
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
COURSES = ["math", "python", "database"]

df = pd.read_csv(os.path.join(HERE, "scores.csv"))

fig, ax = plt.subplots(figsize=(12, 5))
for course in COURSES:
    ax.scatter(df["student_id"], df[course], label=course)
ax.set_title("Student scores")
ax.set_xlabel("Student")
ax.set_ylabel("Score")
ax.tick_params(axis="x", rotation=90)
ax.grid(True, alpha=0.3)
ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1))
fig.tight_layout()
fig.savefig(os.path.join(HERE, "scattered.png"), dpi=150)


fig, axes = plt.subplots(1, 3, figsize=(14, 4), sharex=True, sharey=True)
for ax, course in zip(axes, COURSES):
    ax.hist(df[course].dropna(), bins=8, edgecolor="black")
    ax.set_title(course)
    ax.set_xlabel("Score")
axes[0].set_ylabel("Number of students")
fig.suptitle("Histogram of marks per course")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "histo.png"), dpi=150)

fig, ax = plt.subplots(figsize=(6, 5))
df[COURSES].plot.box(ax=ax)        # pandas ignores the empty (NaN) scores
ax.set_title("Box plot of marks")
ax.set_ylabel("Score")
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "box.png"), dpi=150)

plt.show()

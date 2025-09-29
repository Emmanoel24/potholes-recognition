import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1️⃣ Load the detection data
df = pd.read_csv("detections_log.csv")

# 2️⃣ Convert timestamps to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# 3️⃣ Plot detection count over time
plt.figure(figsize=(10, 5))
df["timestamp"].value_counts().sort_index().plot(kind="line")
plt.title("📊 Detections Over Time")
plt.xlabel("Time")
plt.ylabel("Number of Detections")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4️⃣ Plot class distribution
plt.figure(figsize=(7, 5))
sns.countplot(data=df, x="class", palette="coolwarm")
plt.title("🚗 Detection Class Distribution")
plt.xlabel("Detected Object")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# 5️⃣ Plot confidence distribution
plt.figure(figsize=(7, 5))
sns.histplot(df["confidence"], bins=20, kde=True, color="green")
plt.title("📈 Confidence Score Distribution")
plt.xlabel("Confidence")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()
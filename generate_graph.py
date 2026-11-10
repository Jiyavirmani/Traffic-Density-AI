import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV file
data = pd.read_csv("output/traffic_data.csv")


plt.figure()
plt.plot(data["Time"], data["Vehicles"], marker="o")
plt.title("Vehicle Flow Over Time")
plt.xlabel("Time")
plt.ylabel("Number of Vehicles")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("output/vehicle_flow_graph.png")

plt.close()



plt.figure()
sns.countplot(x="Density", data=data)

plt.title("Traffic Density Distribution")
plt.xlabel("Density Level")
plt.ylabel("Frequency")

plt.tight_layout()
plt.savefig("output/density_graph.png")

plt.close()

print("Graphs generated successfully!")
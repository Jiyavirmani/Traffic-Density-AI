from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd

# Load CSV
data = pd.read_csv("output/traffic_data.csv")

# Stats
total_vehicles = data["Vehicles"].sum()
avg_vehicles = data["Vehicles"].mean()
max_vehicles = data["Vehicles"].max()

most_common_density = data["Density"].mode()[0]
max_signal = data["SignalTime"].max()
total_alerts = (data["Alert"] == "YES").sum()

peak_row = data.loc[data["Vehicles"].idxmax()]
peak_time = peak_row["Time"]
peak_value = peak_row["Vehicles"]

# Create PDF
doc = SimpleDocTemplate("output/traffic_report.pdf")
styles = getSampleStyleSheet()
elements = []

# Title
elements.append(Paragraph("AI Traffic Monitoring Report", styles['Title']))
elements.append(Spacer(1, 20))

# SECTION 1: Summary
elements.append(Paragraph("Summary", styles['Heading2']))
elements.append(Spacer(1, 10))

elements.append(Paragraph(f"Total Vehicles Detected: {total_vehicles}", styles['Normal']))
elements.append(Paragraph(f"Average Vehicles per Interval: {avg_vehicles:.2f}", styles['Normal']))
elements.append(Paragraph(f"Peak Traffic Count: {max_vehicles}", styles['Normal']))
elements.append(Spacer(1, 20))

# SECTION 2: AI Insights
elements.append(Paragraph("AI-Based Insights", styles['Heading2']))
elements.append(Spacer(1, 10))

elements.append(Paragraph(f"Most Frequent Density Level: {most_common_density}", styles['Normal']))
elements.append(Paragraph(f"Maximum Signal Time Suggested: {max_signal} seconds", styles['Normal']))
elements.append(Paragraph(f"Traffic Jam Alerts Triggered: {total_alerts}", styles['Normal']))
elements.append(Paragraph(f"Peak Traffic Time: {peak_time} with {peak_value} vehicles", styles['Normal']))
elements.append(Spacer(1, 20))

# SECTION 3: Graphs
elements.append(Paragraph("Vehicle Flow Analysis", styles['Heading2']))
elements.append(Image("output/vehicle_flow_graph.png", width=400, height=250))
elements.append(Spacer(1, 20))

elements.append(Paragraph("Traffic Density Distribution", styles['Heading2']))
elements.append(Image("output/density_graph.png", width=400, height=250))
elements.append(Spacer(1, 20))

# SECTION 4: System Intelligence
elements.append(Paragraph("System Intelligence", styles['Heading2']))
elements.append(Spacer(1, 10))

elements.append(Paragraph(
    "The system dynamically analyzes traffic patterns and provides intelligent decision support such as adaptive signal timing, "
    "congestion detection, and peak traffic identification. These capabilities demonstrate the transition from simple monitoring "
    "to an AI-driven traffic management system.",
    styles['Normal']
))
elements.append(Spacer(1, 20))

# SECTION 5: Conclusion
elements.append(Paragraph("Conclusion", styles['Heading2']))
elements.append(Spacer(1, 10))

elements.append(Paragraph(
    "This report highlights the effectiveness of the AI-based traffic monitoring system in detecting, analyzing, and interpreting "
    "traffic conditions. The integration of detection, analytics, and decision-making enables real-time traffic optimization and "
    "provides valuable insights for smart city applications.",
    styles['Normal']
))

# Build
doc.build(elements)

print("✅ FINAL PDF Generated Successfully")
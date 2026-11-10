# import streamlit as st
# import os

# st.title("🚦 AI Traffic Monitoring System")

# st.write("Upload a video and analyze traffic using AI")

# # Upload video
# uploaded_file = st.file_uploader("Upload Traffic Video", type=["mp4"])

# if uploaded_file is not None:

#     # Save uploaded file
#     with open("data/uploaded_video.mp4", "wb") as f:
#         f.write(uploaded_file.read())

#     st.success("Video uploaded successfully!")

#     if st.button("▶️ Run Analysis"):

#         st.write("Running AI model... Please wait ⏳")

#         # Run your existing script (NO CHANGE)
#         os.system("python video_test.py")

#         st.success("Analysis Complete!")

#         # Show outputs
#         st.subheader("📊 Results")

#         if os.path.exists("output/vehicle_flow_graph.png"):
#             st.image("output/vehicle_flow_graph.png", caption="Vehicle Flow")

#         if os.path.exists("output/density_graph.png"):
#             st.image("output/density_graph.png", caption="Traffic Density")

#         if os.path.exists("output/traffic_report.pdf"):
#             with open("output/traffic_report.pdf", "rb") as f:
#                 st.download_button(
#                     "📄 Download PDF Report",
#                     f,
#                     file_name="traffic_report.pdf"
#                 )
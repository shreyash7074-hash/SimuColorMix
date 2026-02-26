import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# -------------------------------
# App Title & Description
# -------------------------------
st.title("🎨 IoT-based Real-Time Color Recognition & Mixing Simulator")

st.markdown("""
This simulator extracts colors from an uploaded image, shows RGB values,  
and simulates the mixing process using virtual pumps.
""")

# -------------------------------
# Image Upload
# -------------------------------
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:

    # Open image using PIL
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Convert PIL image to OpenCV format (BGR)
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # -------------------------------
    # Pixel Selection
    # -------------------------------
    st.subheader("Select Pixel Coordinates")

    x = st.number_input(
        "X coordinate (width)",
        min_value=0,
        max_value=img_cv.shape[1] - 1,
        value=50
    )

    y = st.number_input(
        "Y coordinate (height)",
        min_value=0,
        max_value=img_cv.shape[0] - 1,
        value=50
    )

    # Extract BGR values
    b, g, r = img_cv[int(y), int(x)]
    rgb_color = (r, g, b)

    st.write(f"**Extracted Color (R, G, B): {rgb_color}**")

    # -------------------------------
    # Color Preview
    # -------------------------------
    st.markdown("### Selected Color Preview")
    st.color_picker(
        "Extracted Color",
        f"#{r:02x}{g:02x}{b:02x}"
    )

    # -------------------------------
    # Pump Simulation Calculation
    # -------------------------------
    total = r + g + b if (r + g + b) > 0 else 1

    r_perc = (r / total) * 100
    g_perc = (g / total) * 100
    b_perc = (b / total) * 100

    st.markdown("### Pump Simulation (RGB Proportions)")
    st.write(f"🔴 Red Pump: {r_perc:.2f}%")
    st.write(f"🟢 Green Pump: {g_perc:.2f}%")
    st.write(f"🔵 Blue Pump: {b_perc:.2f}%")

    # -------------------------------
    # Bar Chart Visualization
    # -------------------------------
    fig, ax = plt.subplots()
    pumps = ['Red', 'Green', 'Blue']
    values = [r_perc, g_perc, b_perc]

    ax.bar(pumps, values, color=['red', 'green', 'blue'])
    ax.set_ylabel("Pump Strength (%)")
    ax.set_ylim(0, 100)

    st.pyplot(fig)

    # -------------------------------
    # Final Mixed Color Output
    # -------------------------------
    st.markdown("### Final Mixed Color")

    final_color = np.zeros((100, 100, 3), np.uint8)
    final_color[:] = (b, g, r)  # OpenCV uses BGR

    st.image(final_color, caption="Mixed Output Color", use_container_width=False)
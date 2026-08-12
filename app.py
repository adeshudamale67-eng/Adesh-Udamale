import streamlit as st

st.set_page_config(
    page_title="Smart Agriculture Advisor",
    page_icon="🌱",
    layout="wide"
)

# ---------------- START SCREEN ----------------

if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:

    st.markdown(
        """
        <div style="text-align:center; padding-top:120px;">
            <div style="font-size:80px;">🌱</div>
            <h1>Smart Agriculture Advisor</h1>
            <h3>Technology for Better Farming</h3>
            <p style="font-size:18px;">
                Get suitable crop recommendations using soil and weather conditions.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button(
            "🚀 Start Now",
            use_container_width=True,
            type="primary"
        ):
            st.session_state.started = True
            st.rerun()

    st.stop()


# ---------------- MAIN PROJECT ----------------

st.title("🌱 Smart Agriculture Advisor")
st.subheader("Technology for Better Farming")

st.write(
    "Enter soil and weather conditions to get a suitable crop recommendation."
)

st.divider()

st.header("🌾 Enter Agricultural Details")

col1, col2, col3 = st.columns(3)

with col1:
    nitrogen = st.number_input(
        "Nitrogen (N)",
        min_value=0.0,
        value=80.0
    )

    phosphorus = st.number_input(
        "Phosphorus (P)",
        min_value=0.0,
        value=45.0
    )

with col2:
    potassium = st.number_input(
        "Potassium (K)",
        min_value=0.0,
        value=40.0
    )

    ph = st.number_input(
        "pH Value",
        min_value=0.0,
        max_value=14.0,
        value=6.5
    )

with col3:
    temperature = st.number_input(
        "Temperature (°C)",
        value=26.0
    )

    rainfall = st.number_input(
        "Rainfall (mm)",
        min_value=0.0,
        value=180.0
    )

st.write("")


# ---------------- CROP PREDICTION ----------------

def predict_crop(n, p, k, ph, temperature, rainfall):

    if rainfall > 220 and temperature > 24:
        crop = "Rice"
        tips = [
            "Maintain adequate water availability.",
            "Monitor field drainage.",
            "Use balanced nutrients based on soil testing."
        ]

    elif temperature > 27 and rainfall > 120:
        crop = "Maize"
        tips = [
            "Maintain regular irrigation.",
            "Monitor nitrogen levels.",
            "Control weeds during early growth."
        ]

    elif rainfall < 100 and temperature > 25:
        crop = "Millet"
        tips = [
            "Use water-efficient irrigation.",
            "Maintain suitable soil moisture.",
            "Choose a locally suitable variety."
        ]

    elif 6 <= ph <= 7.5 and 18 <= temperature <= 30:
        crop = "Wheat"
        tips = [
            "Maintain balanced N-P-K levels.",
            "Avoid over-irrigation.",
            "Monitor soil moisture regularly."
        ]

    else:
        crop = "Wheat"
        tips = [
            "Check soil conditions regularly.",
            "Maintain proper irrigation.",
            "Follow local agricultural guidance."
        ]

    return crop, tips


# ---------------- PREDICT BUTTON ----------------

if st.button(
    "🤖 Predict Suitable Crop",
    use_container_width=True
):

    crop, tips = predict_crop(
        nitrogen,
        phosphorus,
        potassium,
        ph,
        temperature,
        rainfall
    )

    st.divider()

    st.success("Prediction Completed Successfully!")

    st.header("📊 Prediction Result")

    st.markdown(
        f"""
        ## 🌱 Recommended Crop: *{crop}*
        """
    )

    st.info(
        "Recommended for the given soil and weather conditions."
    )

    # Input Summary
    st.subheader("📋 Input Summary")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Nitrogen", nitrogen)
        st.metric("Phosphorus", phosphorus)

    with c2:
        st.metric("Potassium", potassium)
        st.metric("pH", ph)

    with c3:
        st.metric(
            "Temperature",
            f"{temperature} °C"
        )

        st.metric(
            "Rainfall",
            f"{rainfall} mm"
        )

    # Recommendations
    st.subheader("💡 Farming Recommendations")

    for tip in tips:
        st.write("✅", tip)


st.divider()

st.caption(
    "Smart Agriculture Advisor | AI/ML Project Demo"
)

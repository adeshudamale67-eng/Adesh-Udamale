import streamlit as st
import sqlite3
import hashlib

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Smart Agriculture Advisor",
    page_icon="🌱",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        margin-top: 80px;
    }

    .sub-title {
        text-align: center;
        font-size: 24px;
        margin-top: 10px;
    }

    .description {
        text-align: center;
        font-size: 18px;
        margin-top: 20px;
        margin-bottom: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DATABASE
# =========================================================

def init_database():

    conn = sqlite3.connect("farmers.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            mobile TEXT NOT NULL,
            password TEXT NOT NULL,
            location TEXT
        )
        """
    )

    conn.commit()
    conn.close()


# =========================================================
# PASSWORD HASHING
# =========================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# =========================================================
# CREATE ACCOUNT
# =========================================================

def create_account(
    name,
    email,
    mobile,
    password,
    location
):

    conn = sqlite3.connect("farmers.db")
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO farmers
            (name, email, mobile, password, location)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                name,
                email,
                mobile,
                hash_password(password),
                location
            )
        )

        conn.commit()

        success = True

    except sqlite3.IntegrityError:

        success = False

    conn.close()

    return success


# =========================================================
# LOGIN
# =========================================================

def login_user(email, password):

    conn = sqlite3.connect("farmers.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name, email, location
        FROM farmers
        WHERE email = ? AND password = ?
        """,
        (
            email,
            hash_password(password)
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user


# =========================================================
# INITIALIZE DATABASE
# =========================================================

init_database()


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:

    st.session_state.page = "welcome"


if "user" not in st.session_state:

    st.session_state.user = None


# =========================================================
# WELCOME / START PAGE
# =========================================================

if st.session_state.page == "welcome":

    st.write("")
    st.write("")
    st.write("")

    st.markdown(
        '<div class="main-title">'
        '🌱 Smart Agriculture Advisor'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">'
        'Technology for Better Farming'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="description">'
        'Get suitable crop recommendations using '
        'soil and weather conditions.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        if st.button(
            "🚀 Start Now",
            use_container_width=True,
            type="primary"
        ):

            st.session_state.page = "login"

            st.rerun()

    st.write("")
    st.write("")

    st.caption(
        "Smart Agriculture Advisor | AI/ML Project Demo"
    )

    st.stop()


# =========================================================
# LOGIN / CREATE ACCOUNT PAGE
# =========================================================

if st.session_state.page == "login":

    st.title("🔐 Farmer Login")

    st.subheader(
        "Login or create your farmer account"
    )

    st.write(
        "Access Smart Agriculture Advisor "
        "to get crop recommendations."
    )

    st.divider()

    # -----------------------------------------------------
    # TABS
    # -----------------------------------------------------

    tab1, tab2 = st.tabs(
        [
            "🔑 Login",
            "📝 Create Account"
        ]
    )


    # =====================================================
    # LOGIN TAB
    # =====================================================

    with tab1:

        st.subheader(
            "Login to Your Account"
        )

        email = st.text_input(
            "📧 Email",
            key="login_email"
        )

        password = st.text_input(
            "🔒 Password",
            type="password",
            key="login_password"
        )

        st.write("")

        if st.button(
            "🔐 Login",
            use_container_width=True,
            type="primary"
        ):

            if email.strip() == "" or password == "":

                st.warning(
                    "Please enter email and password."
                )

            else:

                user = login_user(
                    email.strip(),
                    password
                )

                if user:

                    st.session_state.user = user

                    st.session_state.page = "dashboard"

                    st.success(
                        "Login successful! 🎉"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid email or password."
                    )


    # =====================================================
    # CREATE ACCOUNT TAB
    # =====================================================

    with tab2:

        st.subheader(
            "👨‍🌾 Create Farmer Account"
        )

        name = st.text_input(
            "👤 Farmer Name"
        )

        new_email = st.text_input(
            "📧 Email"
        )

        mobile = st.text_input(
            "📱 Mobile Number"
        )

        location = st.text_input(
            "📍 Village / Location"
        )

        new_password = st.text_input(
            "🔒 Password",
            type="password"
        )

        confirm_password = st.text_input(
            "🔒 Confirm Password",
            type="password"
        )

        st.write("")

        if st.button(
            "📝 Create Account",
            use_container_width=True,
            type="primary"
        ):

            if (
                name.strip() == ""
                or new_email.strip() == ""
                or mobile.strip() == ""
                or new_password == ""
            ):

                st.warning(
                    "Please fill all required fields."
                )

            elif new_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(new_password) < 4:

                st.warning(
                    "Password should contain at least 4 characters."
                )

            else:

                success = create_account(
                    name.strip(),
                    new_email.strip(),
                    mobile.strip(),
                    new_password,
                    location.strip()
                )

                if success:

                    st.success(
                        "Account created successfully! 🎉 "
                        "You can now login."
                    )

                else:

                    st.error(
                        "An account with this email already exists."
                    )

    st.divider()

    if st.button(
        "⬅️ Back to Home",
        use_container_width=True
    ):

        st.session_state.page = "welcome"

        st.rerun()

    st.stop()


# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.page == "dashboard":

    user = st.session_state.user


    # =====================================================
    # HEADER
    # =====================================================

    st.title(
        "🌱 Smart Agriculture Advisor"
    )

    st.subheader(
        "Technology for Better Farming"
    )

    if user:

        st.write(
            f"Welcome, **{user[0]}**! 👨‍🌾"
        )

    st.write(
        "Enter soil and weather conditions "
        "to get a suitable crop recommendation."
    )


    # -----------------------------------------------------
    # LOGOUT
    # -----------------------------------------------------

    if st.button(
        "🚪 Logout"
    ):

        st.session_state.user = None

        st.session_state.page = "login"

        st.rerun()


    st.divider()


    # =====================================================
    # AGRICULTURAL INPUTS
    # =====================================================

    st.header(
        "🌾 Enter Agricultural Details"
    )

    col1, col2, col3 = st.columns(3)


    # -----------------------------------------------------
    # COLUMN 1
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # COLUMN 2
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # COLUMN 3
    # -----------------------------------------------------

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


    # =====================================================
    # CROP PREDICTION FUNCTION
    # =====================================================

    def predict_crop(
        n,
        p,
        k,
        ph,
        temperature,
        rainfall
    ):

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


        elif (
            6 <= ph <= 7.5
            and 18 <= temperature <= 30
        ):

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


    # =====================================================
    # PREDICT BUTTON
    # =====================================================

    if st.button(
        "🤖 Predict Suitable Crop",
        use_container_width=True,
        type="primary"
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


        # =================================================
        # RESULT
        # =================================================

        st.success(
            "Prediction Completed Successfully! 🎉"
        )

        st.header(
            "📊 Prediction Result"
        )

        st.markdown(
            f"""
            ## 🌱 Recommended Crop: **{crop}**
            """
        )

        st.info(
            "Recommended for the given soil "
            "and weather conditions."
        )


        # =================================================
        # INPUT SUMMARY
        # =================================================

        st.subheader(
            "📋 Input Summary"
        )

        c1, c2, c3 = st.columns(3)


        with c1:

            st.metric(
                "Nitrogen",
                nitrogen
            )

            st.metric(
                "Phosphorus",
                phosphorus
            )


        with c2:

            st.metric(
                "Potassium",
                potassium
            )

            st.metric(
                "pH",
                ph
            )


        with c3:

            st.metric(
                "Temperature",
                f"{temperature} °C"
            )

            st.metric(
                "Rainfall",
                f"{rainfall} mm"
            )


        # =================================================
        # FARMING RECOMMENDATIONS
        # =================================================

        st.subheader(
            "💡 Farming Recommendations"
        )

        for tip in tips:

            st.write(
                "✅",
                tip
            )


    st.divider()

    st.caption(
        "Smart Agriculture Advisor | "
        "AI/ML Project Demo"
    )

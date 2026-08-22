import os
import json
import joblib
import pandas as pd
import streamlit as st
import h2o

# =========================================================
# PROJECT PATHS
# =========================================================

root_dir = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
    )
)

dataset_path = os.path.join(
    root_dir,
    "Component_datasets",
    "Recidivism_cleaned_data.csv",
)

model_dir = os.path.join(
    root_dir,
    "models",
    "Recidivism_model",
)

model_file_path = os.path.join(
    model_dir,
    "StackedEnsemble_BestOfFamily_2_AutoML_1_20240719_183320.zip",
)

scaler_path = os.path.join(
    model_dir,
    "scaler.pkl",
)

frequency_path = os.path.join(
    model_dir,
    "frequency_encoding.json",
)

MODEL_FEATURES = [
    "District_Name",
    "age",
    "Profession",
    "PresentCity",
]

# =========================================================
# H2O INITIALIZATION
# =========================================================

@st.cache_resource
def init_h2o():
    """
    Initialize H2O once per Streamlit session.
    """
    try:
        h2o.init(nthreads=-1, max_mem_size="2G")
        return True
    except Exception:
        return False

# =========================================================
# DATA LOADER
# =========================================================

@st.cache_data
def load_data_recidivism():
    if not os.path.exists(dataset_path):
        st.error(f"Recidivism dataset not found:\n\n{dataset_path}")
        return None

    try:
        dataframe = pd.read_csv(dataset_path)
        if dataframe.empty:
            st.warning("Recidivism dataset contains no records.")
            return None
        return dataframe
    except Exception as error:
        st.error(f"Unable to load recidivism dataset: {error}")
        return None

@st.cache_resource
def load_model_recidivism():
    if not os.path.exists(model_file_path):
        raise FileNotFoundError(f"Recidivism MOJO model not found:\n{model_file_path}")

    if not init_h2o():
        raise RuntimeError("Java Runtime Environment (JRE 8+) is required for H2O AutoML models.")

    return h2o.import_mojo(model_file_path)

@st.cache_resource
def load_scaler():
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler file not found:\n{scaler_path}")
    return joblib.load(scaler_path)

@st.cache_data
def load_frequency_encoding():
    if not os.path.exists(frequency_path):
        raise FileNotFoundError(f"Frequency encoding file not found:\n{frequency_path}")
    with open(frequency_path, "r", encoding="utf-8") as file:
        return json.load(file)

def get_unique_values(dataframe, feature):
    if feature not in dataframe.columns:
        return []
    values = dataframe[feature].dropna().astype(str).str.strip()
    values = values[~values.str.lower().isin(["", "unknown", "nan"])]
    return sorted(values.unique().tolist())

def encode_category(frequency_data, feature, selected_value):
    feature_mapping = frequency_data.get(feature, {})
    return feature_mapping.get(selected_value, 0)

def validate_scaler_features(scaler):
    expected_feature_count = len(MODEL_FEATURES)
    if hasattr(scaler, "n_features_in_"):
        actual_feature_count = scaler.n_features_in_
        if actual_feature_count != expected_feature_count:
            st.error("⚠️ Existing preprocessing artifacts are incompatible with the corrected model.")
            st.warning(f"The current scaler expects {actual_feature_count} features, but CrimeNexus now uses {expected_feature_count} features.")
            st.info("The recidivism model and scaler must be retrained without the protected `Caste` attribute before prediction can be enabled.")
            st.code("Correct model features:\n\nDistrict_Name\nage\nProfession\nPresentCity")
            return False
    return True

def predictive_modeling_recidivism():
    st.subheader("Repeat Offense Prediction (Experimental Recidivism Model)")
    st.write("Explore an experimental machine-learning estimate using historical research data.")
    st.warning("⚠️ This module is a research prototype. Its output must not be used to determine guilt, target an individual, or make an operational law-enforcement decision.")

    h2o_ready = init_h2o()
    if not h2o_ready:
        st.info("ℹ️ **Java (JRE 8+) Environment Requirement**: Local H2O AutoML execution requires Java JRE to run predictions. Please install Java 8+ to enable live ML inferences.")

    cleaned_data = load_data_recidivism()
    if cleaned_data is None:
        return

    try:
        scaler = load_scaler()
    except Exception as error:
        st.error("Unable to load preprocessing scaler.")
        return

    if not validate_scaler_features(scaler):
        return

    try:
        frequency = load_frequency_encoding()
    except Exception as error:
        st.error("Unable to load frequency encoding data.")
        return

    unique_professions = get_unique_values(cleaned_data, "Profession")
    unique_districts = get_unique_values(cleaned_data, "District_Name")
    unique_cities = get_unique_values(cleaned_data, "PresentCity")

    with st.form("recidivism_prediction_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1)
            profession = st.selectbox("Profession", unique_professions)
        with col2:
            present_district = st.selectbox("Recorded Crime District", unique_districts)
            present_city = st.selectbox("Present City", unique_cities)

        submit_prediction = st.form_submit_button("Run Experimental Prediction", type="primary")

    if submit_prediction:
        if not h2o_ready:
            st.error("Cannot execute prediction because Java JRE is not detected on system.")
            return

        try:
            model = load_model_recidivism()
            profession_enc = encode_category(frequency, "Profession", profession)
            present_district_enc = encode_category(frequency, "District_Name", present_district)
            present_city_enc = encode_category(frequency, "PresentCity", present_city)

            new_data = pd.DataFrame({
                "District_Name": [present_district_enc],
                "age": [age],
                "Profession": [profession_enc],
                "PresentCity": [present_city_enc],
            }, columns=MODEL_FEATURES)

            new_data_scaled = scaler.transform(new_data)
            scaled_dataframe = pd.DataFrame(new_data_scaled, columns=MODEL_FEATURES, index=new_data.index)
            h2o_dataframe = h2o.H2OFrame(scaled_dataframe)

            predictions = model.predict(h2o_dataframe)
            predictions_df = predictions.as_data_frame()
            pred = predictions_df.loc[0, "predict"]

            st.divider()
            st.subheader("Experimental Model Output")
            if str(pred).strip() in {"0", "0.0", "False"}:
                st.success("🔵 **Lower Estimated Repeat-Offense Risk**")
            else:
                st.warning("🟠 **Higher Estimated Repeat-Offense Risk**")
        except Exception as error:
            st.error(f"Prediction execution notice: {error}")

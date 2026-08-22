import pandas as pd
import numpy as np
import streamlit as st
from pulp import LpVariable, LpProblem, LpMaximize, lpSum, PULP_CBC_CMD

def optimise_resource_allocation(district_name, sanctioned_asi, sanctioned_chc, sanctioned_cpc):
    district_df = district_name.copy()
    problem = LpProblem("Optimal_Resource_Allocation", LpMaximize)

    asi_vars = LpVariable.dicts("ASI", district_df.index, lowBound=0, cat='Integer')
    chc_vars = LpVariable.dicts("CHC", district_df.index, lowBound=0, cat='Integer')
    cpc_vars = LpVariable.dicts("CPC", district_df.index, lowBound=0, cat='Integer')

    problem += lpSum(district_df.loc[i, 'Normalised Crime Severity'] * (asi_vars[i] + chc_vars[i] + cpc_vars[i]) for i in district_df.index)

    problem += lpSum(asi_vars[i] for i in district_df.index) <= sanctioned_asi
    problem += lpSum(chc_vars[i] for i in district_df.index) <= sanctioned_chc
    problem += lpSum(cpc_vars[i] for i in district_df.index) <= sanctioned_cpc

    for i in district_df.index:
        problem += asi_vars[i] + chc_vars[i] + cpc_vars[i] >= 1

    for i in district_df.index:
        problem += asi_vars[i] <= max(1, sanctioned_asi * district_df.loc[i, 'Normalised Crime Severity'])
        problem += chc_vars[i] <= max(1, sanctioned_chc * district_df.loc[i, 'Normalised Crime Severity'])
        problem += cpc_vars[i] <= max(1, sanctioned_cpc * district_df.loc[i, 'Normalised Crime Severity'])

    problem.solve(PULP_CBC_CMD(msg=False))

    district_df['Allocated ASI'] = [int(np.round(asi_vars[i].varValue or 0)) for i in district_df.index]
    district_df['Allocated CHC'] = [int(np.round(chc_vars[i].varValue or 0)) for i in district_df.index]
    district_df['Allocated CPC'] = [int(np.round(cpc_vars[i].varValue or 0)) for i in district_df.index]

    return district_df

def allocate_resources(option, district_name, updated_asi, updated_chc, updated_cpc):
    st.info(f"**Sanctioned Strengths for {option}**: ASI: {updated_asi} | CHC: {updated_chc} | CPC: {updated_cpc}")

    with st.spinner("Optimizing resource allocation based on severity scores..."):
        updated_district = optimise_resource_allocation(district_name, updated_asi, updated_chc, updated_cpc)

    st.success("Optimization Complete.")

    police_units = ["All"] + sorted(district_name["Police Unit"].dropna().unique().tolist())
    selected_units = st.multiselect("Filter by Police Unit:", police_units, default=["All"])

    if "All" in selected_units or not selected_units:
        selected_data = updated_district
    else:
        selected_data = updated_district[updated_district["Police Unit"].isin(selected_units)]

    display_cols = ["Village Area Name", "Beat Name", "Normalised Crime Severity", "Allocated ASI", "Allocated CHC", "Allocated CPC"]
    avail_cols = [c for c in display_cols if c in selected_data.columns]
    
    st.dataframe(selected_data[avail_cols].reset_index(drop=True), use_container_width=True)

def resource_allocation(df):
    st.title("Police Resource Allocation and Management")
    options = ["Select the District"] + sorted(df["District Name"].dropna().unique().tolist())
    option = st.selectbox("Select District", options)

    if option != "Select the District":
        district_name = df[df["District Name"] == option].copy()
        
        default_asi = int(district_name['Sanctioned Strength of Assistant Sub-Inspectors per District'].iloc[0])
        default_chc = int(district_name['Sanctioned Strength of Head Constables per District'].iloc[0])
        default_cpc = int(district_name['Sanctioned Strength of Police Constables per District'].iloc[0])

        col1, col2, col3 = st.columns(3)
        with col1:
            sanctioned_asi = st.number_input("Sanctioned ASI", value=default_asi, min_value=1, step=1)
        with col2:
            sanctioned_chc = st.number_input("Sanctioned CHC", value=default_chc, min_value=1, step=1)
        with col3:
            sanctioned_cpc = st.number_input("Sanctioned CPC", value=default_cpc, min_value=1, step=1)

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("Use Default Strengths"):
                st.session_state.alloc_mode = "default"
        with btn_col2:
            if st.button("Optimize Allocation", type="primary"):
                st.session_state.alloc_mode = "custom"

        mode = st.session_state.get("alloc_mode", "default")
        if mode == "default":
            allocate_resources(option, district_name, default_asi, default_chc, default_cpc)
        else:
            allocate_resources(option, district_name, sanctioned_asi, sanctioned_chc, sanctioned_cpc)

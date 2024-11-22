import streamlit as st

st.set_page_config(
    page_title="Nutritionist",
    page_icon="🍎",
)

st.title("Nutritionist")

from agent import get_nutrition, get_goals
from profile_manager import create_profile, get_profile, get_notes
from form_manager import update_personal_info, add_note, delete_note

@st.fragment
def info_form():
    with st.form("personal_information"):
        st.header("Personal information")
        
        profile = st.session_state.profile
        
        name = st.text_input("Name", value=profile["general"]["name"])
        age = st.number_input("Age", min_value=1, max_value=120, step=1, value=profile["general"]["age"])
        
        genders = ["Male", "Female", "Other"]
        gender = st.radio("Gender", genders, index=genders.index(profile["general"].get("gender", "Female")))
        
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, step=0.1, value=float(profile["general"]["weight"]))
        height = st.number_input("Height (cm)", min_value=20.0, max_value=250.0, step=0.1, value=float(profile["general"]["height"]))
    
        activities = (
            "Sedentary",
            "Lightly Active",
            "Moderately Active",
            "Very Active",
            "Extremely Active"
        )
        activity_level = st.selectbox("Activity level", activities, index=activities.index(profile["general"].get("activity_level", "Lightly Active")))
        
        personal_information_submit = st.form_submit_button("Save")
        if personal_information_submit:
            if all([name, age, weight, height, gender, activity_level]):
                with st.spinner():
                    st.session_state.profile = update_personal_info(
                                                    profile, 
                                                    "general", 
                                                    name=name, 
                                                    age=age, 
                                                    gender=gender, 
                                                    weight=weight, 
                                                    height=height, 
                                                    activity_level=activity_level
                                                )
                    st.success("Information saved.")
            else:
                st.warning("Please fill in all the data.")
                
                
@st.fragment()
def goals_form():
    profile = st.session_state.profile
    with st.form("goals_form"):
        st.header("Goals")
        goals = st.multiselect(
            "Select your goals", ["Muscle gain", "Fat loss", "Incrase Energy"],
            default=profile.get("goals", ["Muscle gain"])
        )
        if st.session_state.get("show_success_message", False):
                st.success("Goals updated!")
                st.session_state.show_success_message = False
        goals_submit = st.form_submit_button("Save")
        if goals_submit:
            if goals:
                with st.spinner():
                    st.session_state.profile = update_personal_info(profile, "goals", goals=goals)
                    st.session_state.show_success_message = True
                    st.rerun()
            else:
                st.warning("Please enter at least one goal.")
                
                

@st.fragment()
def nutrition_form():
    profile = st.session_state.profile
    nutrition = st.container(border=True)
    nutrition.header("Nutritional goals")
    
    if nutrition.button("Generate with AI"):
        result = get_goals(goals=profile.get("goals"), profile=profile.get("general")) 
        profile["nutrition"] = result 
        st.rerun() 
    
    
    with nutrition.form("nutrition_columns", border=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            calories= st.number_input("Calories", min_value=0, step=1, value=profile["nutrition"].get("calories", 0))
        with col2:
            protein= st.number_input("Protein", min_value=0, step=1, value=profile["nutrition"].get("protein", 0))
        with col3:
            carbs= st.number_input("Carbs", min_value=0, step=1, value=profile["nutrition"].get("carbs", 0))
        with col4:
            fat= st.number_input("Fat", min_value=0, step=1, value=profile["nutrition"].get("fat", 0))
            
        if st.form_submit_button("Save"):
            with st.spinner():
                st.session_state_profile = update_personal_info(profile, "nutrition", calories=calories, protein=protein, carbs=carbs, fat=fat)
                st.success("Information saved.")
            

@st.fragment()
def notes_form():
    st.header("Notes: ")
    for i, note in enumerate(st.session_state.notes):
        cols = st.columns([5, 1])
        with cols[0]:
            st.text(note.get("text"))
        with cols[1]:
            if st.button("Delete", key=i):
                delete_note(note.get("_id"))
                st.session_state.notes.pop(i)
                st.rerun()
            
    new_note = st.text_input("Add a new note: ")
    if st.button("Add Note"):
        if new_note:
            note = add_note(new_note, st.session_state.profile_id)
            st.session_state.notes.append(note)
            st.rerun()


@st.fragment()
def advice_form():
    st.subheader("Nutritionist")
    user_question = st.text_input("Ask our AI nutritionist a question: ")
    if st.button("Ask AI"):
        with st.spinner():
            result = get_nutrition(question=user_question, profile=st.session_state.profile)
            st.write(result)
            
            
def app():
    if "profile" not in st.session_state:
        profile_id = 1
        profile = get_profile(profile_id)
        if not profile:
            profile_id, profile = create_profile(profile_id)
            
        st.session_state.profile = profile
        st.session_state.profile_id = profile_id
        
    if "notes" not in st.session_state:
        st.session_state.notes = get_notes(st.session_state.profile_id)
    info_form()
    goals_form()
    nutrition_form()
    notes_form()
    advice_form()
    
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)


    
if __name__ == "__main__":
    app()
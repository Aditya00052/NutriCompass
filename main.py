import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64


# Initializing a variable to store the api key
GOOGLE_API_KEY = "YOUR_SECRET_KEY"

# Configuring the Google Generative AI library
genai.configure(api_key=GOOGLE_API_KEY)

# Initializing our streamlit app
st.set_page_config(page_title='NutriCompass')  # must be the first streamlit command

# Custom CSS to adjust the header alignment
st.markdown(
    """
    <style>
    .body{
        margin-left: 280px;
    }

    .header {
        display: flex;
        justify-content: center;   /* Center alignment */
        font-size: 2.5em;
        color: #FFF100;            /* Optional: Change color */
    }

    .desc{
        display: flex;
        color: #FFDC7F;
        font-size: 23px;
        letter-spacing: 1px;
        margin-bottom: 50px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Adding header
st.markdown("<h1 class='header body'>NutriCompass</h1>", unsafe_allow_html=True)

# Adding description
st.markdown(
    "<div class='desc body'>Welcome to NutriCompass! This app analyzes the nutritional value of your food.</div>",
    unsafe_allow_html=True
)


# Function to fetch response from gemini wrt a particular prompt and image
def get_gemini_response(input_prompt, image):

    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([input_prompt, image])
    response = response.text

    return response


# Processes the uplpaded file to generate image data
def input_image_processing(uploaded_file):

    # Check if file is uploaded or not
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image = [
            {
                'mime_type': uploaded_file.type,
                'data': bytes_data,
            }
        ]

        return image

    else:
        raise FileNotFoundError('No file uploaded')


# Setting background

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(img):
    with open(img, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(img_path):
    bin_str = get_base64_of_bin_file(img_path)
    page_bg_img = f'''
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{bin_str}");
            background-size: cover;
        }}
        </style>
        '''

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


set_background(img_path='./images/bg_13.jpg')

# Uploading Image
#     Creating a layout with columns to add left margin
left_space, main_content = st.columns([3, 5])

with main_content:
    # Upload image widget
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

    # Display uploaded image if any
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded image', use_column_width=True)

    # Submit button
    submit = st.button('Examine the nutritional value of the meal')

input_prompt = """
        You are an expert in nutritionist where you need to see the food items from the image
        and calculate the total calories, also provide the details of every food items with calories intake
        is below format

           1. Item 1 - no of calories
           2. Item 2 - no of calories
           ----
           ----

        I cannot provide you with amounts of which food i've taken so just give me result based on an approximation.
        Finally You can mention the positive and negative effects of the food in the following format,

        Positive Effects: 
            1. Energy rich food
            2.
            ----

        Negative Effects:
            1. High in cholestrol
            2.
            ----


        Also, provide the percentage proportion of different nutrients in the following format, 
with each value on a new line:

               1. total fat - percentage
               2. saturated fat - percentage
               3. Trans Fat
               4. cholesterol
               5. sodium
               6. total carbohydrate
               7. dietary fiber
               8. total sugars
               9. added sugars
               10. Protien 
               11. Certain Vitamins
               12. Minerals
"""

if submit:
    image = Image.open(uploaded_file)
    response = get_gemini_response(input_prompt, image)

    with main_content:
        st.header('The response is:')
        st.write(response)

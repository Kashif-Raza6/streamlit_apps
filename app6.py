import streamlit as st
import requests
import openai




# Set the API key and model
api_key = "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"
openai.api_key = api_key

# add banner
# Add the banner image to the sidebar
st.sidebar.image("banner.PNG", width=200)

# Add the banner image to the main area of the app
# st.image("banner.PNG", width=200)


# Title and description of the app make color of text BLUE
st.title("Image Creation from Text prompt")

# New way of changing color of title
# new_title = '<p style="font-family:sans-serif; color:Blue; font-size: 50px;">IMAGE CREATION FROM TEXT PROMPT</p>'
# st.markdown(new_title, unsafe_allow_html=True)

st.markdown("This app generates images based on a text description. Enter a text description in the input field and click the 'Generate Image' button to see the generated images. You can select the model to use from the dropdown menu in the sidebar.")

# Sidebar with model selection and number of images to generate
model_selection = st.sidebar.selectbox("Select the model to use:", ["image-alpha-001"])
num_images = st.sidebar.slider("Number of images to generate:", min_value=1, max_value=10, value=1)
# Quality selection
quality_selection = st.sidebar.radio("Select the quality of the image:", ("Low", "Medium", "High"))
# Quality selection
sizes = {
    "Low": "256x256",
    "Medium": "512x512",
    "High": "1024x1024"
}

size = sizes[quality_selection]



# Text input
text_input = st.text_input("Enter the text for the image:")

# Button to generate images
button = st.button("Generate Images")

# Display loading spinner while API request is being processed
with st.spinner("Generating images..."):
  # Send the request to the API and get the image URLs
  @st.cache
  def generate_images():
    prompt = f"Image description: {text_input} \nImage URL:"
    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "model": model_selection,
            "prompt": prompt,
            "num_images": num_images,
            "size": size,
            "response_format": "url"
        }
    )
    image_urls = [image['url'] for image in response.json()['data']]
    return image_urls

# Display the images
if button:
  try:
    image_urls = generate_images()
    st.markdown("Here are the generated images:")
    for url in image_urls:
      st.image(url)
  except:
    st.error("There was an error generating the images. Make sure you have entered a valid text description and selected a valid model.")

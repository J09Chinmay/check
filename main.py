import os
import streamlit as st
import json
from groq import Groq
from email_service import send_email  # Import the email service
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client with your API key
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


# Initialize Groq client with your API key
# client = Groq(api_key="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")

# Set page configuration
st.set_page_config(page_title="Place Info with Groq", page_icon="🗺️")

# Hide the Streamlit header and footer
st.markdown("""
    <style>
    /* Hide header and footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Title and Description
st.title("Get Information About Any Place 🗺️")
st.write("Enter the name of a place to get interesting details about it.")

# User Input
place_name = st.text_input("Enter Place Name")

# Function to get details from Groq with different questions
def get_place_details(place):
    # Define questions for different aspects
    questions = {
        "historical_facts": f"Tell me about the historical significance of {place}.",
        "attractions": f"What are the main attractions in {place}?",
        "famous_places": f"Which famous places should I not miss in {place}?",
        "unique_information": f"Share some unique information about {place}."
    }
    # Dictionary to hold the results
    place_info = {"place": place}

    # Loop through questions and store responses
    for field, question in questions.items():
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": question}],
            model="llama3-8b-8192"
        )
        place_info[field] = response.choices[0].message.content if response.choices else "No details found."

    return place_info

# Button to submit the place name
if st.button("Get Details"):
    if place_name:
        with st.spinner("Fetching details..."):
            try:
                # Get detailed info and store it in JSON format
                details = get_place_details(place_name)
                st.success("Here are the details:")
                
                # Display simple text details for user
                # st.write(f"**Historical Facts**: {details['historical_facts']}")
                # st.write(f"**Attractions**: {details['attractions']}")
                # st.write(f"**Famous Places**: {details['famous_places']}")
                # st.write(f"**Unique Information**: {details['unique_information']}")
                # Display details with styled headers for the user
                st.markdown(f"<span style='font-weight:bold; color:orange;'>Historical Facts</span>: {details['historical_facts']}", unsafe_allow_html=True)
                st.markdown(f"<span style='font-weight:bold; color:orange;'>Attractions</span>: {details['attractions']}", unsafe_allow_html=True)
                st.markdown(f"<span style='font-weight:bold; color:orange;'>Famous Places</span>: {details['famous_places']}", unsafe_allow_html=True)
                st.markdown(f"<span style='font-weight:bold; color:orange;'>Unique Information</span>: {details['unique_information']}", unsafe_allow_html=True)
                # Convert details to JSON in memory (no file saved)
                json_data = json.dumps(details)

                # HTML content for the email
                html_content = f"""
                <html>
                    <head>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                                background-color: #f4f4f4;
                                color: #333;
                            }}
                            .container {{
                                width: 90%;
                                margin: 0 auto;
                                background-color: #ffffff;
                                padding: 20px;
                                border-radius: 8px;
                                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            }}
                            .header {{
                                text-align: center;
                                padding: 10px 0;
                                color: #4CAF50;
                            }}
                            .place-details {{
                                width: 100%;
                                margin-top: 20px;
                                border-collapse: collapse;
                            }}
                            .place-details th {{
                                background-color: #4CAF50;
                                color: white;
                                padding: 12px;
                                text-align: left;
                                border: 1px solid #ddd;
                            }}
                            .place-details td {{
                                padding: 12px;
                                border: 1px solid #ddd;
                                color: #555;
                            }}
                            .footer {{
                                text-align: center;
                                margin-top: 20px;
                                color: #888;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h2 class="header">Place Information Request</h2>
                            <p>Here is the information you requested for <strong>{place_name}</strong>:</p>
                            <table class="place-details">
                                <tr><th>Field</th><th>Information</th></tr>
                                <tr><td><strong>Historical Facts</strong></td><td>{details["historical_facts"]}</td></tr>
                                <tr><td><strong>Attractions</strong></td><td>{details["attractions"]}</td></tr>
                                <tr><td><strong>Famous Places</strong></td><td>{details["famous_places"]}</td></tr>
                                <tr><td><strong>Unique Information</strong></td><td>{details["unique_information"]}</td></tr>
                            </table>
                            <div class="footer"><p>Thank you for using our service!</p><p>Made with ❤️ using Streamlit and Groq</p></div>
                        </div>
                    </body>
                </html>
                """
                
                subject = f"Place Info Request: {place_name}"
                
                # Send email with the HTML content (detailed formatting)
                send_email(subject, html_content)

                # Provide download link for JSON data without saving to file
                st.download_button("Download Details as JSON", data=json_data, file_name=f"{place_name}_details.json", mime="application/json")
                
            except Exception as e:
                st.error(f"Error fetching details: {e}")
    else:
        st.warning("Please enter a place name.")

# Footer
st.markdown("---")
st.write("Made with ❤️ using Streamlit and Groq")

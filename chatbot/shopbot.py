import os
from openai import OpenAI
from IPython.display import display
import ipywidgets as widgets
import time
import pandas as pd

MY_OPENAI_KEY = 'your_api_key'

# Create a Chatbot
def get_completion_from_messages(messages, model="gpt-3.5-turbo"):
  
    client = OpenAI(
        api_key=MY_OPENAI_KEY,
    )

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )
    return chat_completion.choices[0].message.content

# Interacting with Customers
def collect_messages(_):
    user_input = inp.value
    inp.value = ''
    context.append({'role':'user', 'content':f"{user_input}"})

    # Record the start time
    start_time = time.time()  

    response = get_completion_from_messages(context) 

    # Record the end time
    end_time = time.time()  

    # Calculate the duration
    duration = end_time - start_time  

    context.append({'role': 'assistant', 'content': f"{response}"})

    user_pane = widgets.Output()
    with user_pane:
        display(widgets.HTML(f"<b>User:</b> {user_input}"))

    assistant_pane = widgets.Output()
    with assistant_pane:
        display(widgets.HTML(f"<b>Assistant:</b> {response}"))

    display(widgets.VBox([user_pane, assistant_pane]))

    # Check if the user asked for a table summary of the previous order
    if "table summary of the previous order" in user_input.lower():
        # Generate and display the table summary
        display_previous_order_summary()

def display_previous_order_summary():

    previous_order_data = [
        {"Product Name": "T-shirt", "Price": 20, "Quantity": 2},
        {"Product Name": "Stylish Sunglasses", "Price": 20, "Quantity": 1},
        {"Product Name": "Leather Handbag", "Price": 60, "Quantity": 1}
    ]

    previous_order_df = pd.DataFrame(previous_order_data)

    previous_order_df["Total Cost"] = previous_order_df["Price"] * previous_order_df["Quantity"]

    order_summary = previous_order_df[["Product Name", "Price", "Quantity", "Total Cost"]]

    order_summary_str = order_summary.to_string(index=False)

    print("\nTable Summary of the Previous Order:\n")
    print(order_summary_str)

inp = widgets.Text(value="Hi", placeholder='Enter text here…')
button_conversation = widgets.Button(description="Chat!")
button_conversation.on_click(collect_messages)
dashboard = widgets.VBox([inp, button_conversation])
display(dashboard)

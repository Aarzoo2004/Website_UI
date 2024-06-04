import pandas as pd
from static.functions import common_functions
from datetime import datetime
import json



def replace_nan_with_word(data, word="nan"):
    if isinstance(data, dict):
        return {k: replace_nan_with_word(v, word) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_nan_with_word(item, word) for item in data]
    elif pd.isna(data):
        return word
    else:
        return data


def receive_items_table_data_function(name, session_data):
    # Load the data from the Excel file into a pandas DataFrame
    df = pd.read_excel('Excel/handover_data.xlsx')

    # Filter the DataFrame based on the parameters
    filtered_data = df[(df['Receiver'] == name) & 
                       (df['ApprovalToSend'] == "YES") & 
                       (df['ApprovalToReceive'] != "YES") & 
                       (df['CompletionDate'].isnull())]

    # Sort the filtered data by 'InitiationDate' column in descending order
    filtered_data = filtered_data.sort_values(by='InitiationDate', ascending=False)

    # Convert the filtered DataFrame to a dictionary
    filtered_data_dict = filtered_data.to_dict(orient='records')

    # Replace all NaN values in the dictionary with the word 'nan'
    filtered_data_dict = replace_nan_with_word(filtered_data_dict)

    # Append the session_data dictionary
    combined_data = {
        "filtered_data": filtered_data_dict,
        "session_data": session_data
    }

    # Convert the combined data to a JSON object
    json_result = json.dumps(combined_data)

    # Return the JSON object
    return json_result








def receive_approval_request_function(form_data):
    print('This is the form data we received in the receive_approval_request_function function:', form_data)
    
    # Read the Excel file
    excel_data = pd.read_excel('Excel/handover_data.xlsx')
    
    # Extract FormID from the first dictionary
    form_no = form_data[0]['FormID']
    print('This is the form id:', form_no)
    
    # Get the current date and time
    current_datetime = datetime.now()
    
    # Iterate through the form data (excluding the first dictionary)
    for form_item in form_data[1:]:
        serial_no = form_item['SerialNo']
        receiver_condition = form_item['ReceiverCondition']
        receiver_remark = form_item['ReceiverRemark']
        reached = form_item['Reached']
        print('This is the product details serial no:', serial_no)
        
        # Check if FormID and SerialNo match in the Excel data
        match_row = excel_data[(excel_data.iloc[:, 0] == form_no) & (excel_data.iloc[:, 6] == serial_no)]
        print('This is the matched row found:', match_row)
        
        if not match_row.empty:
            # Update the corresponding columns
            match_row_index = match_row.index[0]  # Assuming there's only one match
            excel_data.iloc[match_row_index, 13] = reached
            excel_data.iloc[match_row_index, 14] = receiver_condition
            excel_data.iloc[match_row_index, 15] = receiver_remark
            excel_data.iloc[match_row_index, 19] = current_datetime  # Assuming the 19th column is index 18
        else:
            print(f"No matching entry found for FormID: {form_no} and SerialNo: {serial_no}")
    
    # Update the Excel file
    excel_data.to_excel('Excel/handover_data.xlsx', index=False)
    
    return 'Data processed successfully'




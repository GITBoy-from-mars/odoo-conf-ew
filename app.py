
# import os
# import uuid
# from flask import Flask, request, send_from_directory, render_template_string, url_for
# import pandas as pd

# app = Flask(__name__)

# # Ensure the 'downloads' folder exists
# DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
# os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# # HTML template for the upload form (with spinner)
# UPLOAD_TEMPLATE = '''
# <!doctype html>
# <html>
#   <head>
#     <meta charset="utf-8">
#     <title>SPSS Numeric Converter</title>
#     <style>
#       body {
#         font-family: Arial, sans-serif;
#         background: #f5f5f5;
#         padding: 20px;
#       }
#       .container {
#         max-width: 500px;
#         margin: 0 auto;
#         background: #fff;
#         padding: 30px;
#         border-radius: 8px;
#         box-shadow: 0 2px 5px rgba(0,0,0,0.1);
#       }
#       h2 {
#         text-align: center;
#         color: #333;
#       }
#       form {
#         display: flex;
#         flex-direction: column;
#       }
#       label {
#         margin-top: 10px;
#       }
#       input[type="file"],
#       input[type="text"] {
#         margin: 10px 0;
#         padding: 8px;
#         border: 1px solid #ccc;
#         border-radius: 4px;
#       }
#       button {
#         padding: 10px;
#         background: #28a745;
#         color: #fff;
#         border: none;
#         border-radius: 4px;
#         cursor: pointer;
#         font-size: 16px;
#         margin-top: 10px;
#       }
#       button:hover {
#         background: #218838;
#       }
#       /* Spinner styles */
#       .spinner-overlay {
#         display: none;
#         position: fixed;
#         z-index: 999;
#         top: 0;
#         left: 0;
#         width: 100%;
#         height: 100%;
#         background: rgba(255, 255, 255, 0.8);
#       }
#       .spinner {
#         position: absolute;
#         top: 50%;
#         left: 50%;
#         margin: -25px 0 0 -25px;
#         width: 50px;
#         height: 50px;
#         border: 5px solid #ccc;
#         border-top: 5px solid #28a745;
#         border-radius: 50%;
#         animation: spin 1s linear infinite;
#       }
#       @keyframes spin {
#         0% { transform: rotate(0deg); }
#         100% { transform: rotate(360deg); }
#       }
#     </style>
#     <script>
#       // Show spinner when form is submitted
#       function showSpinner() {
#         document.getElementById('spinner-overlay').style.display = 'block';
#       }
#     </script>
#   </head>
#   <body>
#     <div class="container">
#       <h2>SPSS Numeric Converter</h2>
#       <form method="post" enctype="multipart/form-data" onsubmit="showSpinner()">
#         <label for="file">Upload Excel File (.xlsx):</label>
#         <input type="file" name="file" id="file" accept=".xlsx" required>
#         <label for="sheet">Sheet name (e.g., Sheet1):</label>
#         <input type="text" name="sheet" id="sheet" placeholder="Sheet name" required>
#         <button type="submit">Convert</button>
#       </form>
#     </div>
#     <!-- Spinner overlay -->
#     <div id="spinner-overlay" class="spinner-overlay">
#       <div class="spinner"></div>
#     </div>
#   </body>
# </html>
# '''

# # HTML template for the success dialog after processing
# SUCCESS_TEMPLATE = '''
# <!doctype html>
# <html>
#   <head>
#     <meta charset="utf-8">
#     <title>Task Completed</title>
#     <style>
#       body {
#         font-family: Arial, sans-serif;
#         background: #e9f5ff;
#         padding: 20px;
#         text-align: center;
#       }
#       .dialog {
#         max-width: 500px;
#         margin: 50px auto;
#         background: #fff;
#         padding: 30px;
#         border-radius: 8px;
#         box-shadow: 0 2px 5px rgba(0,0,0,0.1);
#       }
#       h2 {
#         color: #333;
#       }
#       a.button {
#         display: inline-block;
#         margin-top: 20px;
#         padding: 10px 20px;
#         background: #007bff;
#         color: #fff;
#         text-decoration: none;
#         border-radius: 4px;
#       }
#       a.button:hover {
#         background: #0056b3;
#       }
#     </style>
#   </head>
#   <body>
#     <div class="dialog">
#       <h2>Your task is completed!</h2>
#       <p>Click the link below to download your converted file.</p>
#       <a class="button" href="{{ download_url }}">Download File</a>
#       <br><br>
#       <p>Or, explore our services:</p>
#       <a class="button" href="https://www.yourwebsite.com" target="_blank">Visit Our Website</a>
#     </div>
#   </body>
# </html>
# '''

# def convert_to_numeric_codes(df):
#     # Create a dictionary to hold mappings for each column
#     mappings = {}
#     for column in df.columns:
#         # Get unique values in the column, sorted alphabetically
#         unique_values = sorted(df[column].dropna().unique())
#         # Create a dictionary mapping each unique value to an incrementing number
#         value_to_code = {value: idx + 1 for idx, value in enumerate(unique_values)}
#         mappings[column] = value_to_code  # Store the mapping
#         # Replace column values with their corresponding numeric codes
#         df[column] = df[column].map(value_to_code)
#     return df, mappings

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # Retrieve file and sheet name
#         file = request.files['file']
#         sheet_name = request.form['sheet']
        
#         # Read the Excel file
#         df = pd.read_excel(file, sheet_name=sheet_name)
#         df_converted, mappings = convert_to_numeric_codes(df.copy())

#         # Prepare the mappings DataFrame for notation
#         mappings_list = []
#         for column in df.columns:
#             for original_value, code in mappings[column].items():
#                 mappings_list.append({'Questions': column, 'Options': original_value, 'Numeric Code': code})
#         mappings_df = pd.DataFrame(mappings_list)
#         mappings_df['Questions'] = pd.Categorical(mappings_df['Questions'], categories=df.columns, ordered=True)
#         mappings_df = mappings_df.sort_values('Questions').reset_index(drop=True)
#         mappings_df = mappings_df.pivot(index='Questions', columns='Numeric Code', values='Options').reset_index()
#         mappings_df.columns.name = None

#         # Create a unique filename and save the output Excel file in the downloads folder
#         filename = f"spss_converted_{uuid.uuid4().hex}.xlsx"
#         output_path = os.path.join(DOWNLOAD_FOLDER, filename)
#         with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
#             df_converted.to_excel(writer, sheet_name='Converted Data', index=False)
#             mappings_df.to_excel(writer, sheet_name='Notation', index=False)
        
#         # Generate download URL for the saved file
#         download_url = url_for('download_file', filename=filename)
        
#         # Render a success dialog page with a download link and explore services button
#         return render_template_string(SUCCESS_TEMPLATE, download_url=download_url)
    
#     # For GET requests, render the upload page.
#     return render_template_string(UPLOAD_TEMPLATE)

# @app.route('/download/<filename>')
# def download_file(filename):
#     # Serve the file from the downloads folder
#     return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)






import os
import uuid
from flask import Flask, request, send_from_directory, render_template_string, url_for
import pandas as pd

app = Flask(__name__)

# Ensure the 'downloads' folder exists
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# HTML template for the upload page with spinner
UPLOAD_TEMPLATE = '''
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>SPSS Numeric Converter Online</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        background: #f5f5f5;
        padding: 20px;
      }
      .container {
        max-width: 500px;
        margin: 0 auto;
        background: #fff;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      }
      h2 {
        text-align: center;
        color: #333;
      }
      form {
        display: flex;
        flex-direction: column;
      }
      label {
        margin-top: 10px;
      }
      input[type="file"],
      input[type="text"] {
        margin: 10px 0;
        padding: 8px;
        border: 1px solid #ccc;
        border-radius: 4px;
      }
      button {
        padding: 10px;
        background: #28a745;
        color: #fff;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
        margin-top: 10px;
      }
      button:hover {
        background: #218838;
      }
      /* Spinner styles */
      .spinner-overlay {
        display: none;
        position: fixed;
        z-index: 999;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.8);
      }
      .spinner {
        position: absolute;
        top: 50%;
        left: 50%;
        margin: -25px 0 0 -25px;
        width: 50px;
        height: 50px;
        border: 5px solid #ccc;
        border-top: 5px solid #28a745;
        border-radius: 50%;
        animation: spin 1s linear infinite;
      }
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    </style>
    <script>
      // Show spinner when form is submitted
      function showSpinner() {
        document.getElementById('spinner-overlay').style.display = 'block';
      }
    </script>
  </head>
  <body>
    <div class="container">
      <h2>SPSS Numeric Converter</h2>
      <form method="post" enctype="multipart/form-data" onsubmit="showSpinner()">
        <label for="file">Upload Excel File with string Value (.xlsx):</label>
        <input type="file" name="file" id="file" accept=".xlsx" required>
        <label for="sheet">Sheet name (e.g., Sheet1):</label>
        <input type="text" name="sheet" id="sheet" placeholder="Sheet name" required>
        <button type="submit">Convert</button>
      </form>
    </div>
    <!-- Spinner overlay -->
    <div id="spinner-overlay" class="spinner-overlay">
      <div class="spinner"></div>
    </div>
  </body>
</html>
'''

# HTML template for the success page with download button and redirect
SUCCESS_TEMPLATE = '''
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Your Task is Completed</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        background: #e9f5ff;
        padding: 20px;
        text-align: center;
      }
      .dialog {
        max-width: 500px;
        margin: 50px auto;
        background: #fff;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
      }
      h2 {
        color: #333;
      }
      a.button {
        display: inline-block;
        margin-top: 20px;
        padding: 10px 20px;
        background: #007bff;
        color: #fff;
        text-decoration: none;
        border-radius: 4px;
      }
      a.button:hover {
        background: #0056b3;
      }
    </style>
    <script>
      // This function triggers file download and then redirects after a short delay.
      function downloadAndRedirect(e) {
        e.preventDefault();
        var downloadUrl = e.currentTarget.href;
        // Create a hidden link and click it to initiate the download.
        var a = document.createElement('a');
        a.href = downloadUrl;
        a.download = '';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        // Redirect after a delay (e.g., 2 seconds)
        setTimeout(function() {
          window.location.href = "https://www.simbi.in";
        }, 2000);
      }
    </script>
  </head>
  <body>
    <div class="dialog">
      <h2>Your task is completed!</h2>
      <p>Click the button below to download your converted file.</p>
      <a class="button" href="{{ download_url }}" onclick="downloadAndRedirect(event)">Download File</a>
    </div>
  </body>
</html>
'''

def convert_to_numeric_codes(df):
    # Create a dictionary to hold mappings for each column
    mappings = {}
    for column in df.columns:
        unique_values = sorted(df[column].dropna().unique())
        value_to_code = {value: idx + 1 for idx, value in enumerate(unique_values)}
        mappings[column] = value_to_code
        df[column] = df[column].map(value_to_code)
    return df, mappings

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        sheet_name = request.form['sheet']
        
        df = pd.read_excel(file, sheet_name=sheet_name)
        df_converted, mappings = convert_to_numeric_codes(df.copy())

        mappings_list = []
        for column in df.columns:
            for original_value, code in mappings[column].items():
                mappings_list.append({'Questions': column, 'Options': original_value, 'Numeric Code': code})
        mappings_df = pd.DataFrame(mappings_list)
        mappings_df['Questions'] = pd.Categorical(mappings_df['Questions'], categories=df.columns, ordered=True)
        mappings_df = mappings_df.sort_values('Questions').reset_index(drop=True)
        mappings_df = mappings_df.pivot(index='Questions', columns='Numeric Code', values='Options').reset_index()
        mappings_df.columns.name = None

        # Save output file with a unique filename in the downloads folder
        filename = f"spss_converted_{uuid.uuid4().hex}.xlsx"
        output_path = os.path.join(DOWNLOAD_FOLDER, filename)
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df_converted.to_excel(writer, sheet_name='Converted Data', index=False)
            mappings_df.to_excel(writer, sheet_name='Notation', index=False)
        
        download_url = url_for('download_file', filename=filename)
        return render_template_string(SUCCESS_TEMPLATE, download_url=download_url)
    
    return render_template_string(UPLOAD_TEMPLATE)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)


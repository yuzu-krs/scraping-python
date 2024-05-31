import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import os

# Function to handle the URL retrieval and code extraction
def retrieve_code():
    url = url_entry.get()
    
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            code_blocks = soup.find_all('pre', {'class': 'sourceCode c'})
            
            if code_blocks:
                program_count = 0
                
                # Create a directory to store the files if it doesn't exist
                directory = 'extracted_code'
                if not os.path.exists(directory):
                    os.makedirs(directory)
                
                for i, code_block in enumerate(code_blocks):
                    code_text = code_block.get_text().strip()
                    with open(f'{directory}/program_{i + 1}.c', 'w', encoding='utf-8') as file:
                        file.write(code_text)
                    program_count += 1
                
                messagebox.showinfo("Success", f"{program_count} programs saved to individual files.")
            else:
                messagebox.showwarning("Warning", "No code blocks found on the webpage.")
        else:
            messagebox.showerror("Error", f"Failed to retrieve the webpage. Status code: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI setup
root = tk.Tk()
root.title("スクレイピング")

url_label = tk.Label(root, text="コードをダウンロードしたいサイトのURLを入力")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

extract_button = tk.Button(root, text="ダウンロード", command=retrieve_code)
extract_button.pack()

root.mainloop()
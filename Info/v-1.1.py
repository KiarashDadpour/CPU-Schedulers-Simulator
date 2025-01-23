import customtkinter as ctk
import tkinter as tk


def display_html_like_content(text_widget, content):
    # Split content into lines
    lines = content.strip().split("\n")

    for line in lines:
        if line.strip() == "":
            # Add a newline for empty lines (e.g., between paragraphs)
            text_widget.insert("end", "\n")
            continue

        # Parse HTML-like tags
        while "<" in line and ">" in line:
            start_tag = line.find("<")
            end_tag = line.find(">")
            tag = line[start_tag + 1:end_tag]
            line = line[:start_tag] + line[end_tag + 1:]

            # Handle closing tags
            if tag.startswith("/"):
                tag = tag[1:]
                text_widget.tag_remove(tag, "end-1c linestart", "end-1c lineend")
            else:
                # Handle opening tags
                if tag == "strong":
                    text_widget.tag_configure(tag, font=("Arial", 12, "bold"))
                elif tag == "em":
                    text_widget.tag_configure(tag, font=("Arial", 12, "italic"))
                elif tag == "p":
                    # Paragraph: Add a newline before and after
                    text_widget.insert("end", "\n")
                    continue

                # Apply the tag to the next inserted text
                text_widget.insert("end", line[:line.find("<")], tag)
                line = line[line.find("<"):]

        # Insert remaining text without tags
        text_widget.insert("end", line + "\n")


# Set the appearance mode and color theme for CustomTkinter
ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

# Create the CustomTkinter window
root = ctk.CTk()
root.title("HTML-like Content in CustomTkinter")
root.geometry("600x400")

# Create a regular Tkinter Text widget inside the CustomTkinter window
text_widget = tk.Text(root, wrap="word", font=("Arial", 12), padx=10, pady=10)
text_widget.pack(fill="both", expand=True, padx=10, pady=10)

# HTML-like content
html_content = """
<p>
   <strong>FCFS</strong> 
</p>
<p>
  First-Come, First-Served CPU scheduling algorithm is one of the simplest scheduling methods, where processes are executed in the exact order of their arrival. It operates on a <em>non-preemptive</em> basis, meaning once a process starts execution, it runs to completion before the next process begins. While it is straightforward to implement and fair in terms of arrival order, FCFS may lead to poor performance due to the <strong>convoy effect</strong>, where short processes are delayed by longer ones, resulting in high waiting and turnaround times for shorter tasks. This algorithm is best suited for batch systems with predictable workloads.
</p>
"""

# Display the HTML-like content in the Text widget
display_html_like_content(text_widget, html_content)

# Disable editing in the Text widget
text_widget.config(state="disabled")

# Run the CustomTkinter event loop
root.mainloop()

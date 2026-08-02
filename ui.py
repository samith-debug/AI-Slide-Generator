import tkinter as tk
import threading
import utils


# --------------------------------------------------------
# Run PPT generation in background (UI won't freeze)
# --------------------------------------------------------
def generate_ppt_and_show_result():
    thread = threading.Thread(target=run_generation)
    thread.start()


def run_generation():
    from generate_ppt import generate_ppt  # import here to avoid circular errors

    topic = topic_entry.get().strip()
    model = model_entry.get().strip()
    slides = slide_entry.get().strip()
    api_key = api_key_entry.get().strip()

    if not topic or not slides or not api_key:
        result_label.config(text="⚠️ Please fill all fields.")
        return

    try:
        result_label.config(text="⏳ Generating PPT... Please wait...")

        # api_name is always "groq"
        result = generate_ppt(
            topic,
            "groq",
            model,
            int(slides),
            api_key
        )

        result_label.config(text=result)

    except Exception as e:
        result_label.config(text=f"❌ Error: {e}")



config = utils.load_config()



window = tk.Tk()
window.title("PPTX Generator - Groq")
window.geometry("600x430")




tk.Label(window, text="Groq API Key").pack()
api_key_entry = tk.Entry(window, width=50)
api_key_entry.pack()
api_key_entry.insert(0, config.get("groq_key", ""))

tk.Label(window, text="Topic").pack()
topic_entry = tk.Entry(window, width=60)
topic_entry.pack()

tk.Label(window, text="Model").pack()
model_entry = tk.Entry(window, width=40)
model_entry.pack()
model_entry.insert(0, "llama-3.3-70b-versatile")

tk.Label(window, text="Number of Slides").pack()
slide_entry = tk.Entry(window, width=20)
slide_entry.pack()
slide_entry.insert(0, "10")  # default value




tk.Button(
    window,
    text="Generate PPT",
    command=generate_ppt_and_show_result
).pack(pady=15)



result_label = tk.Label(window, text="", wraplength=520, justify="left")
result_label.pack(pady=10)




window.mainloop()

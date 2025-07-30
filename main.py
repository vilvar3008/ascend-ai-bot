from flask import Flask, request
import cohere
import os

app = Flask(__name__)

# Setup Cohere API
api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key)

# Get response from Cohere
def ask_cohere(prompt):
    response = co.generate(
        model='command-r-plus',
        prompt=prompt,
        max_tokens=400,
        temperature=0.8
    )
    return response.generations[0].text.strip()

@app.route("/", methods=["GET", "POST"])
def home():
    html = """
    <h2>🎓 Ascend AI Bot</h2>
    <form method="post">
        <label>Your Interest:</label><br>
        <input name="interest" required><br><br>
        <input type="radio" name="mode" value="career" checked> Career Suggestions<br>
        <input type="radio" name="mode" value="scholarship"> Scholarship Finder<br><br>
        <button type="submit">Submit</button>
    </form>
    """

    if request.method == "POST":
        interest = request.form.get("interest")
        mode = request.form.get("mode")
        if mode == "career":
            prompt = f"Suggest 3 careers, required skills, courses, companies, and scholarships for: {interest}"
        else:
            prompt = f"List scholarships for: {interest} with eligibility and country"

        result = ask_cohere(prompt)
        html += f"<h3>✨ Result:</h3><pre>{result}</pre>"
        html += "<p style='color: green;'>✅ Thank you for using Ascend AI! Come back anytime.</p>"

    return html

app.run(host="0.0.0.0", port=3000)

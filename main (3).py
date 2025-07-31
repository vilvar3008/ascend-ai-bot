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
    <body style="background-color: white; font-family: Arial, sans-serif; padding: 40px; text-align: center;">
        <div style="max-width: 600px; margin: auto; background-color: #f2f2f2; padding: 30px; 
                    border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">

            <h2 style="color: #003366;">🎓 Ascend AI 🚀</h2>
            <p style="color: #333;">Discover careers and scholarships based on your interests</p>

            <form method="post">
                <label><b>Your Interest:</b></label><br>
                <input name="interest" placeholder="e.g. Data Science, Law" required 
                    style="padding: 8px; width: 90%; border: 1px solid #ccc; border-radius: 5px;"><br><br>

                <label><b>Choose Mode:</b></label><br>
                <input type="radio" name="mode" value="career" checked> Career Suggestions<br>
                <input type="radio" name="mode" value="scholarship"> Scholarship Finder<br><br>

                <button type="submit" 
                    style="background-color: #0066cc; color: white; padding: 10px 20px; 
                           border: none; border-radius: 5px; font-size: 16px;">🔍 Submit</button>
            </form>
    """

    if request.method == "POST":
        interest = request.form.get("interest")
        mode = request.form.get("mode")
        if mode == "career":
            prompt = f"Suggest 3 careers, required skills, courses, companies, and scholarships for: {interest}"
        else:
            prompt = f"List scholarships for: {interest} with eligibility and country including India and international scholarships"

        result = ask_cohere(prompt)

        html += f"""
            <div style="text-align: left; margin-top: 30px; background-color: #e6f2ff; 
                        padding: 20px; border-radius: 8px; border: 1px solid #99ccff;">
                <h3 style="color: #003366;">✨ Result:</h3>
                <pre>{result}</pre>
                <p style="color: #006600;"><b>🌟 Keep learning, keep growing — your future starts here with Ascend AI!</b></p>
            </div>
        """

    html += "</div></body>"
    return html

app.run(host="0.0.0.0", port=3000)

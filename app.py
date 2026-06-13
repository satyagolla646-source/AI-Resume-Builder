from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
import google.generativeai as genai
from textwrap import wrap
import os

app = Flask(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite")

resume_data = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():

    global resume_data

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    skills = request.form['skills']
    education = request.form['education']
    experience = request.form['experience']

    prompt = f"""
Create ONLY ONE professional resume summary.

Rules:
- Maximum 4 lines.
- Do not give multiple options.
- Do not explain your answer.
- Do not use headings.
- Do not use bullet points.
- Return only the final summary text.

Name: {name}
Skills: {skills}
Education: {education}
Experience: {experience}
"""

    response = model.generate_content(prompt)

    summary = response.text.strip()

    resume_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education,
        "experience": experience,
        "summary": summary
    }

    return render_template('resume.html', data=resume_data)

@app.route('/download')
def download():
    print(resume_data)

    pdf_file = "resume.pdf"

    c = canvas.Canvas(pdf_file)

    y = 800

    c.drawString(100,y,resume_data["name"])
    y -= 30

    c.drawString(100,y,"Email: " + resume_data["email"])
    y -= 30

    c.drawString(100,y,"Phone: " + resume_data["phone"])
    y -= 40

    c.drawString(100,y,"Professional Summary")
    y -= 20

    summary_lines = wrap(resume_data["summary"], width=70)

    for line in summary_lines:
        c.drawString(100,y,line)
        y -= 20

    y -= 20

    c.drawString(100,y,"Skills")
    y -= 20

    c.drawString(100,y,resume_data["skills"])
    y -= 40

    c.drawString(100,y,"Education")
    y -= 20

    c.drawString(100,y,resume_data["education"])
    y -= 40

    c.drawString(100,y,"Experience")
    y -= 20

    c.drawString(100,y,resume_data["experience"])

    c.save()

    return send_file(pdf_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, send_file, session
from flask_bootstrap import Bootstrap
import spacy
from collections import Counter
import random
from PyPDF2 import PdfReader
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session
Bootstrap(app)

# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

def generate_mcqs(text, num_questions=5):
    if text is None:
        return []

    # Process the text with spaCy
    doc = nlp(text)

    # Extract sentences from the text
    sentences = [sent.text for sent in doc.sents]

    # Ensure that the number of questions does not exceed the number of sentences
    num_questions = min(num_questions, len(sentences))

    # Randomly select sentences to form questions
    selected_sentences = random.sample(sentences, num_questions)

    # Initialize list to store generated MCQs
    mcqs = []

    # Generate MCQs for each selected sentence
    for sentence in selected_sentences:
        # Process the sentence with spaCy
        sent_doc = nlp(sentence)

        # Extract entities (nouns) from the sentence
        nouns = [token.text for token in sent_doc if token.pos_ == "NOUN"]

        # Ensure there are enough nouns to generate MCQs
        if len(nouns) < 3:
            continue

        # Count the occurrence of each noun
        noun_counts = Counter(nouns)

        # Select the most common noun as the subject of the question
        if noun_counts:
            subject = noun_counts.most_common(1)[0][0]

            # Generate the question stem
            question_stem = sentence.replace(subject, "______")

            # Generate answer choices
            answer_choices = [subject]

            # Add relevant words from the text (excluding the subject) as options
            relevant_options = list(set(nouns) - {subject})

            # Ensure we have 4 relevant options
            while len(relevant_options) < 3:
                relevant_options.append("[Relevant Word]")

            answer_choices.extend(relevant_options[:3])  # Add 3 relevant options
            random.shuffle(answer_choices)  # Shuffle answer choices

            correct_answer = chr(65 + answer_choices.index(subject))  # A, B, C, D
            mcqs.append((question_stem, answer_choices, correct_answer))

    return mcqs

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = ""

        # Check if URL is provided
        if 'url' in request.form and request.form['url']:
            url = request.form['url']
            text = process_url(url)
        
        # Check if manual text is provided
        elif 'manual_text' in request.form and request.form['manual_text']:
            text = request.form['manual_text']

        # Check if files were uploaded
        elif 'files[]' in request.files:
            files = request.files.getlist('files[]')
            for file in files:
                if file.filename.endswith('.pdf'):
                    # Process PDF file
                    text += process_pdf(file)
                elif file.filename.endswith('.txt'):
                    # Process text file
                    text += file.read().decode('utf-8')

        # Get the selected number of questions from the dropdown menu
        num_questions = int(request.form['num_questions'])

        mcqs = generate_mcqs(text, num_questions=num_questions)
        mcqs_with_index = [(i + 1, mcq) for i, mcq in enumerate(mcqs)]

        # Store the generated MCQs in the session
        session['mcqs'] = mcqs_with_index

        return render_template('mcqs.html', mcqs=mcqs_with_index)

    return render_template('index.html')

def process_pdf(file):
    text = ""
    pdf_reader = PdfReader(file)
    for page_num in range(len(pdf_reader.pages)):
        page_text = pdf_reader.pages[page_num].extract_text()
        text += page_text
    return text

def process_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract only relevant text (you might need to customize this based on the structure of the website)
        for script in soup(['script', 'style', 'header', 'footer', 'nav']):
            script.decompose()  # Remove these elements

        return soup.get_text(separator='\n')  # Return text with new lines
    except Exception as e:
        print(f"Error processing URL: {e}")
        return ""

def draw_multiline_text(pdf, text, x, y, max_width):
    """
    Draw text on the PDF canvas, wrapping it if it exceeds max_width.
    """
    lines = []
    words = text.split(" ")
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if pdf.stringWidth(test_line, "Helvetica", 12) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    # Append any remaining text
    if current_line:
        lines.append(current_line)

    for line in lines:
        pdf.drawString(x, y, line)
        y -= 14  # Move down for the next line

    return y

@app.route('/download_pdf')
def download_pdf():
    mcqs = session.get('mcqs', [])
    if not mcqs:
        return "No MCQs to download.", 400  # Handle no MCQs case

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    pdf.setFont("Helvetica", 12)

    y_position = height - 40
    margin = 30
    max_width = width - 2 * margin

    for index, mcq in mcqs:
        question, choices, correct_answer = mcq
        
        # Draw the question with word wrapping
        y_position = draw_multiline_text(pdf, f"Q{index}: {question}?", margin, y_position, max_width)

        # Draw answer choices
        options = ['A', 'B', 'C', 'D']
        for i, choice in enumerate(choices):
            y_position = draw_multiline_text(pdf, f"{options[i]}: {choice}", margin + 20, y_position, max_width)

        pdf.drawString(margin + 20, y_position, f"Correct Answer: {correct_answer}")
        y_position -= 20

        if y_position < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y_position = height - 40

    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name='mcqs.pdf', mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)

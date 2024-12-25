# NLP-Based MCQ Generator

This project is an **NLP-based Multiple Choice Question (MCQ) Generator** that enables users to create MCQs from input data. The system leverages **spaCy** for Natural Language Processing and offers multiple options for data input. Users can customize the number of questions, verify their answers, and download the generated MCQs as a PDF.

---

## Features

1. **Input Options**:
   - **Provide URL Link**: Extract content from a web link.
   - **Manual Input**: Input custom text directly.
   - **Upload Files**: Upload PDF or TXT files to extract content.

2. **Question Customization**:
   - Specify the number of questions to generate.
   - Automatically generate MCQs based on the text provided.

3. **Answer Validation**:
   - Choose the correct option from four answer choices.
   - Verify the correctness of the selected answer.

4. **Export Options**:
   - Download the generated MCQs as a PDF file.

5. **Use Cases**:
   - Ideal for creating quizzes and tests for schools, colleges, or online learning platforms.

---

## Technologies Used

- **Python**: Core programming language.
- **Flask**: For creating the web application.
- **spaCy**: For Natural Language Processing (NLP).
- **Bootstrap**: For responsive and user-friendly web design.
- **PyPDF2**: For processing PDF files.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/nlp-mcq-generator.git
   cd nlp-mcq-generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the English spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. Run the application:
   ```bash
   python app.py
   ```



---

## Usage Instructions

1. Launch the application in your browser.
2. Select one of the input options:
   - **Provide URL Link**: (To be implemented if applicable)
   - **Manual Input**: Type or paste the text in the input field.
   - **Upload Files**: Upload PDF or TXT files.
3. Specify the number of MCQs to generate from the dropdown menu.
4. Review the generated questions and options.
5. Choose the correct answers and click **Show Results** to verify them.
6. Download the MCQs as a PDF for further use.

---

## File Structure

```plaintext
├── app.py               # Main application file
├── templates/
│   ├── index.html       # Homepage template
│   ├── mcqs.html        # MCQ display template
│   ├── style.css            # CSS files for styling
│   ├── results.html           
└── README.md            # Project documentation
```

---

## Example Screenshots

### Input Page
![image](https://github.com/user-attachments/assets/4f9c312f-860e-4010-a561-4856aa409739)


### Generated MCQs

![image](https://github.com/user-attachments/assets/6f484774-d4f1-434f-b4e4-b94eb8beaa7f)

---

## Future Enhancements

- Add support for extracting text directly from URLs.
- Improve distractor generation for more challenging options.
- Enhance the NLP pipeline for better context-aware question formation.

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request for review.

---



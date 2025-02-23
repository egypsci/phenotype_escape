from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Game stages
STAGES = [
	"Transcription Initiation",
#	"Transcription Elongation",
#	"Pre-mRNA Splicing",
#	"mRNA Transport",
#	"Translation Initiation",
#	"Translation Elongation",
#	"Post-Translational Modification"
]

def generate_dna_sequence(length=12):
	bases = ['A', 'T', 'C', 'G']
	return ''.join(random.choice(bases) for _ in range(length))

def generate_question(stage):
	if stage == "Transcription Initiation":
		dna = generate_dna_sequence()
		question = f"Type the RNA sequence transcribed from this DNA (5' to 3'): {dna}"
		answer = dna.replace('T', 'U')
		return question, answer
	return "Placeholder question", "answer"

@app.route('/')
def home():
	question, answer = generate_question(STAGES[0])
	return render_template('index.html', stage=STAGES[0], question=question, correct_answer=answer, stage_index=0)

@app.route('/check', methods=['POST'])
def check_answer():
	user_answer = request.form['answer']
	correct_answer = request.form['correct_answer']
	current_stage = int(request.form['stage_index'])
    
	if user_answer.strip().upper() == correct_answer.upper():
		next_stage = current_stage + 1 if current_stage + 1 < len(STAGES) else None
		if next_stage is None:
			return render_template('win.html')
		question, answer = generate_question(STAGES[next_stage])
		return render_template('index.html', stage=STAGES[next_stage], question=question, correct_answer=answer, stage_index=next_stage)
	else:
		# Regenerate question and answer for the current stage
		question, answer = generate_question(STAGES[current_stage])
		return render_template('index.html', stage=STAGES[current_stage], question=question, correct_answer=answer, stage_index=current_stage, error="Wrong answer, try again!")

@app.route('/win')
def win():
	return render_template('win.html')

if __name__ == '__main__':
	app.run(debug=True)

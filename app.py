from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

# Game stages
STAGES = [
    "Transcription Initiation",
    "Transcription Elongation",
    "Pre-mRNA Splicing",
    "mRNA Transport",
    "Translation Initiation",
    "Translation Elongation",
    "Post-Translational Modification"
]


def generate_dna_sequence(length=12):
    bases = ['A', 'T', 'C', 'G']
    return ''.join(random.choice(bases) for _ in range(length))


def generate_rna_sequence(length=12):
    bases = ['A', 'U', 'C', 'G']
    return ''.join(random.choice(bases) for _ in range(length))


def reverse_complement(dna):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join(complement[base] for base in dna[::-1])


def generate_question(stage):
    if stage == "Transcription Initiation":
        dna = generate_dna_sequence(12)
        direction = random.choice(["5' to 3'", "3' to 5'"])
        if direction == "5' to 3'":
            question = f"Type the RNA sequence transcribed from this DNA template strand (5' to 3'): {dna}"
            answer = dna.replace('T', 'U')
        else:
            question = f"Type the RNA sequence transcribed from this DNA template strand (3' to 5'): {dna}"
            answer = reverse_complement(dna).replace('T', 'U')
        return question, answer

    elif stage == "Transcription Elongation":
        dna = generate_dna_sequence(15)
        partial_rna = dna[:5].replace('T', 'U')
        question = f"During elongation, RNA polymerase has transcribed {partial_rna} from this DNA template (5' to 3'): {dna}. Complete the full RNA sequence (5' to 3')."
        answer = dna.replace('T', 'U')
        return question, answer

    elif stage == "Pre-mRNA Splicing":
        exon1 = generate_rna_sequence(5)
        intron = generate_rna_sequence(6)
        exon2 = generate_rna_sequence(5)
        pre_mrna = exon1 + intron + exon2
        question = f"Splice this pre-mRNA (5' to 3'): {pre_mrna}. Introns are {intron}. Type the mature mRNA sequence."
        answer = exon1 + exon2
        return question, answer

    elif stage == "mRNA Transport":
        mrna = generate_rna_sequence(12)
        question = f"This mRNA sequence (5' to 3'): {mrna} is ready for transport from the nucleus to the cytoplasm. Type the sequence as it appears in the cytoplasm (assuming no modifications)."
        answer = mrna
        return question, answer

    elif stage == "Translation Initiation":
        mrna = "AUG" + generate_rna_sequence(9)
        question = f"For this mRNA (5' to 3'): {mrna}, type the first amino acid coded by the start codon."
        answer = "Met"
        return question, answer

    elif stage == "Translation Elongation":
        codons = {"UUU": "Phe", "AUG": "Met", "UAA": "Stop", "GCU": "Ala"}
        mrna = "AUG" + "GCU" + "UUU" + "UAA"
        question = f"Translate this mRNA (5' to 3'): {mrna} into its amino acid sequence (use three-letter codes, separate with hyphens, e.g., Met-Ala)."
        answer = "Met-Ala-Phe-Stop"
        return question, answer

    elif stage == "Post-Translational Modification":
        sequence = "Met-Ala-Phe"
        question = f"This polypeptide: {sequence} needs a phosphate group added to function. Type the modified residue if 'Ala' is phosphorylated (e.g., p-Ala)."
        answer = "p-Ala"
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
        return render_template('index.html', stage=STAGES[next_stage], question=question, correct_answer=answer,
                               stage_index=next_stage)
    else:
        question, answer = generate_question(STAGES[current_stage])
        return render_template('index.html', stage=STAGES[current_stage], question=question, correct_answer=answer,
                               stage_index=current_stage, error="Wrong answer, try again!")


@app.route('/win')
def win():
    return render_template('win.html')


if __name__ == '__main__':
    app.run(debug=True)
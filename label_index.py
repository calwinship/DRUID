import json

with open("data/questions_repo.json", "r") as f:
    x = json.load(f)

def build_label_index(json_data):
    """
    Builds an index for quick lookup of questions by label.
    """
    label_index = {}
    for year, papers in json_data.items():
        for paper, questions in papers.items():
            for question_number, question_details in questions.items():
                for label in question_details.get("labels", []):
                    if label not in label_index:
                        label_index[label] = []
                    label_index[label].append((year, paper, question_number))
    return label_index


# Build the index
label_index = build_label_index(x)
print(label_index)

# Now you can quickly get questions by label
def get_questions_by_label(label_index, label):
    return label_index.get(label, []) # better than label_index[label] because it won't raise a KeyError if the label is not found

# Example usage
questions_probability = get_questions_by_label(label_index, "Probability")
for part in questions_probability:
    print(part)

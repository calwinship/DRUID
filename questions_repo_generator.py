import json


class QuestionsRepo:
    def __init__(self, filepath = "data/questions_repo.json"):
        self.exams = {}
        self.filepath = filepath
        if self.filepath:
            self.load_from_file()

    def add_exam(self, year, paper, question, parts, solutions, images, labels):
        if year not in self.exams:
            self.exams[year] = {}
        if paper not in self.exams[year]:
            self.exams[year][paper] = {}
        if question not in self.exams[year][paper]:
            self.exams[year][paper][question] = {"parts": {}, "solutions": {}, "images": [], "labels": []}
        for image in images:
            if image not in self.exams[year][paper][question]["images"]:
                self.exams[year][paper][question]["images"].append(image)
        for label in labels:
            if label not in self.exams[year][paper][question]["labels"]:
                self.exams[year][paper][question]["labels"].append(label)
        for part, content in parts.items():
            self.exams[year][paper][question]["parts"][part] = content
        for part, solution in solutions.items():
            self.exams[year][paper][question]["solutions"][part] = solution

    def get_exam(self, year, paper, question):
        try:
            return self.exams[year][paper][question]
        except KeyError:
            print(f"Question {question} not found in paper {paper} of year {year}")
            return None
        
    def save_to_file(self):
        with open(self.filepath, "w") as f:
            json.dump(self.exams, f, indent=4)

    def load_from_file(self):
        try:
            with open(self.filepath, "r") as f:
                self.exams = json.load(f)
        except FileNotFoundError:
            print(f"No existing file found at {self.filepath}. Starting with an empty repository.")
        except json.JSONDecodeError:
            print("Error decoding JSON from the file. Starting with an empty repository.")


year = "2022",
paper = "2",
question = "10",
parts = {
    "ai": "In an athletics competition, there were a number of heats of the 1500 m race. In the heats, the times that it took the runners to complete the 1500 m were approximately normally distributed, with a mean time of 225 seconds and a standard deviation of 12 seconds. Find the percentage of runners in these heats who took more than 240 seconds to run the 1500 m.",
    "aii": "The 20% of runners with the fastest times qualified for the final. Assuming the race times were normally distributed as described above, work out the time needed to qualify for the final, correct to the nearest second.",
    "b": "Sally takes part in a number of different races in the competition. The probability that she makes a false start in any given race is 5%. Find the probability that she makes her first false start in her fourth race. Give your answer correct to 4 decimal places.",
    "c": "20 relay teams took part in the competition. For any particular team, the probability that they drop the baton at some point during the competition is 0.1. Find the probability that at most 2 teams drop the baton during the competition. Give your answer correct to 4 decimal places.",
    "d": "300 runners take part in a road race. Each runner has a number, from 1 to 300 inclusive. No two runners have the same number. Two runners are picked at random from the runners in this race. Work out the probability that the sum of their numbers is 101. Give your answer as a fraction in its simplest form."
},
solutions = {
    "ai": "𝑧 = (240-225) / 12 = 15 / 12 = 1.25, 𝑃(𝑥 > 240) = 𝑃(𝑧 > 1.25) = 1 − 𝑃(𝑧 < 1.25) = 1 − 0.8944 = 0.1056. Answer: 10.56%",
    "aii": "Look up 𝑃=0.8: 𝑧=0.84 or 0.85. Time=(225 - x)/12 = 0.84. So Time= 225 − 0.84(12) = 214.92. Or Time = 225 − 0.85(12) = 214.8. Accept time = 214 [secs] or 215 [secs].",
    "b": "1 − 0.05 = 0.95. 𝑃 = 0.95 × 0.95 × 0.95 × 0.05 = 0.04286 ... = 0.0429 [4 D.P.]",
    "c": "𝑃(at most 2) = 𝑃(0 or 1 or 2) = 𝑃(0) + 𝑃(1) + 𝑃(2) = 0.9^20 + 20C1 * 0.1 * 0.9^19 + 20C2 * 0.1^2 * 0.9^18 = 0.12157 ... + 0.27017 ... + 0.28517 ... = 0.67692 ... = 0.6769 [4 D.P.]",
    "d": "50 possible pairs of numbers add to 101: 1+100, 2+99, ..., 50+51. 300C2 = 44850 pairs in total. So 𝑃 = 50/44850 = 1/897. OR 100 different 1st numbers could be picked; for each, only one 2nd number will give 101: 𝑃 = (100/300) * (1/299) = 1/897."
},
images = ["Exam22_2_Q10_A.png", "Exam22_2_Q10_B.png", "Exam22_2_Q10_C.png", "Exam22_2_Q10_D.png"]
labels = ["Probability", "Statistics"]

# print(questions_repo.exams['2021']['2']['8'])

if __name__ == "__main__":
    questions_repo = QuestionsRepo()     
    
    questions_repo.add_exam(year, paper, question, parts, solutions, images, labels)

    questions_repo.save_to_file()

# year="2022",
# paper="2",
# question="10",
# parts={
#     "a": "The school caretaker has a box with 23 room keys in it. 12 of the keys are for general classrooms, 6 for science labs and 5 for offices. Four keys are drawn at random from the box. What is the probability that the 4th key drawn is the first office key drawn? Give your answer correct to 4 decimal places.",
#     "b": "All the keys are returned to the box. Then 3 keys are drawn at random from the box one after the other, without replacement. What is the probability that one of them is for a general classroom, one is for a science lab and one is for an office? Give your answer correct to 4 decimal places."
# },
# solutions={
#     "a": "Assuming no replacement: (18/23) * (17/22) * (16/21) * (5/20) = 0.11518... = 0.1152 OR Assuming replacement: (18/23)^3 * (5/23) = 0.10420... = 0.1042",
#     "b": "((12/23) * (6/22) * (5/21)) * 3! = 0.20327... = 0.2033"
# },
# images=["images/Exam21_2_Q8c.JPG"], 
# labels=["Probability", "bernoulli_trials"]


# st.image('Exam22_2_Q5_B.png')

# tags = {"Probability", "bernoulli_trials"}

# exam = {
#     "questions": { 
#         "b": {
#             "In 2019, people with a pre-pay mobile phone plan spent an average (mean) of €20.79 on their mobile phone each month (source: www.comreg.ie). In 2021, some students carried out a survey to see if this figure had changed. They surveyed a random sample of 500 people with pre-pay mobile phone plans. For this sample, the mean amount spent per month was €22.16 and the standard deviation was €8.12. Carry out a hypothesis test at the 5% level of significance to see if this shows a change in the mean monthly spend on mobile phones for people with a pre-pay plan. State your null hypothesis and your alternative hypothesis, state your conclusion, and give a reason for your conclusion."
#         }
#     },
#     "solutions": {
#         "b": {
#             "Null Hypothesis: Average [mean] amount has not changed. Alternative Hypothesis: Average [mean] amount has changed. Conclusion: The average amount has changed. Calculations & Reason: 𝑧 = (22.16 - 20.79) / (8.12 / sqrt(500)) = 3.7726 ..., which is greater than 1.96 OR 20.79 ± 1.96 * (8.12 / sqrt(500)) = [20.07.., 21.51..], and 22.16 lies outside this range OR 22.16 ± 1.96 * (8.12 / sqrt(500)) = [21.44.., 22.87...], and 20.79 lies outside this range."
#         }
#     }
# }




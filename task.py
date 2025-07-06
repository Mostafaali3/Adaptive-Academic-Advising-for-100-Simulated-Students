import random
import networkx as nx
import matplotlib.pyplot as plt
import json
import pickle

COURSE_INTEREST_MAP = {
    "AI101": "AI",
    "SEC101": "Security",
    "DS101": "Data Science"
}

def build_curriculum_graph():
    G = nx.DiGraph()

    courses = {
        "CS101": [],
        "CS102": ["CS101"],
        "CS201": ["CS102"],
        "CS202": ["CS102"],
        "CS301": ["CS201"],
        "AI101": ["CS201"],
        "DS101": ["CS102"],
        "SEC101": ["CS201"],
        "MATH101": [],
        "MATH201": ["MATH101"],
    }

    # Add nodes and edges
    for course, prereqs in courses.items():
        G.add_node(course)
        for prereq in prereqs:
            G.add_edge(prereq, course)

    return G


INTERESTS = ["AI", "Security", "Data Science"]
ALL_COURSES = list(COURSE_INTEREST_MAP.keys()) + ["CS101", "CS102", "CS201", "CS202", "CS301", "MATH101", "MATH201"]


def generate_student(student_id, graph):
    completed = set()
    available_courses = set([c for c in graph.nodes if graph.in_degree(c) == 0])
    max_courses = random.randint(2, 6)
    max_courses_per_term = random.randint(3, 5)  # course load limit per term
    failed_courses = set()
    term_courses = 0

    while len(completed) < max_courses and available_courses:
        if term_courses >= max_courses_per_term:
            break  # reached per-term limit

        course = random.choice(list(available_courses))
        # Simulate grade and retake logic
        grade = round(random.uniform(1.0, 4.0), 2)

        if grade >= 2.0:
            completed.add(course)
        else:
            failed_courses.add(course)

        term_courses += 1

        # Update available courses
        for c in graph.nodes:
            if c not in completed and c not in failed_courses:
                prereqs = list(graph.predecessors(c))
                if all(p in completed for p in prereqs):
                    available_courses.add(c)

        available_courses -= completed
        available_courses -= failed_courses

    completed = list(completed)
    grades = {course: round(random.uniform(2.0, 4.0), 2) for course in completed}
    gpa = round(sum(grades.values()) / len(grades), 2) if grades else 0.0
    interest = random.choice(INTERESTS)
    return {
        "id": student_id,
        "completed_courses": completed,
        "grades": grades,
        "gpa": gpa,
        "interest": interest,
        "failed_courses": list(failed_courses),
        "max_courses_per_term": max_courses_per_term
    }


def simulate_students(n=100, graph=None):
    return [generate_student(f"S{i:03}", graph) for i in range(1, n+1)]



def get_eligible_courses(student, graph):
    completed = set(student["completed_courses"])
    eligible = []
    for course in graph.nodes:
        if course in completed:
            continue
        prereqs = list(graph.predecessors(course))
        if all(p in completed for p in prereqs):
            eligible.append(course)
    return eligible


def heuristic_course_recommendation(student, graph):
    eligible = get_eligible_courses(student, graph)
    interest = student["interest"]
    max_courses = student["max_courses_per_term"]

    prioritized = [c for c in eligible if COURSE_INTEREST_MAP.get(c) == interest]
    others = [c for c in eligible if c not in prioritized]

    recommended = prioritized + others
    return recommended[:max_courses]


if __name__ == "__main__":

    G = build_curriculum_graph()
    with open("curriculum_graph.pkl", "wb") as f:
        pickle.dump(G, f)


    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1500, edge_color='gray', arrows=True)
    plt.title("University Curriculum Graph")
    plt.savefig("curriculum_graph.png")
    plt.close()


    students = simulate_students(100, graph=G)
    with open("students.json", "w") as f:
        json.dump(students, f, indent=4)


    heuristic_recs = {}
    for student in students[:10]:
        heuristic_recs[student["id"]] = heuristic_course_recommendation(student, G)

    with open("heuristic_recommendations.json", "w") as f:
        json.dump(heuristic_recs, f, indent=4)

    print("Curriculum, student simulation, and heuristic-based recommendations complete.")
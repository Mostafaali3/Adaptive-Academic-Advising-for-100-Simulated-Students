# Course Recommendation System

A Python-based course recommendation system that uses graph theory to model university curriculum dependencies and provides personalized course recommendations based on student interests and academic progress.

## 🎯 Overview

This system simulates a university course recommendation engine that:
- Models curriculum structure using directed acyclic graphs (DAGs)
- Generates realistic student academic profiles
- Provides personalized course recommendations based on prerequisites and interests
- Visualizes curriculum dependencies and student progress

## 🏗️ System Architecture

### Graph Schema
The curriculum is represented as a directed graph where:
- **Nodes**: Individual courses
- **Edges**: Prerequisite relationships (A → B means A is prerequisite for B)
- **Structure**: Ensures proper academic sequencing and dependency management

### Course Structure
```
Foundation → Intermediate → Advanced → Specialization
CS101       CS102         CS201      AI101 (AI)
MATH101  →  MATH201    →  CS202   →  SEC101 (Security)
                          DS101      CS301 (Advanced CS)
```

## 📋 Requirements

```bash
pip install networkx matplotlib json pickle random
```

## 🚀 Quick Start

1. **Clone and run the system:**
```bash
python course_recommendation.py
```

2. **Generated outputs:**
   - `curriculum_graph.pkl`: Serialized graph structure
   - `curriculum_graph.png`: Visual representation of course dependencies
   - `students.json`: Simulated student profiles
   - `heuristic_recommendations.json`: Course recommendations for sample students

## 🔧 Core Components

### 1. Graph Construction (`build_curriculum_graph()`)
Creates the curriculum dependency graph with the following courses:

| Course | Prerequisites | Type |
|--------|--------------|------|
| CS101  | None | Foundation |
| CS102  | CS101 | Intermediate |
| CS201  | CS102 | Advanced |
| CS202  | CS102 | Advanced |
| CS301  | CS201 | Specialization |
| AI101  | CS201 | Specialization (AI) |
| DS101  | CS102 | Specialization (Data Science) |
| SEC101 | CS201 | Specialization (Security) |
| MATH101| None | Foundation |
| MATH201| MATH101 | Intermediate |

### 2. Student Generation (`generate_student()`)
Creates realistic student profiles with:
- **Academic History**: Completed courses with grades (2.0-4.0 scale)
- **GPA Calculation**: Based on completed courses only
- **Course Load**: Random limit (3-5 courses per term)
- **Interest Area**: AI, Security, or Data Science
- **Failed Courses**: Tracked separately, block dependent courses

### 3. Recommendation Engine (`heuristic_course_recommendation()`)
Provides personalized recommendations using:
- **Prerequisite Validation**: Ensures all dependencies are met
- **Interest Prioritization**: Favors courses matching student interests
- **Capacity Management**: Respects individual course load limits

## 📊 Student Profile Structure

```json
{
  "id": "S001",
  "completed_courses": ["CS101", "CS102", "MATH101"],
  "grades": {"CS101": 3.2, "CS102": 2.8, "MATH101": 3.5},
  "gpa": 3.17,
  "interest": "AI",
  "failed_courses": [],
  "max_courses_per_term": 4
}
```

## 🎯 Recommendation Algorithm

The system uses a heuristic approach:

1. **Identify Eligible Courses**: Find courses with completed prerequisites
2. **Apply Interest Filter**: Prioritize courses matching student interest
3. **Respect Constraints**: Limit recommendations to course load capacity
4. **Return Ranked List**: Interest-aligned courses first, then others

```python
def heuristic_course_recommendation(student, graph):
    eligible = get_eligible_courses(student, graph)
    interest = student["interest"]
    max_courses = student["max_courses_per_term"]
    
    # Prioritize interest-aligned courses
    prioritized = [c for c in eligible if COURSE_INTEREST_MAP.get(c) == interest]
    others = [c for c in eligible if c not in prioritized]
    
    recommended = prioritized + others
    return recommended[:max_courses]
```

## 📈 Example Usage

### Generate Student Population
```python
# Create curriculum graph
G = build_curriculum_graph()

# Generate 100 students
students = simulate_students(100, graph=G)

# Get recommendations for a specific student
recommendations = heuristic_course_recommendation(students[0], G)
```

### Analyze Student Progress
```python
# Check eligible courses for a student
eligible_courses = get_eligible_courses(students[0], G)

# View student academic profile
student_profile = students[0]
print(f"Student {student_profile['id']}: GPA {student_profile['gpa']}")
print(f"Completed: {student_profile['completed_courses']}")
```

## 🔍 Key Features

- **Academic Policy Compliance**: 100% prerequisite validation
- **Personalized Recommendations**: Interest-based course prioritization
- **Realistic Simulation**: Grade-based progression with failure handling
- **Scalable Design**: Handles varying student populations
- **Visual Analytics**: Graph visualization and progress tracking

## 📁 File Structure

```
course_recommendation_system/
├── course_recommendation.py    # Main system code
├── curriculum_graph.pkl        # Serialized graph (generated)
├── curriculum_graph.png        # Graph visualization (generated)
├── students.json              # Student profiles (generated)
├── heuristic_recommendations.json # Recommendations (generated)
└── README.md                  # This file
```


## 🔗 Dependencies

- **NetworkX**: Graph creation and manipulation
- **Matplotlib**: Visualization and plotting
- **JSON**: Data serialization
- **Pickle**: Object serialization
- **Random**: Student simulation

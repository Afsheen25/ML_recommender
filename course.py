from flask import Flask, render_template, request
import pickle
import csv
app = Flask(__name__)

# Load the course list and similarity matrix using pickle

    # Load the pickle file
with open(r'edx_data.pkl', 'rb') as f:
    courses = pickle.load(f)
with open(r'similarity.pkl','rb') as s:
    similarity = pickle.load(s)  


# Create a list of course titles
course_list = list(courses['subject'])




@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        # Get the selected subject from the form
        selected_subject = request.form.get('selected_subject')
        
        # Use the selected subject and similarity matrix to recommend similar courses
        recommended_courses = recommend(selected_subject)
        course_url=get_url(selected_subject)
        
        # Return the recommended courses to the template
        return render_template('home.html', course_list=course_list, recommended_courses=recommended_courses,course_url=course_url)

    return render_template('home.html', course_list=course_list)

def recommend(course):
    course = course.lower()
    course_indices = courses[courses['subject'] == course].index
    if len(course_indices) > 0:
        course_index = course_indices[0]
        distances = similarity[course_index]
        recommended_courses=[]
        course_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]
        for i in course_list:
            recommended_courses.append(courses.iloc[i[0]].title)
            
            

    else:
        print(f"No courses found for subject: {course}")   

    return recommended_courses    

def get_url(course):
    course = course.lower()
    course_indices = courses[courses['subject'] == course].index
    if len(course_indices) > 0:
        course_index = course_indices[0]
        distances = similarity[course_index]
        course_url=[]
        course_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]
        for i in course_list:
            course_url.append(courses.iloc[i[0]].url)
            

    else:
        print(f"No courses found for subject: {course}")   

    return course_url      

@app.route('/about')
def about():
    return 'This is the about page.'

@app.route('/contact')
def contact():
    return 'Contact us at contact@example.com.'

@app.route('/home')
def home():
    return 'welcome.'

        
if __name__ == '__main__':
    app.run()

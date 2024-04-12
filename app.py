from utils import connector, generate_recommendations, get_recommendations
from flask import Flask, request
from flask_cors import CORS

tf_idf = []
model = []
context = {
    "tf_idf" : None,
    "model" : None,
    "ids_arr" : None
}
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/generateRecommendation', methods = ["GET"])
def generate_recommendation() :
    global context
    context["ids_arr"], skills_arr = connector()
    context["tf_idf"], context["model"] = generate_recommendations(skills_arr, min(len(context["ids_arr"]), 50))
    
@app.route('/getRecommendation', methods = ["POST"])
def get_recommendation() :
   data = request.get_json()
   skills = data["skills"]
   recommendations = get_recommendations(context["tf_idf"], context["ids_arr"], context["model"], skills)
   return {
       "recommendations" : recommendations
   }

if __name__ == '__main__':
    context["ids_arr"], skills_arr = connector()
    context["tf_idf"], context["model"] = generate_recommendations(skills_arr)
    app.run()
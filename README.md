# Chats-and-Sentiment-Analyzer
A web-based tool built using Python, Machine Learning, and Flask to analyze personal and group chats. The application provides insightful statistics and sentiment analysis of conversations, helping users understand engagement levels and emotional tones in their messages.

## Project Overview
This project processes chat data (like WhatsApp/Telegram exports), cleans and structures it, then uses machine learning to perform sentiment classification. It offers visual insights such as:

* Most active users

* Message frequency over time

* Common words used

* Sentiment distribution (positive, neutral, negative)

## Key Features
### Chat Statistics Dashboard

* Total messages, media shared, and word counts

* Most active participants

* Most used words and emojis

### Time-Based Analysis

* Messages by date, week, and month

* Activity heatmaps and timelines

### Sentiment Analysis

* Classify each message as Positive, Neutral, or Negative

* Sentiment trendline over time

### Web App Interface (Flask)

* Simple and intuitive UI to upload chat files

* Real-time processing and visualization

### Tech Stack
* **Frontend:** HTML, CSS, JavaScript

* **Backend:** Python (Flask)

* **ML Models:** Logistic Regression, Random Forest, etc.

* **Libraries:** Pandas, NLTK, Matplotlib, Seaborn, Scikit-learn

* **Deployment:** Heroku

## How Sentiment Analysis Works
* Text is cleaned (removing emojis, stopwords, etc.)

* Vectorized using TF-IDF or CountVectorizer

* Trained using a labeled dataset with ML models

* Each message is predicted and labeled with a sentiment tag

## How To Run The Proect
1. Clone the repository
git clone https://github.com/your-username/your-repo-name.git

2. Navigate to the project directory
cd your-repo-name

3. Install dependencies
pip install -r requirements.txt

4. Run the Flask app
python app.py

5. Open in your browser
http://localhost:5000

## Sample Chat Support
* Supports chat exports from platforms like WhatsApp (in .txt format)

* Just upload the file through the web interface and get instant insights

import React from "react";
import Card from "react-bootstrap/Card";
import { ImPointRight } from "react-icons/im";

function AboutCard() {
  return (
    <Card className="quote-card-view">
      <Card.Body>
        <blockquote className="blockquote mb-0">

          <p style={{ textAlign: "justify" }}>
            Hello there! <br></br>I am <span className="purple">Sai Akhilesh</span>, a Master’s graduate in Computer Science (Data Science) from <span className="purple">The University of Texas at Arlington</span>, passionate about transforming data into actionable insights and driving innovation.
            <br /><br />
            With expertise in <span className="purple">SQL</span>, <span className="purple">Python</span>, <span className="purple">Tableau</span>, <span className="purple">Power BI</span>, <span className="purple">Dataiku DSS</span>, <span className="purple">Statistical Analysis (Inferential and Descriptive Statistics)</span>, <span className="purple">Machine Learning</span>, <span className="purple">Data Visualization</span>, <span className="purple">Data Wrangling</span>, <span className="purple">ETL Pipelines</span>, and <span className="purple">CI/CD Pipelines</span>.
            <br /><br />
            I bring hands-on experience in healthcare analytics, utilizing <span className="purple">Python</span> and <span className="purple">SQL</span> for data preprocessing and feature engineering, developing insightful dashboards with <span className="purple">Tableau</span> and <span className="purple">Power BI</span>, and exploring <span className="purple">Natural Language Processing (NLP)</span>, <span className="purple">Sentiment Analysis</span>, and <span className="purple">Generative AI Applications</span> using <span className="purple">OpenAI’s Large Language Models (LLMs)</span>.
            <br /><br />
            Additionally, I have experience with <span className="purple">Cloud Platforms like AWS</span> for scalable data solutions and deploying projects through <span className="purple">CI/CD Pipelines</span> for continuous integration and delivery.
            <br /><br />
            I am eager to make an impact in data and analytics through innovative, data-driven solutions.
          </p>
        </blockquote>
      </Card.Body>
    </Card>
  );
}

export default AboutCard;

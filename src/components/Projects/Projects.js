import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import ProjectCard from "./ProjectCards";
import Particle from "../Particle";
import leaf from "../../Assets/Projects/leaf.png";
import chatify from "../../Assets/Projects/chatify.png";
import suicide from "../../Assets/Projects/suicide.png";
import bitsOfCode from "../../Assets/Projects/blog.png";
import aiDocIntelligence from "../../Assets/Projects/aiDocIntelligence.png";
import dataLineage from "../../Assets/Projects/PLTR.png"; // Updated image name

function Projects() {
  return (
    <Container fluid className="project-section">
      <Particle />
      <Container>
        <h1 className="project-heading">
          My Recent <strong className="purple">Works </strong>
        </h1>
        <p style={{ color: "white" }}>
          Here are a few projects I've worked on recently.
        </p>
        <Row style={{ justifyContent: "center", paddingBottom: "10px" }}>
          {/* AI Document Intelligence */}
          <Col md={4} className="project-card">
            <ProjectCard
              imgPath={aiDocIntelligence}
              isBlog={false}
              title="AI Document Intelligence"
              description={
                "Streamlit‑based system that ingests PDFs, extracts text via PyMuPDF, " +
                "summarizes content with GPT‑4 (LangChain), classifies by category, " +
                "analyzes sentiment, and provides an AI chatbot for Q&A. " +
                "Integrates with Zapier webhooks and Salesforce tasks for end‑to‑end automation."
              }
              ghLink="https://github.com/akhilesh360/Automation"
              demoLink="https://automation-ddwvwyexfe56f6s6bcowz5.streamlit.app/"
            />
          </Col>

          <Col md={4} className="project-card">
            <ProjectCard
              imgPath={chatify}
              isBlog={false}
              title="Algeria Wild Fires Prediction"
              description="Developed a predictive model using Ridge regression to assess wildfire risks in Algeria with 98.4% accuracy based on environmental data like temperature, humidity, and wind speed. Deployed the application via Flask and AWS Elastic Beanstalk, enabling user input and predictions. Built a CI/CD pipeline from GitHub to AWS for seamless updates."
              ghLink="https://github.com/akhilesh360/ForestFiresPrediction"
              demoLink="http://forestfiresprediction-env-1.eba-djbn9yjg.us-east-2.elasticbeanstalk.com/"
            />
          </Col>

          <Col md={4} className="project-card">
            <ProjectCard
              imgPath={bitsOfCode}
              isBlog={false}
              title="AI Video Insight Assistant"
              description="Developed AI Video Insight Assistant leveraging DeepSeek LLM to summarize YouTube transcripts and answer user queries. Utilized YouTube Transcript API for transcript extraction and concise summarization. Deployed via Streamlit and GitHub for seamless user access. Ensured secure API key management with environment variables and GitHub Secrets, enabling scalable, user-friendly interaction for video analysis and Q&A functionality."
              ghLink="https://github.com/akhilesh360/youtubevideoassistant"
              demoLink="https://saiyoutubeassistant.streamlit.app/"
            />
          </Col>

          {/* LexFoundry */}
          <Col md={4} className="project-card">
            <ProjectCard
              imgPath={dataLineage}
              isBlog={false}
              title="Palantir - LexFoundry, Legal API Integration & Data Governance Framework"
              description="“Lex” is Latin for “law,” and this project reflects a modern data engineering approach to managing complex legal data lifecycles with agility and governance. Prototype simulating legal data ingestion, transformation, ontology modeling, and access control using Palantir Foundry. Demonstrates a modern, end-to-end legal data pipeline, integrating client, case, and document data from multiple sources (including REST APIs) into Foundry pipelines. Highlights best practices in data quality, automation, semantic modeling, and security on the Foundry platform."
              ghLink="https://github.com/akhilesh360/LexFoundry"
            />
          </Col>

          <Col md={4} className="project-card">
            <ProjectCard
              imgPath={leaf}
              isBlog={false}
              title="Customer Review Sentiment Analysis"
              description="Developed a sentiment analysis model using Logistic Regression to assess customer sentiments in car rental reviews. The model predicted sentiments based on customer feedback, helping optimize car inventory. Deployed the solution using Dataiku for training, testing, and sentiment prediction. Applied text preprocessing techniques, including tokenization, stop word removal, and stemming using NLTK, to prepare the review data. Integrated sentiment prediction into the workflow, enabling real-time analysis of new customer reviews."
              ghLink="https://github.com/akhilesh360/Sentiment-Analysis-in-Dataiku-DSS/tree/main"
            />
          </Col>

          <Col md={4} className="project-card">
            <ProjectCard
              imgPath={suicide}
              isBlog={false}
              title="Customer Segmentation based on Spending"
              description="Developed a customer segmentation model using KMeans Clustering to group customers based on spending behavior, annual income, and age. The dataset included 5 features. The model segmented customers into distinct clusters, ensuring quick and efficient analysis. Results were visualized through a 3D scatter plot, with clusters highlighted by color to clearly interpret patterns. These insights enable the company to target customers more effectively based on their age and spending behavior, driving the design of efficient marketing strategies and personalized campaigns."
              ghLink="https://github.com/akhilesh360/Customer_Segmentation"
            />
          </Col>
        </Row>
      </Container>
    </Container>
  );
}

export default Projects;

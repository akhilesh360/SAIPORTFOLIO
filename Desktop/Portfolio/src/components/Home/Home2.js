import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import myImg from "../../Assets/avatar.svg";
import Tilt from "react-parallax-tilt";
import {
  AiFillGithub,
  AiOutlineTwitter,
  AiFillInstagram,
} from "react-icons/ai";
import { FaLinkedinIn } from "react-icons/fa";

function Home2() {
  return (
    <Container fluid className="home-about-section" id="about">
      <Container>
        <Row>
          <Col md={8} className="home-about-description">
            <h1 style={{ fontSize: "2.6em" }}>
            A Quick Story <span className="purple">  About </span>  My Journey
            </h1>
            <p className="home-about-body">
              My name is <span className="purple">SAI AKHILESH</span>, I am a data enthusiast who views the world through the lens of curiosity and innovation. For me, data isn’t just numbers on a screen—it’s a treasure trove of stories waiting to be uncovered, a tool to solve problems, and a means to create meaningful impact.
              <br />
              <br />
              <strong><span className="purple">A Quick Story About My Journey</span></strong>
              <br />
              I’ve always been fascinated by the power of data to transform chaos into clarity. Imagine using <span className="purple">SQL</span> to analyze thousands of feedback entries, uncovering trends that reshape business strategies. Picture leveraging <span className="purple">Python</span> to build predictive models that not only forecast outcomes with precision but also provide clarity in uncertain scenarios. Using tools like <span className="purple">Power BI</span> and <span className="purple">Tableau</span>, I’ve crafted visualizations that turn complex datasets into intuitive stories, making insights accessible to everyone. This version highlights your technical expertise while maintaining the narrative flow and impact of the original text.
              <br />
              <br />
              Every dataset I encounter feels like a puzzle waiting to be solved. Whether it’s uncovering hidden patterns through exploratory analysis or designing dashboards that empower stakeholders with actionable insights, I thrive on turning raw data into something meaningful and impactful.
              <br />
              <br />
              <strong><span className="purple">Why Data Matters More Than Ever</span></strong>
              <br />
              Did you know that <span className="purple">88% of the world’s data has been generated in the last 10 years?</span> Every day, new data is being generated everywhere—on social media, in transactions, through IoT devices and it holds immense potential for organizations. Some of the most impactful applications include:
              <ul>
                <li><span className="purple">Sentiment Analysis</span>: Understanding customer emotions to improve experiences</li>
                <li><span className="purple">Future Demand Prediction</span>: Staying ahead of trends for better planning</li>
                <li><span className="purple">Customer Segmentation</span>: Driving personalized marketing strategies</li>
                <li><span className="purple">Fraud Detection</span>: Safeguarding financial systems and operations</li>
              </ul>
              <span className="purple">Data is the new oil</span>. But just like oil, its value lies in how it’s refined and used. Those who know how to harness its power hold the key to innovation and transformation.
              <br />
              <br />
              <strong><span className="purple">What Drives Me</span></strong>
              <br />
              For me, every project is an opportunity to make an impact—whether it’s conducting exploratory analysis to uncover hidden patterns or designing dashboards that empower stakeholders with actionable insights. It’s not just about using tools or techniques; it’s about creating real-world value through data-driven decisions.
              <br />
              <br />
              I believe in the power of data to change perspectives, solve problems, and build a better future. My ultimate goal is to leverage my skills to make the <span className="purple">world a better place</span> to live - one data-driven decision at a time.
              <br />
              <br />
              <span className="purple">Interested in unlocking potential, Let us connect!</span>
            </p>
          </Col>
          <Col md={4} className="myAvtar">
            <Tilt>
              <img src={myImg} className="img-fluid" alt="avatar" />
            </Tilt>
          </Col>
        </Row>
        <Row>
          <Col md={12} className="home-about-social">
            <h1>FIND ME ON</h1>
            <p>
              Feel free to <span className="purple">connect </span>with me
            </p>
            <ul className="home-about-social-links">
              <li className="social-icons">
                <a
                  href="https://github.com/akhilesh360?tab=repositories"
                  target="_blank"
                  rel="noreferrer"
                  className="icon-colour  home-social-icons"
                >
                  <AiFillGithub />
                </a>
              </li>
              
              <li className="social-icons">
                <a
                  href="https://www.linkedin.com/in/saiakhileshveldi/"
                  target="_blank"
                  rel="noreferrer"
                  className="icon-colour  home-social-icons"
                >
                  <FaLinkedinIn />
                </a>
              </li>
              
            </ul>
          </Col>
        </Row>
      </Container>
    </Container>
  );
}
export default Home2;

# WorkTrust  
**An AI-Powered Workplace Safety and Trust Platform for Women**

---

## Overview

WorkTrust is a full-stack platform designed to improve workplace safety and transparency for women through anonymous reporting, AI-driven analysis, and graph-based trust modeling.

The system aggregates user experiences across companies, teams, and individuals, and computes a multi-layer trust score to identify patterns of workplace risk, including harassment, bias, and exclusion.

---

## Objectives

- Enable safe and anonymous sharing of workplace experiences  
- Provide data-driven insights into organizational culture  
- Detect systemic issues using aggregated signals  
- Model trust using both community trends and social networks  
- Support informed decision-making for safer workplaces  

---

## System Architecture

### Backend
- FastAPI (Python) for API development  
- MongoDB for flexible and scalable data storage  
- NetworkX for graph-based modeling and trust propagation  
- PyTorch with Hugging Face Transformers for NLP processing  

### Frontend
- React 19 for UI development  
- D3.js for interactive graph visualization  
- React Router for navigation  
- Vite for fast development and build processes  

### Authentication
- Token-based authentication (JWT-style)  
- OTP-based user verification  
- MongoDB-backed account management  

---

## Core Features

- Anonymous workplace reviews and reporting  
- Trust scoring across companies, teams, and individuals  
- Graph-based relationship modeling (user–team–company hierarchy)  
- Visualization of social and professional connections  
- Pattern detection for systemic workplace issues  
- Risk flagging based on aggregated signals  
- Full-text search and entity browsing  

---

## NLP Pipeline

### Sentiment Analysis
- Model: DistilBERT  
- Framework: Hugging Face Transformers with PyTorch  
- Outputs a sentiment score for each review  

### Category Classification
- Keyword-based classification into seven categories:
  - Harassment  
  - Bias  
  - Inclusion  
  - Pay equity  
  - Maternity support  
  - Microaggressions  
  - Workplace culture  

### Toxicity Detection
- Hybrid approach:
  - Keyword-based filtering  
  - Sentiment threshold-based detection  

---

## Trust Scoring Model

WorkTrust computes a composite trust score using three components:

| Component        | Weight |
|-----------------|--------|
| Global Trust     | 0.30   |
| Community Trust  | 0.35   |
| Network Trust    | 0.35   |

### Network Trust Computation

- Graph traversal using Breadth-First Search (BFS)  
- Multi-hop propagation up to 3 levels  
- Per-hop decay factor of 0.5  

This design ensures:
- Higher influence from closer connections  
- Controlled propagation to reduce noise  

---

## Graph Architecture

- Graph Type: NetworkX MultiDiGraph  

### Node Types
- Users  
- Teams  
- Companies  

### Edge Types

**Structural Edges**
- User → Team  
- Team → Company  

**Relationship Edges**
- Friend  
- Colleague  
- Manager  
- Review  

### Visualization
- Ego-graph rendering using D3.js for localized network exploration  

---

## Project Structure

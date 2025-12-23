# Cloud Fun Facts Generator ☁️

A full-stack, serverless cloud project that generates witty cloud computing fun facts using:

- **AWS Lambda** – serverless backend
- **Amazon API Gateway** – HTTP API endpoint
- **Amazon DynamoDB** – stores base fun facts
- **Amazon Bedrock (Claude 3.5 Sonnet)** – rewrites facts in a fun, engaging style
- **Static Frontend (HTML/JS)** – calls the API and displays facts
- **(Optional) AWS Amplify Hosting** – deploy the frontend as a public website

---

## 🧩 Architecture Overview

1. User opens the **Cloud Fun Facts** web page (hosted on Amplify or locally).
2. Frontend calls the `GET /funfact` endpoint on **API Gateway**.
3. API Gateway triggers the **Lambda** function.
4. Lambda:
   - Reads a random fact from the **CloudFacts** table in DynamoDB.
   - Sends it to **Amazon Bedrock (Claude 3.5 Sonnet)**.
   - Receives a witty, AI-enhanced version of the fact.
5. Lambda returns the witty fact as JSON to the frontend.
6. The frontend displays the fact to the user.

---

## 📁 Project Structure

```bash
cloud_fun_facts_project/
├── backend/
│   └── lambda_function.py      # Lambda code (DynamoDB + Bedrock + CORS)
├── frontend/
│   └── index.html              # Single-page HTML frontend
├── architecture.png            # High-level architecture diagram
└── README.md                   # This documentation
```

---

## 🚀 How to Use This Repo

### 1. Backend: Lambda + API Gateway + DynamoDB + Bedrock

- Create a DynamoDB table:

  - **Table name**: `CloudFacts`
  - **Partition key**: `FactID` (String)

- Insert sample items:

  - `FactID`: "1", `FactText`: "AWS S3 was one of the very first AWS services, launched in 2006."`
  - etc. (15+ facts recommended)

- Create a Python Lambda function and paste `backend/lambda_function.py`.

- Attach IAM policies to the Lambda execution role:

  - `AWSLambdaBasicExecutionRole`
  - `AmazonDynamoDBReadOnlyAccess`
  - `AmazonBedrockFullAccess` (for learning/demo)

- Create an **HTTP API** in API Gateway and integrate it with the Lambda.
- Define a route:

  - `GET /funfact`

- Enable CORS for:

  - Origins: `*`
  - Methods: `GET, OPTIONS`
  - Headers: `Content-Type`

### 2. Frontend: HTML

- Open `frontend/index.html` locally in your browser  
  or
- Upload to **AWS Amplify Hosting** as a static site.
- Update the `API_URL` constant in the `<script>` section if your endpoint changes.

---

## 🧪 Testing

- Test Lambda directly from the console to verify it returns a JSON with a witty `fact`.
- Test the API Gateway endpoint via Postman or browser.
- Finally, open the frontend and click **Generate Fun Fact**.

If everything is wired correctly, you’ll see witty, AI-generated cloud facts on each click.

---

## 🧹 Clean-up Steps (Cost Control)

To avoid unintended charges after experimenting:

1. **Amplify App** (if used)
   - Amplify Console → select app → **Actions → Delete app**

2. **API Gateway**
   - API Gateway Console → select your HTTP API → **Delete**

3. **Lambda Functions**
   - Lambda Console → delete `CloudFunFacts` (and any test functions)
   - CloudWatch → Log groups → delete groups under `/aws/lambda/...`

4. **DynamoDB**
   - DynamoDB Console → Tables → delete `CloudFacts`

5. **IAM Role** (optional)
   - IAM → Roles → delete the specific Lambda execution role if not reused.

**Project:** Cloud Fun Facts Generator (Serverless AWS + GenAI)  
**Tech:** AWS Lambda, API Gateway, DynamoDB, Amazon Bedrock (Claude 3.5 Sonnet), HTML/JS, IAM, CloudWatch  

**Highlights:**

- Designed and implemented a fully serverless, event-driven architecture on AWS.
- Integrated DynamoDB for scalable NoSQL storage of application content.
- Used Amazon Bedrock with Claude 3.5 Sonnet to dynamically rewrite and enhance content.
- Built a responsive, CORS-enabled frontend that consumes a secured HTTP API.
- Followed AWS best practices for IAM and resource clean-up to stay within free-tier limits.

This project demonstrates end-to-end cloud solution design: **API + compute + database + GenAI + UI**.

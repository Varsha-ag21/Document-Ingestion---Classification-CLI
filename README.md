# Document Ingestion & Classification Pipeline

### Hexaware Mavericks Gen AI Designathon - July 2025 Submission

This repository contains the Phase 1 prototype for the "Document Ingestion & Classification" application. The project aims to solve the business challenge of manually processing large volumes of unstructured documents by creating an intelligent, automated pipeline using a multi-agent system.

---

## 1. Problem Statement

Enterprises generate hundreds of unstructured documents daily—such as PDFs, scanned images, and emails. The manual process of sorting, extracting data from, and routing these documents is:
- **Slow & Costly:** Human reviewers create a significant operational bottleneck.
- **Error-Prone:** Manual data entry and classification lead to mistakes that can impact compliance and business operations.
- **Unscalable:** The growing volume of documents quickly overwhelms static, manual workflows.

## 2. Our Solution

We propose an AI-powered Multi-Agent System (MAS) that automates the entire document lifecycle. The system is architected as a pipeline of four collaborating AI agents that leverage Generative AI for advanced reasoning and NLP tasks.

The four agents are:
1.  **Ingestor Agent:** Detects and ingests new documents.
2.  **Extractor Agent:** Uses OCR and an LLM to extract text and structured entities.
3.  **Classifier Agent:** Classifies the document into a specific type (e.g., Invoice, Contract).
4.  **Router Agent:** Routes the document and its data to the appropriate downstream system (e.g., ERP, database).

This Phase 1 prototype is a **Command-Line Interface (CLI) application** that simulates the complete, end-to-end functionality of this pipeline.

## 3. Features of the CLI Prototype

- **Automated File Watching:** The `IngestorAgent` automatically detects when new files are added to a specified directory.
- **Simulated Agent Pipeline:** The script runs the document through the full, four-agent workflow.
- **Mock LLM Integration:** The `ExtractorAgent` simulates a call to an LLM service to perform entity extraction, demonstrating where and how GenAI is utilized.
- **Detailed Console Logging:** Provides rich, color-coded console output for monitoring and observability, showing the step-by-step journey of each document.
- **File Management:** Automatically moves processed files from the input directory to a designated `processed` directory.

## 4. Tech Stack

- **Language:** Python 3.x
- **Standard Libraries Used:** `os`, `time`, `json`, `random`, `datetime` (No external packages are required for this prototype).

## 5. Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-github-repo-url>
    cd <your-project-directory>
    ```

2.  **Verify Folder Structure:**
    The script requires two sub-directories to be present. If they don't exist, the script will create them on first run. The required structure is:
    ```
    .
    |-- main.py
    |-- documents_to_process/   <-- Place documents to be processed here
    |-- processed_documents/    <-- Processed files will be moved here
    `-- README.md
    ```

## 6. How to Run and Use the Application

1.  **Run the script from your terminal:**
    ```bash
    python main.py
    ```
    The application will start and begin monitoring the `documents_to_process` folder.

2.  **Add files for processing:**
    To trigger the pipeline, simply **copy or move a file** into the `documents_to_process` folder. You can use any file type (`.txt`, `.pdf`, `.docx`, etc.). For this prototype, the content of `.txt` files will be read, while other file types will have their content simulated.

3.  **Observe the Console Output:**
    Watch the terminal. The script will print detailed logs showing each agent's actions as it processes the document.

4.  **Check the Processed Folder:**
    Once processing is complete, the file will be moved from the `documents_to_process` folder to the `processed_documents` folder.

## 7. Sample Console Output

Here is an example of the output generated when processing an invoice:

[2025-07-28 13:30:00] [INGESTOR AGENT ] New file detected: 'invoice.txt' 
[2025-07-28 13:30:00] [INGESTOR AGENT ] File size: 45 bytes. Event 'INGESTED' created.
[2025-07-28 13:30:01] [EXTRACTOR AGENT ] Received event for 'invoice.txt' 
[2025-07-28 13:30:01] [EXTRACTOR AGENT ] Text content successfully read from file. 
[2025-07-28 13:30:01] [LLM SERVICE ] Analyzing text for entities... 
[2025-07-28 13:30:03] [LLM SERVICE ] Extraction complete. Found 3 entities. 
[2025-07-28 13:30:03] [EXTRACTOR AGENT ] Event 'EXTRACTED' created.
[2025-07-28 13:30:04] [CLASSIFIER AGENT ] Received event for 'invoice.txt' 
[2025-07-28 13:30:05] [CLASSIFIER AGENT ] Document classified as 'Invoice' with 0.97 confidence.
[2025-07-28 13:30:06] [ROUTER AGENT ] Received event for 'invoice.txt' 
[2025-07-28 13:30:07] [ROUTER AGENT ] Action: Calling ERP API with invoice data: {'InvoiceID': 'INV-4812', ...} 
[2025-07-28 13:30:07] [ROUTER AGENT ] Event 'ROUTED' created. Document processing complete.
[2025-07-28 13:30:07] [ORCHESTRATOR     ] Moved 'invoice.txt' to 'processed_documents'

## 8. Future Work (Phase 2)

The next phase of this project will involve building a full-stack application with a web-based UI, including:
- An operator dashboard for live monitoring.
- A visual workflow progress bar for each document.
- Integration with a real LLM API (e.g., Google Gemini).
- A robust event bus (e.g., Kafka or Redis).
- Manual override capabilities for human-in-the-loop corrections.
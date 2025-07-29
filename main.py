import os
import time
import json
import random
import datetime

# --- CONFIGURATION ---
# Directory where new documents will be placed for processing.
# Create this folder in the same directory as the script.
DOCS_TO_PROCESS_DIR = "documents_to_process"

# Directory where processed documents will be moved.
# Create this folder as well.
PROCESSED_DOCS_DIR = "processed_documents"

# --- HELPER FUNCTIONS ---


def print_agent_step(agent_name, message, color_code="36"):
    """Prints a formatted step for a specific agent with a timestamp and color."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Using ANSI escape codes for color. \033[<color_code>m ... \033[0m
    print(
        f"\033[1;{color_code}m[{timestamp}] [{agent_name.upper():<16}] {message}\033[0m"
    )


# --- MOCK EXTERNAL SERVICES ---


def mock_llm_entity_extraction(text_content):
    """
    Simulates calling a Generative AI/LLM API to extract entities from text.
    This represents a "Tool-Using Agent" capability.
    """
    print_agent_step("LLM Service", "Analyzing text for entities...", "35")
    time.sleep(2)  # Simulate network latency and processing time

    text_lower = text_content.lower()
    entities = {"source_text_length": len(text_content)}

    # Rule-based simulation for different document types
    if "invoice" in text_lower:
        entities.update(
            {
                "InvoiceID": f"INV-{random.randint(1000, 9999)}",
                "Amount": f"${random.uniform(100, 5000):.2f}",
                "DueDate": (
                    datetime.date.today() + datetime.timedelta(days=30)
                ).strftime("%Y-%m-%d"),
            }
        )
    elif "contract" in text_lower:
        entities.update(
            {
                "ContractingParties": ["ABC Corp", "XYZ Inc."],
                "EffectiveDate": datetime.date.today().strftime("%Y-%m-%d"),
                "Term": f"{random.randint(1, 5)} Years",
            }
        )
    elif "resume" in text_lower:
        entities.update(
            {
                "CandidateName": "Jane Doe",
                "YearsOfExperience": random.randint(2, 10),
                "KeySkills": ["Python", "GenAI", "System Design"],
            }
        )
    else:
        entities["error"] = (
            "Could not determine document structure for entity extraction."
        )

    print_agent_step(
        "LLM Service", f"Extraction complete. Found {len(entities)-1} entities.", "35"
    )
    return entities


# --- AGENT DEFINITIONS ---
# This structure simulates an "Agentic Framework" where each agent has a specific role.


class IngestorAgent:
    """Scans for new files and starts the processing pipeline."""

    def __init__(self, watch_directory):
        self.watch_directory = watch_directory
        print_agent_step("Ingestor Agent", f"Monitoring directory: '{watch_directory}'")

    def run(self):
        """Checks for a single file to process."""
        for filename in os.listdir(self.watch_directory):
            file_path = os.path.join(self.watch_directory, filename)
            if os.path.isfile(file_path):
                print_agent_step("Ingestor Agent", f"New file detected: '{filename}'")
                try:
                    file_size = os.path.getsize(file_path)
                    # Create the initial event payload
                    event = {
                        "status": "INGESTED",
                        "filename": filename,
                        "original_path": file_path,
                        "metadata": {
                            "size_bytes": file_size,
                            "ingestion_time": datetime.datetime.now().isoformat(),
                        },
                    }
                    print_agent_step(
                        "Ingestor Agent",
                        f"File size: {file_size} bytes. Event 'INGESTED' created.",
                    )
                    return event
                except OSError as e:
                    print_agent_step(
                        "Ingestor Agent", f"Error accessing file {filename}: {e}", "31"
                    )
        return None  # No file found


class ExtractorAgent:
    """Extracts text and structured data from a document."""

    def run(self, event):
        """Processes an 'INGESTED' event."""
        print_agent_step("Extractor Agent", f"Received event for '{event['filename']}'")
        file_path = event["original_path"]

        # Simulate OCR / Text Reading
        try:
            # For this simulation, we'll just read .txt files.
            # For .pdf, .docx, we return placeholder text.
            if file_path.endswith(".txt"):
                with open(file_path, "r") as f:
                    text_content = f.read()
                print_agent_step(
                    "Extractor Agent", "Text content successfully read from file."
                )
            else:
                text_content = f"Simulated OCR content for {event['filename']}. Contains keywords: invoice, contract, or resume."
                print_agent_step("Extractor Agent", f"Simulating OCR for non-TXT file.")

            time.sleep(1)

            # Simulate calling an LLM for entity extraction
            extracted_entities = mock_llm_entity_extraction(text_content)

            # Update the event
            event["status"] = "EXTRACTED"
            event["extracted_text"] = text_content
            event["extracted_entities"] = extracted_entities
            print_agent_step("Extractor Agent", "Event 'EXTRACTED' created.")
            return event

        except Exception as e:
            print_agent_step("Extractor Agent", f"An error occurred: {e}", "31")
            event["status"] = "EXTRACTION_FAILED"
            event["error_message"] = str(e)
            return event


class ClassifierAgent:
    """Classifies the document based on its content."""

    def run(self, event):
        """Processes an 'EXTRACTED' event."""
        print_agent_step(
            "Classifier Agent", f"Received event for '{event['filename']}'"
        )
        text_to_classify = event.get("extracted_text", "").lower()

        doc_type = "Unknown"
        confidence = 0.0

        # Simple keyword-based classification logic
        if "invoice" in text_to_classify:
            doc_type = "Invoice"
            confidence = random.uniform(0.90, 0.99)
        elif "contract" in text_to_classify:
            doc_type = "Contract"
            confidence = random.uniform(0.85, 0.95)
        elif "resume" in text_to_classify:
            doc_type = "Resume"
            confidence = random.uniform(0.88, 0.98)
        else:
            confidence = random.uniform(0.40, 0.60)

        time.sleep(1)

        # Update the event
        event["status"] = "CLASSIFIED"
        event["classification"] = {
            "document_type": doc_type,
            "confidence": round(confidence, 2),
        }
        print_agent_step(
            "Classifier Agent",
            f"Document classified as '{doc_type}' with {confidence:.2f} confidence.",
        )
        return event


class RouterAgent:
    """Routes the document or triggers an action based on its type."""

    def run(self, event):
        """Processes a 'CLASSIFIED' event."""
        print_agent_step("Router Agent", f"Received event for '{event['filename']}'")
        classification = event.get("classification", {})
        doc_type = classification.get("document_type", "Unknown")

        routing_action = "No action taken"

        # Routing logic based on classification
        if doc_type == "Invoice":
            routing_action = (
                f"Calling ERP API with invoice data: {event['extracted_entities']}"
            )
        elif doc_type == "Contract":
            routing_action = "Archiving contract to legal department database."
        elif doc_type == "Resume":
            routing_action = "Forwarding resume to HR Applicant Tracking System."
        else:
            routing_action = "Flagging document for manual review."

        time.sleep(1)
        print_agent_step("Router Agent", f"Action: {routing_action}")

        # Update the event
        event["status"] = "ROUTED"
        event["routing_info"] = {
            "action_taken": routing_action,
            "routed_at": datetime.datetime.now().isoformat(),
        }
        print_agent_step(
            "Router Agent", "Event 'ROUTED' created. Document processing complete."
        )
        return event


# --- MAIN ORCHESTRATION ---


def main():
    """
    Main function to set up agents and run the processing pipeline.
    This simulates the "Event Bus" and overall orchestration.
    """
    print(
        "\n\033[1;34m--- DOCUMENT INGESTION & CLASSIFICATION PIPELINE (CLI PROTOTYPE) ---\033[0m\n"
    )

    # 1. Setup: Create directories if they don't exist
    for dir_path in [DOCS_TO_PROCESS_DIR, PROCESSED_DOCS_DIR]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"Created directory: '{dir_path}'")

    # 2. Initialize Agents
    ingestor = IngestorAgent(DOCS_TO_PROCESS_DIR)
    extractor = ExtractorAgent()
    classifier = ClassifierAgent()
    router = RouterAgent()

    # 3. Main processing loop
    print("\n\033[1;33mStarting processing loop... (Press Ctrl+C to stop)\033[0m")
    try:
        while True:
            # Ingestor checks for a new file
            event = ingestor.run()

            if event:
                # If a file is found, run it through the pipeline
                print("\n\033[1;32m--- Processing New Document --- \033[0m")
                print(
                    f"\033[1;37mInitial Event:\n{json.dumps(event, indent=2)}\033[0m\n"
                )

                # Run through the rest of the agents
                event = extractor.run(event)
                if "FAILED" not in event["status"]:
                    event = classifier.run(event)
                    event = router.run(event)

                print(
                    f"\n\033[1;37mFinal Event State:\n{json.dumps(event, indent=2, default=str)}\033[0m"
                )

                # Move the processed file
                try:
                    processed_path = os.path.join(PROCESSED_DOCS_DIR, event["filename"])
                    os.rename(event["original_path"], processed_path)
                    print_agent_step(
                        "Orchestrator",
                        f"Moved '{event['filename']}' to '{PROCESSED_DOCS_DIR}'",
                        "34",
                    )
                except OSError as e:
                    print_agent_step("Orchestrator", f"Could not move file: {e}", "31")

                print("\n\033[1;32m--- End of Processing ---\033[0m\n")

            # Wait before checking for new files again
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n\n\033[1;33mProcessing stopped by user. Exiting.\033[0m")


if __name__ == "__main__":
    main()

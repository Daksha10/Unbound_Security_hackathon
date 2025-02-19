🚀 Unbound Chat Routing System
📌 Overview
This project is a lightweight chat UI with a secure backend that dynamically routes user prompts to different language model providers. It features regex-based routing policies, an admin portal, and file upload support for intelligent prompt processing.

🛠️ Tech Stack
Frontend: HTML, CSS, JavaScript
Backend: Python (Flask)
Database: PostgreSQL
🎯 Features
✅ Milestone 1: Models Endpoint
GET /models returns a list of supported models.
✅ Milestone 2: Chat Completions
POST /v1/chat/completions routes chat prompts to predefined LLM responses.
✅ Milestone 3: Regex-Based Routing
Stores regex rules in PostgreSQL to dynamically reroute prompts to alternate models.
✅ Milestone 4: Web-Based Chat UI
A minimal UI to select models, input prompts, and receive responses.
✅ Milestone 5: Admin Portal
CRUD operations for regex-based routing policies.
✅ Milestone 6: File Upload Support
Allows PDF uploads with response confirmation.
✅ Milestone 7: Special Routing for File Uploads
Routes file uploads to specific models based on type (e.g., PDFs → Anthropic’s claude-v1).

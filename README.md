# Sindibad Ticket Tagging Service v3.0.0

An intelligent automated ticket tagging and routing service with layered architecture, powered by AI agents using OpenAI Agents SDK. Provides real-time, context-aware classification with modern Python practices and comprehensive monitoring.

## 📋 Problem Analysis (Phase 1)

### Current State
- **Manual Agent Tagging**: Customer service agents manually apply two tags per ticket:
  - **Service Type**: Flight, Hotel, Visa, eSIM, Wallet, Other
  - **Category**: Cancellation, Modify, Top Up, Withdraw, Order Re-Check, Pre-Purchase, Others
- **Pain Points Identified**:
  - Misapplied tags causing poor analytics and incorrect routing
  - Agent fatigue leading to inconsistent tagging quality
  - Ambiguous category definitions creating confusion
  - UI/UX friction in the manual tagging process
  - Lack of standardized training on tag definitions

### Root Cause Analysis

#### 1. Human Error Factors
- **Cognitive Load**: Agents handling multiple conversations simultaneously
- **Time Pressure**: Need to resolve tickets quickly to meet SLAs
- **Subjective Interpretation**: Categories open to personal interpretation
- **Context Switching**: Constantly switching between different service types

#### 2. System Design Issues
- **No Real-time Guidance**: Agents lack immediate feedback on tag accuracy
- **Overlapping Definitions**: Similar categories cause confusion
- **No Validation**: No system checks for tag consistency
- **Training Gaps**: Inconsistent understanding across agents

#### 3. Process Inefficiencies
- **Manual Process**: Every ticket requires manual tagging effort
- **Quality Assurance**: Limited ability to validate tag accuracy
- **Feedback Loop**: No mechanism to improve tagging over time
- **Scalability**: Manual process doesn't scale with volume growth

### Impact Assessment
- **Business Impact**: Poor analytics leading to wrong business decisions
- **Customer Experience**: Incorrect routing causing longer resolution times
- **Agent Productivity**: Time spent on tagging vs customer service
- **Operational Costs**: Increased handling time and reduced efficiency

## 🎯 Solution Design

### Core Objectives
1. **Automate Tagging**: Eliminate manual tagging while maintaining accuracy
2. **Improve Consistency**: Standardize tagging across all agents
3. **Enhance Speed**: Reduce resolution time through better routing
4. **Enable Analytics**: Provide reliable data for business decisions

### Architecture Approach
- **Layered Architecture**: Clean separation of concerns using Domain-Driven Design
- **Two-Layer Tagging**: Keywords (fast) + AI Agent (accurate)
- **Real-time Processing**: Immediate classification and routing
- **Monitoring & Feedback**: Built-in analytics and improvement mechanisms

### Technology Stack
- **AI Engine**: OpenAI Agents SDK for intelligent conversation analysis
- **Backend**: FastAPI with async support for high performance
- **Database**: SQLite with SQLAlchemy for reliable data persistence
- **Frontend**: Web dashboard for real-time monitoring
- **Deployment**: Docker for consistent environments

### Success Criteria
- **Accuracy Target**: >85% tagging accuracy
- **Performance**: <2 second response time
- **Reliability**: 99.9% uptime
- **Scalability**: Handle 1000+ tickets per hour

## 🎯 Overview

Sindibad is a sophisticated ticket tagging system designed to automatically classify customer service conversations across multiple service types and categories. The system uses a layered architecture with AI-powered semantic analysis to ensure accurate, consistent tagging while maintaining high performance and developer experience.

### Key Capabilities

- 🤖 **AI-Powered Analysis**: Pure LLM-based conversation understanding using OpenAI Agents SDK
- 🏗️ **Layered Architecture**: Clean separation of concerns with Domain-Driven Design
- 📊 **Real-Time Dashboard**: Live monitoring and analytics interface
- 🔄 **Two-Layer Tagging**: Keywords (Layer 1) + Agentic AI (Layer 2)
- 🚀 **Modern Python Stack**: FastAPI, UV package manager, comprehensive testing
- 📈 **Performance Monitoring**: Confidence scoring, success rates, and detailed analytics

## 📊 North Star Metrics (Phase 3)

### Primary North Star Metric
**🎯 Tagging Accuracy Rate**
- **Definition**: Percentage of tickets with correct service_type AND category tags
- **Target**: >85% accuracy in first month, >95% within 3 months
- **Measurement**: Manual audit of 100 random tickets weekly + automated validation

### Justification
1. **Business Impact**: Directly correlates with routing efficiency and analytics reliability
2. **Customer Experience**: Accurate tags → faster resolution times → higher satisfaction
3. **Operational Efficiency**: Correct classification → proper agent assignment → reduced handling time
4. **Data Quality**: Reliable tags enable data-driven business decisions
5. **Scalability**: Foundation metric that supports all other improvements

### Secondary Metrics

#### 1. Agent Override Rate
- **Definition**: % of tickets where agents modify auto-applied tags
- **Target**: <15% override rate
- **Justification**: Measures system reliability and agent trust

#### 2. Time-to-Resolution Improvement
- **Definition**: Average time from ticket creation to resolution
- **Target**: 20% improvement from baseline
- **Justification**: Shows routing efficiency gains and customer satisfaction impact

#### 3. Tag Consistency Score
- **Definition**: Variance in tagging for similar ticket types
- **Target**: >95% consistency for identical patterns
- **Justification**: Ensures reliable analytics and reporting

#### 4. Processing Speed
- **Definition**: Average time to tag a conversation
- **Target**: <1.5 seconds for keyword layer, <3 seconds for AI layer
- **Justification**: Enables real-time processing and user experience

#### 5. System Reliability
- **Definition**: Uptime percentage and error rates
- **Target**: 99.9% uptime, <0.1% error rate
- **Justification**: Ensures production readiness and user trust

### Metric Hierarchy
```
🎯 North Star: Tagging Accuracy Rate
├── 📈 Secondary: Agent Override Rate
├── ⚡ Secondary: Processing Speed
├── 🔄 Secondary: Time-to-Resolution
├── 📊 Secondary: Tag Consistency Score
└── 🛡️ Secondary: System Reliability
```

### Measurement Approach
- **Daily Monitoring**: Automated metrics collection
- **Weekly Reports**: Manual accuracy audits and trend analysis
- **Monthly Reviews**: Business impact assessment
- **Quarterly Planning**: Goal adjustments based on performance data

## 🏗️ Architecture

The system follows a **layered architecture** with clear separation of concerns:

```
┌─────────────────┐  Presentation Layer
│   Web Dashboard │  - Real-time monitoring UI
│   REST API      │  - FastAPI endpoints
│   WebSocket     │  - Live updates
└─────────────────┘
        │
┌─────────────────┐  Application Layer
│ Use Cases       │  - Business logic orchestration
│ Services        │  - Application services
│ DTOs            │  - Data transfer objects
└─────────────────┘
        │
┌─────────────────┐  Domain Layer
│ Entities        │  - Core business models (Ticket, Message, Tag)
│ Value Objects   │  - Domain concepts (TaggingResult, Confidence)
│ Enums           │  - Service types and categories
└─────────────────┘
        │
┌─────────────────┐  Infrastructure Layer
│ Database        │  - SQLite with async SQLAlchemy
│ External APIs   │  - OpenAI Agents SDK
│ Configuration   │  - Pydantic settings
└─────────────────┘
```

### Tagging System

The system implements a sophisticated **two-layer tagging approach**:

#### Layer 1: Keywords Engine
- ⚡ **High Performance**: Fast rule-based tagging for clear cases
- 🔍 **Pattern Matching**: Regex-based keyword detection
- 🎯 **Default Fallback**: "Other-Other" classification for unmatched content

#### Layer 2: Agentic AI Engine
- 🤖 **Pure LLM Analysis**: OpenAI Agents SDK for semantic understanding
- 🧠 **Context Awareness**: Natural language processing of full conversations
- 📊 **Confidence Scoring**: Detailed reasoning and confidence levels
- 🔄 **Session Continuity**: Conversation context preservation

### Service Types & Categories

The system classifies tickets into:

**Service Types:**
- ✈️ **Flight**: Bookings, cancellations, modifications, status checks
- 🏨 **Hotel**: Reservations, check-in/out, changes
- 📋 **Visa**: Applications, status, document requirements
- 📱 **eSIM**: Mobile data plans, connectivity, roaming
- 💳 **Wallet**: Payment services, balances, top-ups, withdrawals
- ❓ **Other**: General inquiries or unclear services

**Categories:**
- ❌ **Cancellation**: Cancel services, refunds, termination
- ✏️ **Modify**: Change bookings, updates, alterations
- ➕ **Top Up**: Add funds, recharge, load money
- ➖ **Withdraw**: Remove funds, cash out, transfers
- 🔍 **Order Re-Check**: Check status, verify bookings, confirm details
- ❓ **Pre-Purchase**: Information requests, guidance, how-to questions
- 📝 **Others**: General inquiries, miscellaneous requests

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.12+** - Required runtime environment
- **UV Package Manager** - [Install UV](https://docs.astral.sh/uv/getting-started/installation/) (recommended)
- **OpenAI API Key** - Optional, for AI-powered tagging features

### Step-by-Step Setup Instructions

#### Option 1: Docker (Recommended for Production)

```bash
# Step 1: Clone the repository
git clone <repository-url>
cd sindibad-task

# Step 2: Create environment file
cp .env.example .env

# Step 3: Configure OpenAI API key (optional)
# Edit .env file:
# OPENAI_API_KEY=sk-your-openai-api-key-here

# Step 4: Build and run the application
docker-compose up --build

# Step 5: Verify installation
curl http://localhost:8000/api/health
```

**✅ Service URLs:**
- **API Documentation**: http://localhost:8000/api/docs
- **Dashboard**: http://localhost:8000/dashboard
- **Health Check**: http://localhost:8000/api/health

#### Option 2: UV (Recommended for Development)

```bash
# Step 1: Clone repository
git clone <repository-url>
cd sindibad-task

# Step 2: Install Python 3.12 (if needed)
uv python install 3.12

# Step 3: Sync dependencies and create virtual environment
uv sync

# Step 4: Configure environment (optional)
export OPENAI_API_KEY="sk-your-openai-api-key-here"

# Step 5: Run the application
uv run python main.py

# Alternative: Development mode with hot reload
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

#### Option 3: Traditional pip

```bash
# Step 1: Clone repository
git clone <repository-url>
cd sindibad-task

# Step 2: Create virtual environment
python3.12 -m venv venv

# Step 3: Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Step 4: Install dependencies
pip install -r requirements.txt

# Step 5: Configure environment (optional)
export OPENAI_API_KEY="sk-your-openai-api-key-here"

# Step 6: Run the application
python main.py
```

### 🔧 Configuration

Create a `.env` file in the project root directory:

```bash
# OpenAI Configuration (optional - enables AI features)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Application Settings
APP_ENV=development
DEBUG=true

# Database Settings
DATABASE_URL=sqlite+aiosqlite:///./tickets.db

# Logging Configuration
LOG_LEVEL=INFO
```

### ✅ Verification Steps

```bash
# 1. Check service health
curl http://localhost:8000/api/health

# 2. Access interactive API documentation
open http://localhost:8000/api/docs

# 3. View real-time dashboard
open http://localhost:8000/dashboard

# 4. Test basic API functionality
curl -X GET "http://localhost:8000/api/tickets?limit=5"
```

### 🔍 Troubleshooting

**Common Issues:**
- **Port 8000 already in use**: Change port with `uvicorn src.main:app --port 8001`
- **OpenAI API key issues**: Check `.env` file format and API key validity
- **Database errors**: Ensure write permissions in project directory
- **Python version**: Verify Python 3.12+ with `python --version`

**Logs:**
```bash
# View application logs
uv run python main.py

# Docker logs
docker-compose logs -f sindibad-tagging-service
```

## 🔌 API Usage Guide

The Sindibad service provides a comprehensive REST API. Access interactive documentation at `http://localhost:8000/api/docs`.

### 🚀 Getting Started with APIs

```bash
# Base URL
BASE_URL="http://localhost:8000"

# Health check
curl -X GET "$BASE_URL/api/health"
```

### 📨 Core Ticket Operations

#### 1. Process New Messages (Main Webhook)

```bash
# Create a new ticket with customer message
curl -X POST "$BASE_URL/api/webhooks/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "conv_12345",
    "timestamp": "2025-01-15T14:30:00Z",
    "messages": [
      {
        "text": "My flight got cancelled due to weather and I need to rebook urgently",
        "sender": "user"
      }
    ]
  }'
```

**Response:**
```json
{
  "ticket_id": "550e8400-e29b-41d4-a716-446655440000",
  "conversation_id": "conv_12345",
  "service_type": "Flight",
  "category": "Cancellation",
  "confidence": 0.95,
  "method": "agentic",
  "status": "open",
  "message_count": 1
}
```

#### 2. Retrieve Tickets

```bash
# Get all tickets with pagination
curl -X GET "$BASE_URL/api/tickets?limit=10&offset=0"

# Get specific ticket by ID
curl -X GET "$BASE_URL/api/tickets/550e8400-e29b-41d4-a716-446655440000"

# Get ticket statistics
curl -X GET "$BASE_URL/api/stats"
```

#### 3. Update Ticket Status

```bash
# Mark ticket as closed
curl -X PUT "$BASE_URL/api/tickets/550e8400-e29b-41d4-a716-446655440000/status?status=closed"

# Mark ticket as pending
curl -X PUT "$BASE_URL/api/tickets/550e8400-e29b-41d4-a716-446655440000/status?status=pending"
```

#### 4. Get Tag Explanations

```bash
# Understand why specific tags were applied
curl -X GET "$BASE_URL/api/tickets/550e8400-e29b-41d4-a716-446655440000/tags/explain"
```

**Response:**
```json
{
  "ticket_id": "550e8400-e29b-41d4-a716-446655440000",
  "service_type": "Flight",
  "category": "Cancellation",
  "confidence": 0.95,
  "explanation": "Detected keywords: 'cancelled', 'rebook' in flight context",
  "method": "agentic",
  "timestamp": "2025-01-15T14:30:00Z"
}
```

### 🤖 AI Agent Endpoints

#### Direct Text Analysis

```bash
# Test AI agent with direct text
curl -X POST "$BASE_URL/agentic/tag-text" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=I want to cancel my hotel booking and get a refund"
```

#### Conversation Analysis with Session

```bash
# Analyze multi-message conversation
curl -X POST "$BASE_URL/agentic/tag-conversation" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      "Hi, I need help with my flight",
      "It was cancelled and I want to rebook",
      "Also need to cancel the hotel I booked"
    ],
    "session_id": "user_12345"
  }'
```

#### AI Performance Monitoring

```bash
# Get AI agent metrics
curl -X GET "$BASE_URL/agentic/metrics"

# Reset performance metrics
curl -X POST "$BASE_URL/agentic/reset-metrics"
```

#### AI Decision Explanations

```bash
# Get detailed explanation of AI analysis
curl -X POST "$BASE_URL/agentic/explain-tagging" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": ["My flight was cancelled, help me rebook"]
  }'
```

### 📊 Dashboard & Monitoring

#### Real-time Data

```bash
# Get real-time ticket updates for dashboard
curl -X GET "$BASE_URL/dashboard/api/tickets/realtime"
```

### 🧪 Complete API Workflow Example

```bash
#!/bin/bash

# 1. Check service health
echo "🔍 Checking service health..."
curl -s "$BASE_URL/api/health" | jq .

# 2. Create a new ticket
echo "📝 Creating new ticket..."
TICKET_RESPONSE=$(curl -s -X POST "$BASE_URL/api/webhooks/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "workflow_demo_001",
    "timestamp": "2025-01-15T10:00:00Z",
    "messages": [{"text": "I need to cancel my flight booking", "sender": "user"}]
  }')

echo "Ticket created:"
echo "$TICKET_RESPONSE" | jq .

# 3. Extract ticket ID
TICKET_ID=$(echo "$TICKET_RESPONSE" | jq -r '.ticket_id')

# 4. Get ticket details
echo "📋 Getting ticket details..."
curl -s "$BASE_URL/api/tickets/$TICKET_ID" | jq .

# 5. Get tag explanation
echo "🧠 Getting tag explanation..."
curl -s "$BASE_URL/api/tickets/$TICKET_ID/tags/explain" | jq .

# 6. Update ticket status
echo "✅ Updating ticket status..."
curl -s -X PUT "$BASE_URL/api/tickets/$TICKET_ID/status?status=closed" | jq .

# 7. Get system statistics
echo "📊 Getting system statistics..."
curl -s "$BASE_URL/api/stats" | jq .
```

### 📝 API Response Codes

- **200**: Success
- **201**: Created
- **400**: Bad Request (invalid input)
- **404**: Not Found (ticket doesn't exist)
- **422**: Validation Error
- **500**: Internal Server Error

### 🔐 Authentication

Currently, the API doesn't require authentication. In production, consider adding:
- API Key authentication
- JWT tokens
- OAuth 2.0

### 📋 Rate Limiting

- Default: 100 requests per minute per IP
- Configurable via environment variables
- Applies to all endpoints except health checks

### 🐛 Error Handling

All endpoints return structured error responses:

```json
{
  "detail": "Error description",
  "error_code": "ERROR_TYPE",
  "timestamp": "2025-01-15T10:00:00Z"
}
```

## 💡 Example Use Cases

### Real-World Scenarios

#### ✈️ Flight Service Request
```bash
curl -X POST "http://localhost:8000/api/webhooks/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "flight_mod_001",
    "timestamp": "2025-01-15T10:00:00Z",
    "messages": [
      {
        "text": "I want to modify my flight booking. Can I change the departure date?",
        "sender": "user"
      }
    ]
  }'
```
**Result:** `service_type: Flight`, `category: Modify`

#### 🏨 Hotel Cancellation
```bash
curl -X POST "http://localhost:8000/api/webhooks/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "hotel_cancel_001",
    "timestamp": "2025-01-15T11:00:00Z",
    "messages": [
      {
        "text": "I need to cancel my hotel reservation due to emergency",
        "sender": "user"
      }
    ]
  }'
```
**Result:** `service_type: Hotel`, `category: Cancellation`

#### 💳 Wallet Top-up
```bash
curl -X POST "http://localhost:8000/api/webhooks/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "wallet_topup_001",
    "timestamp": "2025-01-15T12:00:00Z",
    "messages": [
      {
        "text": "How can I add money to my wallet? I want to top up $100",
        "sender": "user"
      }
    ]
  }'
```
**Result:** `service_type: Wallet`, `category: Top Up`

#### 📱 Complex Multi-Service Request
```bash
curl -X POST "http://localhost:8000/api/webhooks/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "complex_001",
    "timestamp": "2025-01-15T13:00:00Z",
    "messages": [
      {
        "text": "My flight got cancelled due to weather and I need to rebook urgently. Can you also help me cancel the hotel since I won'\''t be traveling anymore?",
        "sender": "user"
      }
    ]
  }'
```
**AI Analysis:** The system uses semantic understanding to identify the primary service (Flight) and category (Cancellation) while considering the full context.

## 🧪 Development & Testing

### Running Tests

#### With UV (Recommended)
```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage report
uv run pytest tests/ -v --cov=src --cov-report=html

# Run specific test categories
uv run pytest tests/unit/ -v        # Unit tests
uv run pytest tests/integration/ -v # Integration tests
```

#### With pip
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx pytest-cov

# Run tests
pytest tests/ -v --cov=src --cov-report=html
```

### Code Quality

#### Linting and Formatting
```bash
# With UV (recommended)
uv run ruff check .         # Lint code
uv run ruff format .        # Format code
uv run mypy .              # Type checking
uv run black .             # Code formatting

# With pip
ruff check .
black .
mypy .
```

### Manual Testing Checklist

- [ ] **API Health**: `GET /api/health` returns healthy status
- [ ] **Webhook Processing**: `POST /api/webhooks/messages` creates tickets with proper tags
- [ ] **Ticket Management**: CRUD operations work for tickets
- [ ] **AI Agent**: Direct tagging endpoints return proper classifications
- [ ] **Dashboard**: Web interface loads and shows real-time data
- [ ] **Tag Explanations**: Explanation endpoints provide reasoning
- [ ] **Statistics**: Stats endpoints return accurate metrics

## 📊 Monitoring & Analytics

### Real-Time Dashboard

The system includes a comprehensive web dashboard for monitoring:

- **Live Ticket Feed**: Real-time ticket creation and updates
- **Performance Metrics**: Tagging accuracy, confidence scores, response times
- **Service Distribution**: Breakdown by service types and categories
- **AI Agent Analytics**: Success rates, error tracking, cost monitoring
- **System Health**: API status, database connections, error rates

Access the dashboard at: `http://localhost:8000/dashboard`

### Key Performance Metrics

- **Tagging Accuracy**: Percentage of correct service type + category classifications
- **Processing Time**: Average time to tag conversations
- **Confidence Distribution**: AI agent confidence score analytics
- **Error Rate**: Failed tagging attempts and error types
- **Cost Tracking**: OpenAI API usage and costs (when enabled)

### Logging & Debugging

```bash
# Application logs (with structured JSON)
uv run python main.py

# Docker logs
docker-compose logs -f sindibad-tagging-service

# Debug specific components
uv run python -c "import logging; logging.basicConfig(level=logging.DEBUG)"
```

## 🛠️ Development Roadmap

### ✅ Version 3.0.0 (Current)
- **Layered Architecture**: Clean separation of concerns with DDD
- **AI-Powered Tagging**: OpenAI Agents SDK integration
- **Real-Time Dashboard**: Live monitoring and analytics
- **Modern Python Stack**: FastAPI, UV, comprehensive testing
- **Async Operations**: Full async/await support with SQLAlchemy

### 🚧 Future Enhancements

#### v3.1: Enhanced AI Features
- [ ] Multi-model support (GPT-4, Claude, etc.)
- [ ] Advanced prompt engineering and few-shot learning
- [ ] Confidence threshold optimization
- [ ] Batch processing capabilities

#### v3.2: Advanced Analytics
- [ ] Historical trend analysis
- [ ] Agent performance comparison
- [ ] Automated quality assurance
- [ ] Custom reporting dashboards

#### v4.0: Enterprise Features
- [ ] Multi-language support
- [ ] Integration APIs for external systems
- [ ] Advanced workflow automation
- [ ] Scalability improvements (Redis, PostgreSQL)

### Debug Endpoints

The system provides several debugging and monitoring endpoints:

```bash
# Service health and version info
curl http://localhost:8000/api/health

# Ticket statistics and metrics
curl http://localhost:8000/api/stats

# AI agent performance metrics
curl http://localhost:8000/agentic/metrics

# Interactive API documentation
open http://localhost:8000/api/docs
```

## 🏗️ Technical Details

### Database Schema (SQLite with SQLAlchemy)

The system uses SQLAlchemy with async support for data persistence:

```sql
-- Tickets table
CREATE TABLE tickets (
    ticket_id VARCHAR(36) PRIMARY KEY,
    conversation_id VARCHAR(255) UNIQUE NOT NULL,
    service_type VARCHAR,        -- ServiceType enum
    category VARCHAR,           -- Category enum
    confidence FLOAT DEFAULT 0.0,
    method VARCHAR(50) DEFAULT '',
    status VARCHAR NOT NULL DEFAULT 'open',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Messages table
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id VARCHAR(36) NOT NULL,
    text TEXT NOT NULL,
    sender VARCHAR(50) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets (ticket_id)
);
```

### Core Components

#### Domain Layer
- **Entities**: `Ticket`, `Message`, `Tag` with rich business logic
- **Value Objects**: `TaggingResult`, `Confidence` for immutable data
- **Enums**: `ServiceType`, `Category`, `TicketStatus` for type safety

#### Application Layer
- **Use Cases**: Business logic orchestration (`ProcessMessageUseCase`, `ListTicketsUseCase`)
- **Services**: Application services with dependency injection
- **DTOs**: Data transfer objects for API communication

#### Infrastructure Layer
- **Database**: Async SQLAlchemy with repository pattern
- **External APIs**: OpenAI Agents SDK integration
- **Configuration**: Pydantic settings with environment variable support

### AI Agent Architecture

The system implements a sophisticated AI agent using OpenAI Agents SDK:

```python
# Agent Configuration
ai_agent = Agent(
    name="Conversation Analysis Agent",
    instructions="""Analyze customer service conversations...""",
    output_type=None
)

# Session Management for Conversation Continuity
session = SQLiteSession(session_id, db_path)

# AI Analysis Execution
result = await Runner.run(
    ai_agent,
    f"Analyze this conversation: {combined_text}",
    session=session
)
```

## 🤝 Contributing

### Development Workflow

1. **Fork & Clone**: Fork the repository and create a feature branch
2. **Setup Environment**: Follow the setup guide above using UV
3. **Code Standards**: Ensure all code passes linting and type checking
4. **Testing**: Add comprehensive tests for new features
5. **Documentation**: Update README and docstrings as needed

### Code Standards

#### With UV (Recommended)
```bash
# Install and setup development environment
uv sync

# Format code with black
uv run black .

# Lint with ruff (fast and comprehensive)
uv run ruff check .
uv run ruff format .

# Type checking with mypy
uv run mypy .

# Run tests with coverage
uv run pytest tests/ --cov=src --cov-report=html
```

#### Pre-commit Hooks (Optional)
```bash
# Install pre-commit hooks for automated quality checks
uv run pre-commit install
uv run pre-commit run --all-files
```

### Architecture Guidelines

#### Adding New Service Types
1. **Domain Layer**: Add enum value to `ServiceType` in `src/domain/entities/ticket.py`
2. **Infrastructure**: Update AI agent instructions in `src/infrastructure/external_services/agentic_tagger.py`
3. **Tests**: Add test cases in `tests/` directory
4. **Documentation**: Update this README with new service type

#### Adding New Categories
1. **Domain Layer**: Add enum value to `Category` in `src/domain/entities/ticket.py`
2. **Infrastructure**: Update AI agent instructions for category classification
3. **Tests**: Add comprehensive test coverage
4. **Documentation**: Update README examples and API docs

#### Adding New Features
1. **Domain Layer**: Define entities and business logic
2. **Application Layer**: Create use cases and services
3. **Presentation Layer**: Add API endpoints and dashboard components
4. **Infrastructure**: Implement data persistence and external integrations
5. **Tests**: Unit and integration tests for all layers

### Commit Guidelines

- Use clear, descriptive commit messages
- Reference issue numbers when applicable
- Keep commits focused on single changes
- Squash related commits before merging

### Pull Request Process

1. **Create PR**: Push your feature branch and create a pull request
2. **Description**: Provide detailed description of changes
3. **Testing**: Ensure all tests pass and add new tests as needed
4. **Review**: Address reviewer feedback
5. **Merge**: Squash and merge after approval

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support & Resources

### Getting Help

- **API Documentation**: Interactive docs at `http://localhost:8000/api/docs`
- **Dashboard**: Real-time monitoring at `http://localhost:8000/dashboard`
- **Health Check**: Service status at `http://localhost:8000/api/health`
- **Tag Explanations**: Debug tagging decisions with `/api/tickets/{id}/tags/explain`

### Issue Reporting

When reporting issues, please include:
- Python version and environment details
- OpenAI API key configuration (redacted)
- Example requests and expected vs actual responses
- Relevant log output with `LOG_LEVEL=DEBUG`

### Community

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and general discussion
- **Contributing Guide**: See contributing section above

## 🏆 Acknowledgments

- **OpenAI Agents SDK**: For powering the intelligent conversation analysis
- **FastAPI**: Modern, fast web framework for Python
- **SQLAlchemy**: Powerful ORM with async support
- **UV**: Modern Python package manager for fast development
- **Python Community**: For the rich ecosystem of libraries and tools

---

## 📊 Project Stats

- **Version**: 3.0.0
- **Python**: 3.12+
- **License**: MIT
- **Architecture**: Layered (DDD)
- **Database**: SQLite with async SQLAlchemy
- **AI**: OpenAI Agents SDK
- **Web Framework**: FastAPI
- **Package Manager**: UV

**Built with ❤️ using modern Python practices and AI-powered intelligence**
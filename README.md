# Sindibad Ticket Tagging Service v3.0.0

An intelligent automated ticket tagging and routing service with layered architecture, powered by AI agents using OpenAI Agents SDK. Provides real-time, context-aware classification with modern Python practices and comprehensive monitoring.

## 🎯 Overview

Sindibad is a sophisticated ticket tagging system designed to automatically classify customer service conversations across multiple service types and categories. The system uses a layered architecture with AI-powered semantic analysis to ensure accurate, consistent tagging while maintaining high performance and developer experience.

### Key Capabilities

- 🤖 **AI-Powered Analysis**: Pure LLM-based conversation understanding using OpenAI Agents SDK
- 🏗️ **Layered Architecture**: Clean separation of concerns with Domain-Driven Design
- 📊 **Real-Time Dashboard**: Live monitoring and analytics interface
- 🔄 **Two-Layer Tagging**: Keywords (Layer 1) + Agentic AI (Layer 2)
- 🚀 **Modern Python Stack**: FastAPI, UV package manager, comprehensive testing
- 📈 **Performance Monitoring**: Confidence scoring, success rates, and detailed analytics

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

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- [UV package manager](https://docs.astral.sh/uv/getting-started/installation/) (recommended)
- OpenAI API Key (optional, for AI features)

### Option 1: Docker (Recommended for Production)

```bash
# Clone the repository
git clone <repository-url>
cd sindibad-task

# Copy environment template
cp .env.example .env

# Edit .env file with your OpenAI API key
# OPENAI_API_KEY=sk-your-openai-api-key-here

# Build and run with Docker Compose
docker-compose up --build

# Service available at:
# - API Documentation: http://localhost:8000/api/docs
# - Dashboard: http://localhost:8000/dashboard
# - Health Check: http://localhost:8000/api/health
```

### Option 2: UV (Recommended for Development)

```bash
# Clone the repository
git clone <repository-url>
cd sindibad-task

# Install Python 3.12 (if not available)
uv python install 3.12

# Sync dependencies and create virtual environment
uv sync

# Set OpenAI API key (optional)
export OPENAI_API_KEY="sk-your-openai-api-key-here"

# Run the service
uv run python main.py

# Or run with hot reload for development
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Traditional pip

```bash
# Clone the repository
git clone <repository-url>
cd sindibad-task

# Create and activate virtual environment
python3.12 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key (optional)
export OPENAI_API_KEY="sk-your-openai-api-key-here"

# Run the service
python main.py
```

### 🔑 Configuration

Create a `.env` file in the project root:

```bash
# OpenAI Configuration (optional)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Application Settings
APP_ENV=development
DEBUG=true

# Database Settings
DATABASE_URL=sqlite+aiosqlite:///./tickets.db

# Logging
LOG_LEVEL=INFO
```

### Verify Installation

```bash
# Health check
curl http://localhost:8000/api/health

# API documentation (interactive)
open http://localhost:8000/api/docs

# Dashboard
open http://localhost:8000/dashboard
```

## 🔌 API Reference

The Sindibad service provides a comprehensive REST API with interactive documentation at `/api/docs`.

### Core Endpoints

#### Process Messages (Webhook)

```bash
# Create or update ticket with new messages
curl -X POST "http://localhost:8000/api/webhooks/messages" \
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

#### Ticket Management

```bash
# List all tickets with pagination
curl -X GET "http://localhost:8000/api/tickets?limit=20&offset=0"

# Get specific ticket
curl -X GET "http://localhost:8000/api/tickets/{ticket_id}"

# Update ticket status
curl -X PUT "http://localhost:8000/api/tickets/{ticket_id}/status?status=closed"

# Get ticket statistics
curl -X GET "http://localhost:8000/api/stats"
```

#### Tag Explanations

```bash
# Get explanation for ticket tags
curl -X GET "http://localhost:8000/api/tickets/{ticket_id}/tags/explain"
```

### 🤖 AI Agent Endpoints

The system includes dedicated endpoints for AI-powered analysis:

```bash
# Direct text tagging (development/testing)
curl -X POST "http://localhost:8000/agentic/tag-text" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=I need to cancel my hotel booking and rebook my flight"

# Conversation tagging with session continuity
curl -X POST "http://localhost:8000/agentic/tag-conversation" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": ["I want to book a flight", "Actually, I need to cancel it instead"],
    "session_id": "user_12345"
  }'

# Get AI agent performance metrics
curl -X GET "http://localhost:8000/agentic/metrics"

# Explain AI agent analysis decisions
curl -X POST "http://localhost:8000/agentic/explain-tagging" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": ["My flight was cancelled, help me rebook"]
  }'

# Reset AI agent metrics
curl -X POST "http://localhost:8000/agentic/reset-metrics"
```

### 📊 Dashboard Endpoints

```bash
# Real-time ticket updates (used by dashboard)
curl -X GET "http://localhost:8000/dashboard/api/tickets/realtime"
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
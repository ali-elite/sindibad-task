# Sindibad Ticket Tagging Service - Agentic Enhanced

An intelligent automated ticket tagging and routing service powered by AI agents, designed to provide real-time, context-aware classification while optimizing costs and maintaining high accuracy.

## 🎯 Problem Analysis

### Current State
- Agents manually apply **two tags** per ticket:
  - **Service Type:** Flight, Hotel, Visa, eSIM, Wallet, Other
  - **Category:** Cancellation, Modify, Top Up, Withdraw, Order Re-Check, Pre-Purchase, Others
- **Problems identified:**
  - Misapplied tags causing poor analytics and bad routing
  - Agent fatigue leading to inconsistent tagging
  - Ambiguous category definitions
  - UI/UX friction in manual tagging process
  - Lack of standardized training on tag definitions

### Root Cause Analysis
1. **Human Error Factors:**
   - Cognitive load from handling multiple conversations
   - Time pressure to resolve tickets quickly
   - Subjective interpretation of categories
   
2. **System Design Issues:**
   - No real-time guidance for tag selection
   - Overlapping category definitions
   - No feedback mechanism for tag accuracy

3. **Training Gaps:**
   - Inconsistent understanding of service boundaries
   - No standardized examples for edge cases

## 🚀 Solution Design

### Architecture Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Chat Service  │───▶│  Webhook API    │───▶│ Tagging Engine  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │ Ticket Database │    │ Bot Response    │
                       └─────────────────┘    │    Service      │
                                              └─────────────────┘
```

### V2 Implementation: Agentic AI-Powered System

**Current Approach:** Hybrid AI Agent + Rule-based fallback with cost optimization

**🤖 Agentic Architecture:**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Message  │───▶│  Cost Optimizer │───▶│   AI Agent      │
└─────────────────┘    └─────────────────┘    │  (GPT-3.5)      │
                                │              └─────────────────┘
                                ▼                       │
                       ┌─────────────────┐              ▼
                       │ Rule-based      │    ┌─────────────────┐
                       │ Fallback        │◀───│ Response Cache  │
                       └─────────────────┘    └─────────────────┘
```

**Trade-offs Analysis:**

| Approach | Pros | Cons | V2 Implementation |
|----------|------|------|-------------------|
| **Pure AI** | • Highest accuracy<br>• Context understanding<br>• Natural language processing | • High cost<br>• API dependency<br>• Latency | ❌ Too expensive |
| **Pure Rule-Based** | • No cost<br>• Fast<br>• Reliable | • Limited accuracy<br>• No context<br>• Maintenance heavy | ❌ Not intelligent enough |
| **Hybrid Agentic** ✅ | • High accuracy when needed<br>• Cost optimized<br>• Intelligent fallback<br>• Real-time monitoring | • Complex architecture<br>• API dependency for complex cases | **Perfect for V2** |

**Why Agentic Approach for V2:**
- **Cost Intelligence:** Only uses AI when rule-based confidence is low
- **Real-time Adaptation:** AI handles complex, ambiguous cases
- **Transparent Costs:** Full cost tracking and optimization
- **Business Value:** 90%+ accuracy with controlled costs

### Key Features

1. **🤖 Agentic AI Tagging Engine**
   - OpenAI GPT-3.5 powered intelligent classification
   - Context-aware conversation understanding
   - Cost-optimized hybrid approach (AI + rule-based fallback)
   - Real-time response caching for efficiency
   - Multi-language and complex scenario support

2. **💰 Cost Intelligence System**
   - Token usage tracking and cost monitoring
   - Smart routing: AI only when rule-based confidence < 70%
   - Response caching to minimize API calls
   - Real-time cost metrics and projections
   - Configurable cost thresholds and limits

3. **🔄 Intelligent Fallback Mechanism**
   - Rule-based keyword matching as backup
   - Confidence scoring for decision routing
   - Explainable tagging decisions
   - Seamless degradation when AI unavailable

4. **📊 Advanced Monitoring & Analytics**
   - Real-time performance metrics dashboard
   - Cost tracking per request and monthly projections
   - AI vs rule-based usage analytics
   - Cache hit rates and efficiency metrics
   - Detailed tagging explanations and reasoning

5. **🚀 Enhanced APIs**
   - Async webhook processing for real-time tagging
   - Direct text tagging endpoint for testing
   - Cost metrics and performance monitoring endpoints
   - Advanced ticket management with metadata

## 📊 Success Metrics

### North Star Metric
**Tagging Accuracy Rate**: Percentage of tickets with correct service_type AND category tags
- **Target:** >85% accuracy in first month
- **Measurement:** Manual audit of 100 random tickets weekly

### Secondary Metrics

1. **Agent Override Rate**
   - % of tickets where agents modify auto-applied tags
   - Target: <20% override rate
   - Indicates system reliability

2. **Time-to-Resolution Improvement**
   - Average time from ticket creation to resolution
   - Target: 15% improvement from baseline
   - Shows routing efficiency gains

3. **Tag Consistency Score**
   - Variance in tagging for similar ticket types
   - Target: >90% consistency for identical patterns
   - Measures system reliability

4. **Bot Response Relevance**
   - User satisfaction with initial bot responses
   - Target: >4.0/5.0 rating
   - Indicates proper tag-to-response mapping

### Business Impact Alignment

- **Better Analytics:** Accurate tags → reliable reports → data-driven decisions
- **Faster Routing:** Correct tags → proper agent assignment → reduced resolution time  
- **Reduced Agent Workload:** Automated tagging → less manual work → focus on complex issues
- **Improved Customer Experience:** Faster routing + relevant bot responses → higher satisfaction

## 🏗 Architecture

This project is organized using a **layered architecture** with clear separation of concerns:

```
┌─────────────────┐  Presentation Layer
│   Web UI        │  - Real-time dashboard
│   REST API      │  - API endpoints
└─────────────────┘  - WebSocket support
        │
┌─────────────────┐  Application Layer
│ Use Cases       │  - Business logic
│ Services        │  - Application services
└─────────────────┘  - Orchestration
        │
┌─────────────────┐  Domain Layer
│ Entities        │  - Core business models
│ Value Objects   │  - Domain concepts
└─────────────────┘  - Business rules
        │
┌─────────────────┐  Infrastructure Layer
│ Database        │  - Data persistence
│ External APIs   │  - Third-party services
└─────────────────┘  - Configuration
```

### Tagging Layers

The system implements a **two-layer tagging approach**:

1. **Keywords Layer** (Layer 1): Fast, rule-based tagging using keyword matching
   - Quick initial classification
   - Default fallback to "others-others" if no matches
   - High performance, low latency

2. **Agentic Layer** (Layer 2): Intelligent AI-powered tagging
   - Context-aware conversation analysis
   - Complex scenario handling
   - Confidence-based routing from Layer 1

## 🛠 Setup Guide

### Prerequisites
- Python 3.12+
- UV (Python package manager) - [Install UV](https://docs.astral.sh/uv/getting-started/installation/)
- OpenAI API Key (optional, for AI features)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd sindibad-task

# Set OpenAI API key (optional)
export OPENAI_API_KEY="your-openai-api-key-here"

# Build and run with Docker Compose
docker-compose up --build

# Service will be available at:
# - API: http://localhost:8000/api/docs
# - Dashboard: http://localhost:8000/dashboard
# - Health: http://localhost:8000/api/health
```

### Option 2: Local Development with UV (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd sindibad-task

# Install Python 3.12 (if not already installed)
uv python install 3.12

# Sync dependencies and create virtual environment
uv sync

# Set OpenAI API key for AI features (optional)
export OPENAI_API_KEY="your-openai-api-key-here"

# Run the service
uv run python main.py

# Service will be available at http://localhost:8000
```

### Option 3: Legacy pip setup

```bash
# Clone the repository
git clone <repository-url>
cd sindibad-task

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Set OpenAI API key for AI features (optional)
export OPENAI_API_KEY="your-openai-api-key-here"

# Run the service
python main.py

# Service will be available at http://localhost:8000
```

### 🔑 OpenAI API Configuration

The agentic system can run in two modes:

1. **AI-Enhanced Mode** (with OpenAI API key):
   - Intelligent context-aware tagging
   - Handles complex and ambiguous cases
   - Cost-optimized with smart routing

2. **Rule-Based Mode** (without API key):
   - Falls back to keyword-based tagging
   - Zero API costs
   - Still highly effective for clear cases

**Cost Optimization Features:**
- AI only used when rule-based confidence < 70%
- Response caching reduces duplicate API calls
- Token counting prevents expensive requests
- Real-time cost monitoring and alerts

### Verify Installation

```bash
# Health check
curl http://localhost:8000/health

# API documentation
curl http://localhost:8000/docs
```

## 🔌 API Usage Examples

### Core Ticket Management

#### 1. Send Message (Webhook with Layered Tagging)

```bash
# Create new ticket with complex request - Layered tagging will classify
curl -X POST "http://localhost:8000/api/webhooks/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "conv_12345",
    "timestamp": "2025-01-15T14:30:00Z",
    "messages": [
      {
        "text": "My flight got cancelled due to weather and I need to rebook urgently. Can you also help me cancel the hotel since I won'\''t be traveling anymore?",
        "sender": "user"
      }
    ]
  }'
```

#### 2. List All Tickets

```bash
curl -X GET "http://localhost:8000/api/tickets"
```

#### 3. Get Specific Ticket

```bash
curl -X GET "http://localhost:8000/api/tickets/{ticket_id}"
```

#### 4. Update Ticket Status

```bash
curl -X PUT "http://localhost:8000/api/tickets/{ticket_id}/status?status=closed"
```

### 🤖 Agentic AI Features

#### 5. Direct Text Tagging (Test AI Agent)

```bash
# Test the AI agent directly with any text
curl -X POST "http://localhost:8000/agentic/tag-text" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=I booked a complete travel package but now need to cancel just the hotel portion while keeping my flights"
```

#### 6. Get Performance & Cost Metrics

```bash
# Monitor AI usage, costs, and performance
curl -X GET "http://localhost:8000/agentic/metrics"
```

#### 7. Reset Metrics & Cache

```bash
# Reset performance metrics and clear cache
curl -X POST "http://localhost:8000/agentic/reset-metrics"
```

### Legacy Features

#### 8. Explain Tag Decisions (Rule-based)

```bash
curl -X GET "http://localhost:8000/tickets/{ticket_id}/tags/explain"
```

## 📝 Example Scenarios

### Scenario 1: Flight Modification
```bash
curl -X POST "http://localhost:8000/webhooks/messages" \
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
**Expected Tags:** `service_type: Flight`, `category: Modify`

### Scenario 2: Hotel Cancellation
```bash
curl -X POST "http://localhost:8000/webhooks/messages" \
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
**Expected Tags:** `service_type: Hotel`, `category: Cancellation`

### Scenario 3: Wallet Top-up
```bash
curl -X POST "http://localhost:8000/webhooks/messages" \
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
**Expected Tags:** `service_type: Wallet`, `category: Top Up`

## 🧪 Testing

### Run Tests

#### With UV (Recommended)
```bash
# Run tests (dependencies already installed via uv sync)
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ -v --cov=app --cov-report=html
```

#### With pip
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx pytest-cov

# Run tests
pytest tests/ -v
```

### Manual Testing Checklist

- [ ] Webhook receives messages and creates tickets
- [ ] Tags are correctly applied for different service types
- [ ] Bot responses are generated and logged
- [ ] Tickets can be retrieved and updated
- [ ] Tag explanations work correctly
- [ ] Health check endpoint responds

## 📈 Path to Production

### V1 (Current): Rule-Based Foundation
- ✅ Keyword-based tagging engine
- ✅ Basic bot response generation  
- ✅ API infrastructure
- ✅ Monitoring and logging

### V2: Machine Learning Integration
- [ ] Collect tagged conversation data
- [ ] Train lightweight ML classifier (logistic regression/SVM)
- [ ] A/B test ML vs rule-based tagging
- [ ] Hybrid approach with ML + rule fallback

### V3: Feedback Loop
- [ ] Agent correction interface
- [ ] Tag correction tracking
- [ ] Model retraining pipeline
- [ ] Confidence threshold optimization

### V4: Advanced Features
- [ ] Real-time clarification bot for ambiguous cases
- [ ] Multi-language support
- [ ] Integration with knowledge base
- [ ] Advanced analytics dashboard

## 🔍 Monitoring and Debugging

### Logs Location
- **Application Logs:** Console output with structured JSON
- **Bot Response Logs:** Separate logger for ChatService mock calls
- **Docker Logs:** `docker-compose logs -f`

### Key Log Events
- `TICKET_CREATED`: New ticket creation
- `TAGS_APPLIED`: Automatic tagging results
- `BOT_RESPONSE_GENERATED`: Mock bot response
- `TICKET_UPDATED`: Status or tag changes

### Debug Endpoints
- `GET /tickets/{id}/tags/explain` - See why tags were applied
- `GET /health` - Service health status
- `GET /docs` - Interactive API documentation

## 🏗 System Architecture Details

### Database Schema (SQLite)
```sql
-- Tickets table
CREATE TABLE tickets (
    ticket_id TEXT PRIMARY KEY,
    conversation_id TEXT UNIQUE NOT NULL,
    service_type TEXT,
    category TEXT, 
    status TEXT NOT NULL DEFAULT 'open',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

-- Messages table  
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id TEXT NOT NULL,
    text TEXT NOT NULL,
    sender TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (ticket_id) REFERENCES tickets (ticket_id)
);
```

### Tagging Algorithm
1. **Text Preprocessing:** Convert to lowercase, normalize whitespace
2. **Keyword Matching:** Regex-based pattern matching with word boundaries
3. **Scoring:** Count matches + specificity bonus for rare keywords
4. **Selection:** Highest scoring tag per category
5. **Confidence:** Based on match count and keyword specificity

### Bot Response Logic
1. **Context Analysis:** Service type + category combination
2. **Template Selection:** Pre-defined responses per service/category
3. **Personalization:** Dynamic content based on detected entities
4. **Logging:** Mock external API call for integration testing

## 🤝 Contributing

### Development Setup

#### With UV (Recommended)
```bash
# Development dependencies are already installed via uv sync
# They're defined in pyproject.toml under [tool.uv.dev-dependencies]

# Code formatting
uv run black .

# Linting with ruff (modern, fast linter)
uv run ruff check .
uv run ruff format .

# Traditional linting
uv run flake8 .

# Type checking
uv run mypy .

# Pre-commit hooks (optional)
uv run pre-commit install
uv run pre-commit run --all-files
```

#### With pip
```bash
# Install development dependencies
pip install -e .[dev]

# Code formatting
black .

# Linting  
flake8 .

# Type checking
mypy .
```

### Adding New Service Types
1. Add enum value to `ServiceType` in `models.py`
2. Add keywords to `service_keywords` in `tagging_engine.py`
3. Add response templates to `bot_service.py`
4. Update tests and documentation

### Adding New Categories
1. Add enum value to `Category` in `models.py`  
2. Add keywords to `category_keywords` in `tagging_engine.py`
3. Add response logic to `bot_service.py`
4. Update tests and documentation

## 📄 License

MIT License - See LICENSE file for details.

## 📞 Support

For questions or issues:
1. Check the `/docs` endpoint for API documentation
2. Review logs for debugging information
3. Use `/tickets/{id}/tags/explain` to understand tagging decisions
4. Submit issues with example requests and expected behavior

---

**Built with:** FastAPI, SQLite, Python 3.12+, UV package manager  
**Deployment:** Docker, Docker Compose, UV  
**Architecture:** Microservice, REST API, AI-powered agents
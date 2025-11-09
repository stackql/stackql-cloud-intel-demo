# StackQL Cloud Intelligence Demo

A demonstration of StackQL's Model Context Protocol (MCP) integration with OpenAI, providing a natural language chat interface for querying and analyzing cloud infrastructure.

![StackQL Cloud Intelligence](https://img.shields.io/badge/StackQL-MCP%20Enabled-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green)
![Python](https://img.shields.io/badge/Python-3.11+-yellow)
![License](https://img.shields.io/badge/License-Apache%202.0-red)

## Overview

This demo showcases how StackQL's MCP server can be integrated with AI language models (like OpenAI's GPT-4o mini) to enable natural language querying of cloud infrastructure. Users can ask questions in plain English about their cloud resources, and the AI agent will:

1. Understand the intent
2. Discover available resources using StackQL's MCP tools
3. Construct appropriate StackQL queries
4. Execute queries and retrieve results
5. Present findings in a clear, conversational format

## Features

- **Natural Language Interface**: Ask questions about your cloud infrastructure in plain English
- **Multi-Provider Support**: Query resources across Google Cloud, AWS, Azure, GitHub, Okta, and more
- **Real-time Insights**: Get immediate answers about your cloud estate
- **AI-Powered Analysis**: Leverage GPT-4o mini for intelligent query construction and result interpretation
- **Web-Based UI**: Clean, intuitive Streamlit interface
- **Easy Deployment**: Docker Compose setup for quick starts

## Architecture

```
┌─────────────────┐
│   User Query    │
│  (Natural Lang) │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│   Streamlit Chat UI     │
│   (app.py)              │
└──────────┬──────────────┘
           │
           ▼
┌──────────────────────────┐
│  OpenAI GPT-4o mini      │
│  (Function Calling)      │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  StackQL MCP Client      │
│  (stackql_mcp_client.py) │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  StackQL MCP Server      │
│  (HTTP Protocol)         │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  Cloud Providers         │
│  (GCP, AWS, Azure, etc.) │
└──────────────────────────┘
```

## Prerequisites

- **OpenAI API Key**: Required for the AI agent ([Get one here](https://platform.openai.com/api-keys))
- **StackQL**: Either installed locally or using Docker
- **Python 3.11+**: For running the chat interface
- **Cloud Provider Credentials**: For the providers you want to query

### Option 1: Docker (Recommended)
- Docker and Docker Compose installed

### Option 2: Local Installation
- StackQL installed ([Installation guide](https://stackql.io/docs))
- Python 3.11+ with pip

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/stackql-cloud-intel-demo.git
cd stackql-cloud-intel-demo
```

### 2. Configure Environment

Copy the example environment file and edit it with your credentials:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
STACKQL_MCP_URL=http://127.0.0.1:9912
```

Add cloud provider credentials as needed:

```env
# Google Cloud
GOOGLE_CREDENTIALS=/path/to/google-credentials.json

# AWS
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key

# Azure
AZURE_TENANT_ID=your_tenant_id
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret

# GitHub
GITHUB_TOKEN=your_github_token
```

### 3. Start the Demo

#### Option A: Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

This starts both the StackQL MCP server and the chat interface.

#### Option B: Using the Startup Script

```bash
./start.sh
```

This script will:
- Validate your configuration
- Start the StackQL MCP server
- Create a Python virtual environment
- Install dependencies
- Launch the Streamlit chat interface

#### Option C: Manual Setup

1. Start StackQL MCP Server:

```bash
export GOOGLE_CREDENTIALS=$(cat /path/to/google-credentials.json)

stackql mcp \
  --mcp.server.type=http \
  --mcp.config '{"server": {"transport": "http", "address": "127.0.0.1:9912"}}' \
  --auth='{"google": {"type": "service_account", "credentialsfilepath": "/path/to/google-credentials.json"}}'
```

2. In another terminal, start the chat interface:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### 4. Access the Chat Interface

Open your browser and navigate to:

```
http://localhost:8501
```

## Usage Examples

### Basic Exploration

```
You: What cloud providers are available?
AI: I can help you query the following cloud providers:
    - Google Cloud (google)
    - Amazon Web Services (aws)
    - Microsoft Azure (azure)
    - GitHub (github)
    - Okta (okta)
    ...and many more!
```

### Query Resources

```
You: Show me all my Google Cloud compute instances
AI: Let me query your GCP instances...
    [Executes: SELECT * FROM google.compute.instances WHERE project = 'your-project']

    Found 5 instances in your project:
    1. instance-1 (n1-standard-2, running, us-central1-a)
    2. instance-2 (n1-standard-4, running, us-east1-b)
    ...
```

### Cross-Provider Analysis

```
You: How many compute instances do I have across all providers?
AI: Let me check your compute resources across providers...

    Summary:
    - Google Cloud: 5 instances
    - AWS: 3 instances
    - Azure: 2 instances

    Total: 10 compute instances
```

See [examples.md](examples.md) for more query examples.

## Project Structure

```
stackql-cloud-intel-demo/
├── app.py                      # Streamlit chat interface
├── openai_stackql_agent.py     # OpenAI integration with function calling
├── stackql_mcp_client.py       # StackQL MCP client library
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore rules
├── start.sh                   # Startup script
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Docker Compose configuration
├── examples.md                # Example queries and use cases
└── README.md                  # This file
```

## Available Tools

The StackQL MCP server exposes the following tools to the AI agent:

| Tool | Description | Parameters |
|------|-------------|------------|
| `greet` | Test connection | `name` (string) |
| `list_providers` | List all cloud providers | None |
| `list_services` | List services in a provider | `provider` (string) |
| `list_resources` | List resources in a service | `provider`, `service` |
| `list_methods` | List methods for a resource | `provider`, `service`, `resource` |
| `query_v2` | Execute StackQL query | `sql` (string) |

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | - | Yes |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` | No |
| `STACKQL_MCP_URL` | StackQL MCP server URL | `http://127.0.0.1:9912` | No |
| `GOOGLE_CREDENTIALS` | Path to GCP credentials | - | No |
| `AWS_ACCESS_KEY_ID` | AWS access key | - | No |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | - | No |
| `AZURE_TENANT_ID` | Azure tenant ID | - | No |
| `GITHUB_TOKEN` | GitHub personal access token | - | No |

### StackQL MCP Server Modes

StackQL can be deployed in three different MCP server modes:

1. **Standalone HTTP Server** (used in this demo)
   ```bash
   stackql mcp --mcp.server.type=http --mcp.config '{"server": {"transport": "http", "address": "127.0.0.1:9912"}}'
   ```

2. **MCP + PostgreSQL (In-Memory)**
   ```bash
   stackql srv --mcp.server.type=http --mcp.config '{"server": {"transport": "http", "address": "127.0.0.1:9912"}}' --pgsrv.port 5665
   ```

3. **MCP + PostgreSQL (Reverse Proxy)**
   ```bash
   stackql srv --mcp.server.type=reverse_proxy --mcp.config '{"server": {"transport": "http", "address": "127.0.0.1:9004"}, "backend": {"dsn": "postgres://stackql:stackql@127.0.0.1:5446"}}' --pgsrv.port 5446
   ```

## Troubleshooting

### Connection Issues

**Problem**: Can't connect to StackQL MCP server

**Solutions**:
1. Verify the server is running: `curl http://localhost:9912`
2. Check the logs: `tail -f stackql-mcp.log`
3. Ensure port 9912 is not blocked by firewall
4. Verify `STACKQL_MCP_URL` in `.env` is correct

### Authentication Issues

**Problem**: Queries fail with authentication errors

**Solutions**:
1. Verify cloud provider credentials are set correctly
2. For GCP: Ensure `GOOGLE_CREDENTIALS` points to a valid service account key
3. For AWS: Check that `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are correct
4. Test authentication with StackQL CLI: `stackql exec "SELECT * FROM google.compute.instances"`

### OpenAI API Issues

**Problem**: AI responses are slow or fail

**Solutions**:
1. Verify `OPENAI_API_KEY` is valid
2. Check OpenAI API status: https://status.openai.com
3. Review rate limits on your OpenAI account
4. Try a different model by changing `OPENAI_MODEL` in `.env`

## Development

### Running Tests

```bash
# Test the MCP client
python stackql_mcp_client.py

# Test the OpenAI agent
python openai_stackql_agent.py
```

### Adding New Features

1. **New MCP Tools**: Edit `stackql_mcp_client.py` to add new tool methods
2. **OpenAI Functions**: Update `TOOLS` array in `openai_stackql_agent.py`
3. **UI Enhancements**: Modify `app.py` to add new UI components

## Security Considerations

- **API Keys**: Never commit `.env` file or credentials to version control
- **Cloud Credentials**: Use least-privilege service accounts
- **Network**: Run StackQL MCP server on localhost only, unless properly secured
- **TLS**: For production, use TLS encryption (see StackQL MCP docs)

## Performance Tips

- Use specific queries rather than `SELECT *` for better performance
- Filter results with WHERE clauses when possible
- For large result sets, consider pagination
- Cache frequently accessed data when appropriate

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Resources

- [StackQL Documentation](https://stackql.io/docs)
- [StackQL MCP Server Guide](https://stackql.io/docs/command-line-usage/mcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)

## License

Apache License 2.0

## Support

- GitHub Issues: [Report a bug](https://github.com/yourusername/stackql-cloud-intel-demo/issues)
- StackQL Discord: [Join the community](https://discord.gg/stackql)
- Documentation: [StackQL Docs](https://stackql.io/docs)

## Acknowledgments

- Built with [StackQL](https://stackql.io)
- Powered by [OpenAI](https://openai.com)
- UI created with [Streamlit](https://streamlit.io)

---

Made with ☁️ by the StackQL Community

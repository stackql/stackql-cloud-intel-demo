# StackQL Cloud Intelligence - Example Queries

This document provides example natural language queries you can use with the StackQL Cloud Intelligence demo.

## General Exploration

### Discover Available Providers
- "What cloud providers are available?"
- "List all supported providers"
- "Show me what providers I can query"

### Explore Provider Services
- "What services are available in Google Cloud?"
- "Show me all AWS services"
- "List Azure services"
- "What services does GitHub offer?"

### Discover Resources
- "What compute resources are available in Google Cloud?"
- "Show me storage resources in AWS"
- "List all resources in Azure's compute service"

## Google Cloud Platform (GCP)

### Compute Engine
- "Show me all my Google Cloud compute instances"
- "List all VMs in my GCP project myproject-123"
- "What instances are running in us-central1?"
- "Show me the machine types of my GCP instances"
- "List all compute instances with their IP addresses"

### Cloud Storage
- "Show me all my GCS buckets"
- "List storage buckets in my Google Cloud project"
- "What is the location of my GCS buckets?"

### Networks
- "List all VPC networks in my GCP project"
- "Show me firewall rules in myproject"
- "What subnets do I have configured?"

### IAM
- "List all service accounts in my project"
- "Show me IAM policies for myproject"

## Amazon Web Services (AWS)

### EC2
- "Show me all my AWS EC2 instances"
- "List running instances in us-east-1"
- "What is the instance type of my EC2 instances?"
- "Show me stopped instances"

### S3
- "List all my S3 buckets"
- "Show me S3 buckets in us-west-2"
- "What are the encryption settings for my buckets?"

### VPC
- "List all VPCs in my AWS account"
- "Show me security groups in my default VPC"
- "What subnets are configured?"

### IAM
- "List all IAM users"
- "Show me IAM roles in my account"
- "What policies are attached to this user?"

## Microsoft Azure

### Virtual Machines
- "Show me all Azure virtual machines"
- "List VMs in the East US region"
- "What is the size of my Azure VMs?"

### Storage
- "List all storage accounts"
- "Show me blob containers in my storage account"

### Networking
- "List all virtual networks in Azure"
- "Show me network security groups"

### Resource Groups
- "List all resource groups"
- "Show me resources in my production resource group"

## GitHub

### Repositories
- "List all my GitHub repositories"
- "Show me repositories in my organization"
- "What are my most recently updated repos?"

### Issues and Pull Requests
- "Show me open issues in my repository"
- "List all pull requests"
- "What issues are assigned to me?"

### Teams and Users
- "List all teams in my organization"
- "Show me organization members"

## Okta

### Users
- "List all Okta users"
- "Show me active users"
- "What users were created in the last 30 days?"

### Applications
- "List all Okta applications"
- "Show me which apps are assigned to users"

### Groups
- "List all Okta groups"
- "Show me group memberships"

## Advanced Queries

### Cross-Provider Analysis
- "How many compute instances do I have across all cloud providers?"
- "Compare the number of VMs in AWS vs Azure vs GCP"
- "Show me all storage buckets across providers"

### Resource Optimization
- "Which instances have been running the longest?"
- "Show me underutilized resources"
- "What resources are tagged as 'production'?"

### Security and Compliance
- "List all publicly accessible storage buckets"
- "Show me instances without tags"
- "What resources don't have backup enabled?"
- "List all users with admin privileges"

### Cost Analysis
- "Show me my most expensive instance types"
- "List resources by cost center tag"
- "What resources are in development vs production?"

## Direct StackQL Queries

If you want to execute specific StackQL queries directly, you can ask:

- "Execute this query: SELECT name, status FROM google.compute.instances WHERE project = 'myproject'"
- "Run: SHOW SERVICES IN aws"
- "Query: SELECT bucket_name, location FROM aws.s3.buckets"

## Tips for Effective Queries

1. **Be Specific**: Include project IDs, region names, or resource identifiers when possible
2. **Use Proper Names**: Use the correct provider, service, and resource names
3. **Ask for Help**: If you're unsure what's available, ask "What services are in [provider]?"
4. **Iterate**: Start with broad queries and refine based on results
5. **Combine Filters**: You can ask for specific filters like "running instances in us-east-1"

## Troubleshooting

If you get an error:
- Make sure you've configured authentication for the cloud provider
- Verify that the provider is available with "What providers are available?"
- Check that you're using the correct resource names
- Ensure your StackQL MCP server is running and properly configured

# QA Chat System

An application that allows users to chat with a QA system.

## How It Works

The system operates with three different response modes based on query similarity:

- **High Similarity**: If the search query has a very semantically similar question in the database, the answer of the stored question will be retrieved.

- **Moderate Similarity**: If the search query is moderately similar to a question in the database, the LLM will answer using the stored answer as context.

- **Low Similarity**: If the search is not similar at all, the LLM will answer directly using OpenAI.
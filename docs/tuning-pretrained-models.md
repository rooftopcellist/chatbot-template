---
title: "Tuning Pretrained Models for Optimal Responses"
description: "A comprehensive guide to adjusting model parameters for better performance in the RAG chatbot"
category: "guides"
tags: ["tuning", "parameters", "optimization", "llm", "ollama"]
created: "2023-07-20"
updated: "2023-07-20"
---

# Tuning Pretrained Models for Optimal Responses

This guide explains how to tune the pretrained language model (LLM) used in the chatbot to get the best possible responses for your specific use case. We'll cover all available parameters, when and how to adjust them, and the trade-offs involved.

## Introduction to Model Tuning

The chatbot uses Ollama to run a local LLM (default: qwen3:1.7b). While the RAG architecture helps ground the model's responses in your documentation, tuning the model parameters can significantly improve response quality, accuracy, and style.

The parameters are set in the `query_engine.py` file when initializing the Ollama LLM:

```python
self.llm = Ollama(
    model=config.OLLAMA_MODEL,
    base_url=config.OLLAMA_BASE_URL,
    request_timeout=300.0,
    temperature=0.1,
    num_ctx=4096,
    num_predict=1024,
    repeat_penalty=1.1
)
```

## Core Parameters and Their Effects

### Temperature (`temperature`)

**Current default**: `0.1`

**What it does**: Controls the randomness of the model's outputs. Lower values make the model more deterministic and focused, while higher values make it more creative and diverse.

**When to adjust**:
- **Increase** (e.g., 0.3-0.7) when:
  - Responses are too rigid or predictable
  - You want more creative or diverse answers
  - The chatbot needs to brainstorm or suggest alternatives

- **Decrease** (e.g., 0.0-0.1) when:
  - Factual accuracy is critical
  - You want consistent, predictable responses
  - The model is hallucinating or making things up

**Trade-offs**: Lower temperature reduces creativity but increases reliability. Higher temperature increases creativity but may reduce factual accuracy.

**Example adjustment**:
```python
# For more creative responses
self.llm = Ollama(
    # other parameters...
    temperature=0.7,
)

# For strictly factual responses
self.llm = Ollama(
    # other parameters...
    temperature=0.0,
)
```

### Context Window (`num_ctx`)

**Current default**: `4096`

**What it does**: Determines how many tokens (roughly words or word pieces) the model can consider at once, including both the prompt and the generated response.

**When to adjust**:
- **Increase** (e.g., 8192) when:
  - Your documents contain long, detailed explanations
  - You're retrieving many document chunks (high TOP_K)
  - Responses seem to miss context from retrieved documents

- **Decrease** (e.g., 2048) when:
  - You want to reduce memory usage
  - You're using a smaller model that works better with less context
  - Your documents are short and concise

**Trade-offs**: Larger context windows require more memory and may slow down inference. Smaller context windows use less memory but might miss important information.

**Note**: The maximum possible context window depends on the specific model you're using. Some models support larger contexts than others.

**Example adjustment**:
```python
# For handling more context
self.llm = Ollama(
    # other parameters...
    num_ctx=8192,
)
```

### Maximum Generation Length (`num_predict`)

**Current default**: `1024`

**What it does**: Limits how many tokens the model will generate in its response.

**When to adjust**:
- **Increase** (e.g., 2048) when:
  - You want more detailed, comprehensive answers
  - Responses are being cut off prematurely
  - Your use case requires longer explanations

- **Decrease** (e.g., 512) when:
  - You prefer concise, to-the-point answers
  - You want faster response times
  - You're experiencing memory issues

**Trade-offs**: Longer generation limits allow for more detailed responses but increase generation time. Shorter limits produce faster responses but may omit details.

**Example adjustment**:
```python
# For more detailed responses
self.llm = Ollama(
    # other parameters...
    num_predict=2048,
)

# For concise responses
self.llm = Ollama(
    # other parameters...
    num_predict=512,
)
```

### Repeat Penalty (`repeat_penalty`)

**Current default**: `1.1`

**What it does**: Penalizes the model for repeating the same tokens, helping to prevent repetitive loops or stuttering.

**When to adjust**:
- **Increase** (e.g., 1.2-1.5) when:
  - The model gets stuck in repetitive patterns
  - Responses contain redundant information
  - The model repeats phrases or paragraphs

- **Decrease** (e.g., 1.0-1.05) when:
  - The model seems to avoid necessary repetition
  - Responses feel unnaturally varied
  - You're working with technical content where repetition is expected

**Trade-offs**: Higher penalties reduce repetition but may prevent the model from emphasizing important points. Lower penalties allow natural repetition but may lead to circular responses.

**Example adjustment**:
```python
# For reducing repetition
self.llm = Ollama(
    # other parameters...
    repeat_penalty=1.3,
)
```

### Request Timeout (`request_timeout`)

**Current default**: `300.0` (5 minutes)

**What it does**: Sets the maximum time (in seconds) to wait for the model to generate a response.

**When to adjust**:
- **Increase** when:
  - You're using a larger model that takes longer to generate
  - You've increased the context window or maximum generation length
  - You're experiencing timeout errors

- **Decrease** when:
  - You want to ensure faster response times
  - You're using a smaller, faster model

**Trade-offs**: Longer timeouts prevent premature cutoffs but might leave users waiting. Shorter timeouts ensure responsiveness but might truncate complex responses.

**Example adjustment**:
```python
# For longer generation time
self.llm = Ollama(
    # other parameters...
    request_timeout=600.0,  # 10 minutes
)
```

## Advanced Parameters

These parameters can be added to the Ollama initialization for more fine-grained control:

### Top-P Sampling (`top_p`)

**Recommended range**: `0.1` to `1.0` (default in Ollama: `0.9`)

**What it does**: Controls diversity by considering only the tokens whose cumulative probability exceeds the top_p value. Lower values make the text more focused and deterministic.

**When to adjust**:
- **Increase** (closer to 1.0) for more diverse outputs
- **Decrease** (closer to 0.1) for more focused, deterministic outputs

**Example**:
```python
self.llm = Ollama(
    # other parameters...
    top_p=0.7,  # More focused than default, but still some diversity
)
```

### Top-K Sampling (`top_k`)

**Recommended range**: `1` to `100` (default in Ollama: `40`)

**What it does**: Limits the model to consider only the top K most likely tokens at each step. Lower values make the text more focused.

**When to adjust**:
- **Increase** for more diverse vocabulary and creative responses
- **Decrease** for more predictable, conservative responses

**Example**:
```python
self.llm = Ollama(
    # other parameters...
    top_k=20,  # More conservative token selection
)
```

### Frequency Penalty (`frequency_penalty`)

**Recommended range**: `-2.0` to `2.0` (default in Ollama: `0.0`)

**What it does**: Penalizes tokens based on their frequency in the generated text so far. Positive values discourage repetition of frequent tokens.

**When to adjust**:
- **Increase** (positive values) to encourage use of varied vocabulary
- **Decrease** (negative values) to allow more repetition of common terms

**Example**:
```python
self.llm = Ollama(
    # other parameters...
    frequency_penalty=0.5,  # Encourage more varied vocabulary
)
```

### Presence Penalty (`presence_penalty`)

**Recommended range**: `-2.0` to `2.0` (default in Ollama: `0.0`)

**What it does**: Penalizes tokens that have appeared at all in the generated text so far. Positive values discourage repeating any previous tokens.

**When to adjust**:
- **Increase** (positive values) to discourage repeating any content
- **Decrease** (negative values) to encourage staying on topic

**Example**:
```python
self.llm = Ollama(
    # other parameters...
    presence_penalty=0.5,  # Discourage repeating any previous content
)
```

## Parameter Combinations for Specific Use Cases

### Factual Documentation Assistant

For a chatbot that prioritizes accuracy and factual information:

```python
self.llm = Ollama(
    model=config.OLLAMA_MODEL,
    base_url=config.OLLAMA_BASE_URL,
    temperature=0.0,  # Completely deterministic
    num_ctx=4096,
    num_predict=1024,
    repeat_penalty=1.1,
    top_p=0.5,  # More focused token selection
    frequency_penalty=0.0,
    presence_penalty=0.0
)
```

### Creative Problem Solver

For a chatbot that helps brainstorm solutions and alternatives:

```python
self.llm = Ollama(
    model=config.OLLAMA_MODEL,
    base_url=config.OLLAMA_BASE_URL,
    temperature=0.7,  # More creative
    num_ctx=4096,
    num_predict=2048,  # Longer responses
    repeat_penalty=1.2,  # Avoid repetition
    top_p=0.9,  # More diverse token selection
    frequency_penalty=0.5,  # Encourage varied vocabulary
    presence_penalty=0.3  # Discourage repeating content
)
```

### Concise Technical Support

For a chatbot that provides brief, to-the-point technical answers:

```python
self.llm = Ollama(
    model=config.OLLAMA_MODEL,
    base_url=config.OLLAMA_BASE_URL,
    temperature=0.2,  # Mostly deterministic but slight variation
    num_ctx=4096,
    num_predict=512,  # Shorter responses
    repeat_penalty=1.1,
    top_p=0.7,
    frequency_penalty=0.0,
    presence_penalty=0.0
)
```

## Implementing Parameter Changes

To modify these parameters, you can either:

1. **Edit query_engine.py directly**:
   ```python
   # In query_engine.py
   self.llm = Ollama(
       model=config.OLLAMA_MODEL,
       base_url=config.OLLAMA_BASE_URL,
       temperature=0.3,  # Modified value
       # Other parameters...
   )
   ```

2. **Add parameters to config.py** (recommended):
   ```python
   # In config.py
   # LLM settings
   OLLAMA_MODEL = "qwen3:1.7b"
   OLLAMA_BASE_URL = "http://localhost:11434"
   OLLAMA_TEMPERATURE = 0.3
   OLLAMA_NUM_CTX = 4096
   OLLAMA_NUM_PREDICT = 1024
   OLLAMA_REPEAT_PENALTY = 1.1
   ```

   Then update query_engine.py to use these config values:
   ```python
   # In query_engine.py
   self.llm = Ollama(
       model=config.OLLAMA_MODEL,
       base_url=config.OLLAMA_BASE_URL,
       temperature=config.OLLAMA_TEMPERATURE,
       num_ctx=config.OLLAMA_NUM_CTX,
       num_predict=config.OLLAMA_NUM_PREDICT,
       repeat_penalty=config.OLLAMA_REPEAT_PENALTY
   )
   ```

## Testing and Iterating

The best way to find optimal parameters is through systematic testing:

1. **Create a test set** of representative questions
2. **Try different parameter combinations** and record the results
3. **Gather feedback** from actual users
4. **Iterate and refine** based on the results

Remember that parameter tuning is highly dependent on:
- The specific model you're using
- Your documentation content
- Your team's specific needs and preferences

## Conclusion

Tuning the pretrained model parameters allows you to customize the chatbot's behavior to better suit your team's needs. Start with small adjustments to the most impactful parameters (temperature, context window, and maximum generation length) and fine-tune from there based on the results.

Remember that the RAG architecture already helps ground the model's responses in your documentation. Parameter tuning complements this by controlling the style, tone, and characteristics of the generated responses.

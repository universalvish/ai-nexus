# AI Services Configuration

## AI Service Providers

### OpenAI
```bash
export OPENAI_API_KEY=sk-your-key-here
```

### Anthropic Claude
```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Local Models (Ollama)
```bash
ollama pull llama2
ollama serve
```

## Vector Database (ChromaDB)
```python
CHROMA_PERSIST_DIRECTORY = "./data/chroma"
```
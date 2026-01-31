# Gen AI API Service Research
## Comprehensive Comparison of Free AI Services with 500+ Requests/Day

---

## Executive Summary

This document provides a comprehensive analysis of free Gen AI API services that offer better rate limits than the current Google Gemini API implementation. The goal is to identify services that provide **500+ requests per day** while maintaining quality conversational AI capabilities for the fitness coaching application.

---

## Current Service: Google Gemini API

### Specifications
- **Model Used**: Gemini 2.5 Flash
- **Free Tier Limits** (as of 2026):
  - **15 requests per minute (RPM)**
  - **1 million tokens per minute (TPM)**
  - **1,500 requests per day (RPD)** - Good limit!
  - Rate limit: 15 RPM
- **Pros**:
  - Fast response times
  - Good context understanding
  - Supports JSON structured outputs
  - Free tier is generous
  - Multilingual support
- **Cons**:
  - RPM limit can be restrictive during peak usage
  - Requires internet connection
  - API key management needed

### Current Usage Pattern
- AI voice coach for natural language commands
- Real-time workout guidance
- Context-aware responses
- Exercise control and navigation

---

## Alternative Gen AI Services with Better/Comparable Limits

### 1. ⭐ Groq API (RECOMMENDED)
**Status**: Best Alternative for Speed & Free Tier

#### Specifications
- **Free Tier Limits**:
  - **30 requests per minute (RPM)** - 2x faster than Gemini!
  - **14,400 requests per day (RPD)** - 9.6x more than needed!
  - **6,000 tokens per minute**
  - No credit card required
- **Models Available** (Free Tier):
  - Llama 3.3 70B (Recommended - Most capable)
  - Llama 3.1 8B (Faster, lighter)
  - Mixtral 8x7B
  - Gemma 2 9B
- **Response Time**: 
  - Extremely fast (800+ tokens/second with LPU™ Inference Engine)
  - 10x faster than traditional GPU inference
- **Context Window**: Up to 128K tokens (Llama 3.3)

#### Integration Ease
- Simple REST API or Python SDK
- Drop-in replacement for OpenAI API format
- Good documentation

#### Code Example
```python
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are an enthusiastic AI Fitness Coach..."
        },
        {
            "role": "user",
            "content": "Let's do some pushups!"
        }
    ],
    model="llama-3.3-70b-versatile",  # or llama-3.1-8b-instant for speed
    temperature=0.7,
    max_tokens=1024,
)

response = chat_completion.choices[0].message.content
```

#### Pros
- ✅ **14,400 RPD** - 28.8x more than 500 requirement
- ✅ Ultra-fast inference (800 tokens/sec)
- ✅ Higher RPM than Gemini (30 vs 15)
- ✅ Multiple model options
- ✅ No credit card required
- ✅ OpenAI-compatible API
- ✅ JSON mode support
- ✅ Function calling support

#### Cons
- ⚠️ Smaller context window than Gemini (but sufficient for our use case)
- ⚠️ Primarily open-source models (but high quality)

---

### 2. ⭐ Mistral AI API (RECOMMENDED)
**Status**: Excellent Balance of Quality & Limits

#### Specifications
- **Free Tier** ("La Plateforme" Free Tier):
  - **No hard daily limit initially** (rate-limited instead)
  - **5 requests per second** - Very generous!
  - Free credits: €5 (~$5) monthly
  - With credits: **~2M tokens/month** free
- **Models Available**:
  - Mistral Small (Fast, efficient)
  - Mistral Medium
  - Mixtral 8x7B (Open weight)
- **Context Window**: Up to 32K tokens

#### Integration Ease
- Official Python SDK: `pip install mistralai`
- Clean, simple API
- Good documentation

#### Code Example
```python
from mistralai import Mistral
import os

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

response = client.chat.complete(
    model="mistral-small-latest",
    messages=[
        {
            "role": "system",
            "content": "You are an enthusiastic AI Fitness Coach..."
        },
        {
            "role": "user",
            "content": "Let's do some pushups!"
        }
    ],
    temperature=0.7,
    max_tokens=1024,
)

content = response.choices[0].message.content
```

#### Pros
- ✅ €5 free credits monthly (~2M tokens)
- ✅ 5 requests per second
- ✅ High-quality models
- ✅ JSON mode and function calling
- ✅ European data privacy (Paris-based)
- ✅ Open-weight models available

#### Cons
- ⚠️ Free credits system (not unlimited)
- ⚠️ Need to monitor usage

---

### 3. Together AI
**Status**: Strong Option for Open-Source Models

#### Specifications
- **Free Tier Credits**: $25 free on signup
- **Rate Limits**:
  - Varies by model
  - Generous for free tier users
- **Models Available**:
  - Llama 3.1 405B/70B/8B
  - Mixtral 8x22B
  - Qwen 2.5
  - Many more open-source models
- **Context Window**: Up to 128K tokens

#### Pros
- ✅ $25 free credits (lasts long time)
- ✅ Access to largest models (405B)
- ✅ Wide model selection
- ✅ Fast inference
- ✅ OpenAI-compatible API

#### Cons
- ⚠️ Credit-based system
- ⚠️ Need credit card for signup
- ⚠️ Must monitor spending

---

### 4. OpenRouter
**Status**: Model Aggregator with Free Tier

#### Specifications
- **Free Tier Models**:
  - Various free models available
  - Rate limits per model
  - Some models: **200+ RPD free**
- **Unique Feature**: Access multiple providers through one API
- **Models Available**:
  - Google Gemini (free)
  - Meta Llama (free)
  - Mistral (free)
  - Many others

#### Pros
- ✅ Multiple free models
- ✅ Fallback to different providers
- ✅ Unified API
- ✅ Good for testing different models

#### Cons
- ⚠️ Rate limits vary by model
- ⚠️ Free tier limits can change
- ⚠️ Not all models are free

---

### 5. Hugging Face Inference API
**Status**: Good for Open-Source Models

#### Specifications
- **Free Tier**:
  - **1,000 requests per day** for community models
  - Rate limited (requests per minute vary)
  - No credit card required
- **Models Available**:
  - Thousands of open-source models
  - LLama, Mistral, Falcon, etc.
- **Serverless Inference API**: Free for public models

#### Pros
- ✅ 1,000+ RPD on many models
- ✅ Huge model selection
- ✅ Free tier very accessible
- ✅ No credit card needed
- ✅ Great for experimentation

#### Cons
- ⚠️ Can be slower (cold starts)
- ⚠️ Less reliable for production
- ⚠️ API format varies by model

---

### 6. Anthropic Claude (via APIs.guru or similar)
**Status**: Premium Quality but Limited Free Access

#### Specifications
- **Direct API**: Limited free tier ($5 credit)
- **Via Aggregators**: Some free access available
- **Models**: Claude 3 Haiku (fastest, cheapest)

#### Pros
- ✅ Excellent quality
- ✅ Good at following instructions
- ✅ Strong reasoning

#### Cons
- ⚠️ Limited free tier
- ⚠️ Not ideal for 500+ RPD requirement

---

### 7. Cohere API
**Status**: Production-Ready with Free Tier

#### Specifications
- **Free Tier** (Trial):
  - 100 API calls per minute
  - Limited free tier
  - Good for testing
- **Models Available**:
  - Command-R / Command-R+
  - Optimized for RAG and chat

#### Pros
- ✅ Production-ready
- ✅ Good documentation
- ✅ Fast inference

#### Cons
- ⚠️ Limited free tier
- ⚠️ May not meet 500+ RPD requirement long-term

---

## Detailed Comparison Table

| Service | Free RPD | RPM | Best Model | Speed | Quality | Ease | Credit Card |
|---------|----------|-----|------------|-------|---------|------|-------------|
| **Groq** ⭐ | **14,400** | 30 | Llama 3.3 70B | ⚡ Ultra-fast | ⭐⭐⭐⭐ | Easy | No |
| **Mistral** ⭐ | ~2,000+ | 300 | Mistral Small | ⚡ Fast | ⭐⭐⭐⭐⭐ | Easy | No |
| Gemini (Current) | 1,500 | 15 | Gemini 2.5 Flash | ⚡ Fast | ⭐⭐⭐⭐⭐ | Easy | No |
| Together AI | ~5,000 | Varies | Llama 3.1 405B | ⚡ Fast | ⭐⭐⭐⭐⭐ | Easy | Yes |
| OpenRouter | 200-1,000 | Varies | Multiple | Medium | ⭐⭐⭐⭐ | Medium | No |
| Hugging Face | 1,000+ | Varies | Various | Medium | ⭐⭐⭐ | Medium | No |
| Cohere | Limited | 100 | Command-R | ⚡ Fast | ⭐⭐⭐⭐ | Easy | Trial |

---

## Recommendations

### 🥇 Primary Recommendation: **Groq API**

**Why Groq?**
1. **Exceeds Requirements**: 14,400 RPD vs 500 needed (28.8x more!)
2. **Faster than Gemini**: 30 RPM vs 15 RPM
3. **Ultra-Fast Inference**: 800 tokens/sec response time
4. **No Credit Card**: Easy signup
5. **OpenAI Compatible**: Easy migration path
6. **Free Forever**: No trial period, genuinely free tier
7. **Best for Real-Time**: Perfect for voice coach application

**Best Model for Our Use Case**: `llama-3.3-70b-versatile`
- Excellent instruction following
- Good conversational abilities
- Fast enough for real-time
- 128K context window

**Migration Effort**: Low (2-3 hours)
- Replace google-generativeai with groq
- Update API calls (similar structure)
- Adjust prompt format slightly
- Test and deploy

### 🥈 Secondary Recommendation: **Mistral AI**

**Why Mistral?**
1. **Generous Free Tier**: €5 monthly credits (~2M tokens)
2. **High Rate Limits**: 5 req/sec
3. **Excellent Quality**: On par with GPT-4 for many tasks
4. **European Provider**: Good for GDPR compliance
5. **Production Ready**: Used by many companies

**Best Model**: `mistral-small-latest`
- Fast inference
- Good quality
- Cost-effective

### 🥉 Third Option: **Keep Gemini + Add Groq as Fallback**

**Hybrid Approach**:
1. Use Gemini as primary (current setup)
2. Add Groq as fallback for rate limit scenarios
3. Get best of both worlds
4. Total capacity: 1,500 + 14,400 = 15,900 RPD

---

## Implementation Recommendations

### Recommended Architecture

```python
# Priority-based API router
class AIServiceRouter:
    def __init__(self):
        self.services = [
            {"name": "groq", "client": groq_client, "priority": 1},
            {"name": "gemini", "client": gemini_client, "priority": 2},
            {"name": "mistral", "client": mistral_client, "priority": 3}
        ]
        self.current_service = self.services[0]
    
    def get_response(self, messages):
        for service in self.services:
            try:
                return service["client"].chat(messages)
            except RateLimitError:
                print(f"{service['name']} rate limited, trying next...")
                continue
        raise Exception("All services exhausted")
```

### Migration Steps

1. **Phase 1**: Add Groq alongside Gemini
2. **Phase 2**: Test Groq performance
3. **Phase 3**: Switch primary to Groq
4. **Phase 4**: Keep Gemini as fallback

### Cost Analysis (for reference)

All recommended options are FREE for our use case:
- Groq: Free 14,400 RPD forever
- Mistral: €5/month credit
- Gemini: Free 1,500 RPD forever
- Combined: 15,900+ RPD free capacity

---

## Testing Recommendations

1. **Response Quality Test**
   - Test fitness coaching responses
   - Compare Groq vs Gemini output
   - Measure user satisfaction

2. **Performance Test**
   - Measure response latency
   - Test during peak usage
   - Verify 500+ RPD handling

3. **Reliability Test**
   - Test rate limit behavior
   - Test error handling
   - Test fallback mechanism

---

## Conclusion

**Groq API is the clear winner** for this fitness application:
- ✅ 28.8x more requests than required (14,400 vs 500)
- ✅ Faster inference than current solution
- ✅ Free forever, no credit card
- ✅ Easy migration
- ✅ Perfect for real-time voice coaching

**Action Items**:
1. Sign up for Groq API (free, no credit card)
2. Implement alongside Gemini (2-3 hours work)
3. Test performance in voice coaching scenarios
4. Gradually migrate to Groq as primary
5. Keep Gemini as fallback for reliability

This approach ensures **5x more capacity** than current implementation while maintaining (or improving) quality and speed.

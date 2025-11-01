#!/usr/bin/env python3
"""
Test AI Integration for Notezy Bot
Tests the Grok AI functionality
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_ai_connection():
    """Test basic AI connection and model availability"""
    print("🤖 Testing AI Integration...")
    
    # Check if OpenAI library is available
    try:
        from openai import OpenAI
        print("✅ OpenAI library imported successfully")
    except ImportError as e:
        print(f"❌ OpenAI library not available: {e}")
        return False
    
    # Check if API key is set
    grok_api_key = os.getenv("GROK_API_KEY")
    if not grok_api_key:
        print("❌ GROK_API_KEY not found in environment variables")
        print("💡 Please set GROK_API_KEY in your .env file (using Groq API key)")
        return False
    else:
        print(f"✅ GROK_API_KEY found (Groq): {'*' * (len(grok_api_key) - 10)}{grok_api_key[-10:]}")
    
    # Test basic API call
    try:
        client = OpenAI(
            api_key=grok_api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
        print("🔍 Testing simple AI query...")
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for engineering students."},
                {"role": "user", "content": "Say hello and mention one study tip for VTU engineering students in exactly 2 sentences."}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        ai_response = response.choices[0].message.content.strip()
        print(f"✅ AI Response: {ai_response}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI API call failed: {e}")
        print("💡 Check your GROK_API_KEY (Groq API key) and internet connection")
        return False

def test_query_analysis():
    """Test query analysis functionality"""
    print("\n🔍 Testing Query Analysis...")
    
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=os.getenv("GROK_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        
        test_query = "data structures and algorithms"
        
        analysis_prompt = f"""
        Analyze this user query for a VTU engineering notes search: "{test_query}"
        
        Extract and return only the key subject names, codes, or technical terms that should be used for database search.
        Focus on VTU syllabus subjects, programming languages, algorithms, data structures, engineering concepts.
        Return a comma-separated list of search terms, or the original query if no specific terms can be identified.
        Keep it concise and relevant to engineering education.
        """
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a query analyzer for VTU engineering notes search. Extract key technical terms and subject names."},
                {"role": "user", "content": analysis_prompt}
            ],
            max_tokens=100,
            temperature=0.1
        )
        
        analysis_result = response.choices[0].message.content.strip()
        print(f"✅ Query Analysis:")
        print(f"   Original: {test_query}")
        print(f"   Enhanced: {analysis_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Query analysis test failed: {e}")
        return False

def test_suggestions():
    """Test AI suggestions functionality"""
    print("\n💡 Testing AI Suggestions...")
    
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=os.getenv("GROK_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        
        test_query = "quantum physics"
        
        suggestion_prompt = f"""
        A VTU engineering student searched for: "{test_query}"
        No results found in our notes database.

        Generate 3-4 helpful suggestions:
        1. Alternative search terms they could try
        2. Related VTU subjects they might be interested in
        3. Common misspellings or variations
        4. Broader categories to explore

        Keep suggestions practical and relevant to VTU engineering syllabus.
        Format as a bulleted list.
        """
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful study assistant for VTU engineering students. Provide practical search suggestions."},
                {"role": "user", "content": suggestion_prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        suggestions = response.choices[0].message.content.strip()
        print(f"✅ AI Suggestions for '{test_query}':")
        print(f"{suggestions}")
        
        return True
        
    except Exception as e:
        print(f"❌ Suggestions test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🤖 Notezy Bot AI Integration Test")
    print("=" * 60)
    
    success_count = 0
    total_tests = 3
    
    # Run tests
    if test_ai_connection():
        success_count += 1
    
    if test_query_analysis():
        success_count += 1
        
    if test_suggestions():
        success_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 All AI integration tests passed!")
        print("✅ Your bot is ready with AI features")
    elif success_count > 0:
        print("⚠️ Some AI features are working, but there may be issues")
        print("💡 Check the errors above and your configuration")
    else:
        print("❌ AI integration is not working")
        print("💡 Please check your GROK_API_KEY and internet connection")
    
    print("\n🚀 You can now run your bot with AI features!")
#!/usr/bin/env python3
"""
Quick test script to verify deployment configuration
Run this before deploying to catch common issues
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Check if required environment variables are set"""
    print("=" * 60)
    print("🔍 Checking Deployment Configuration")
    print("=" * 60)
    
    issues = []
    warnings = []
    
    # Check GROQ_API_KEY
    groq_key = os.getenv("GROQ_API_KEY", "")
    if not groq_key:
        issues.append("❌ GROQ_API_KEY is not set")
    elif groq_key == "your_groq_api_key_here":
        issues.append("❌ GROQ_API_KEY is set to placeholder value")
    else:
        print("✅ GROQ_API_KEY is set")
    
    # Check MONGO_URI
    mongo_uri = os.getenv("MONGO_URI", "")
    if not mongo_uri:
        warnings.append("⚠️  MONGO_URI not set (will use default from config.py)")
    else:
        print("✅ MONGO_URI is set")
    
    # Check FastAPI URL
    fastapi_url = os.getenv("FASTAPI_URL", "http://localhost:8000")
    print(f"✅ FASTAPI_URL: {fastapi_url}")
    
    # Check Python environment
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 8:
        print(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        issues.append(f"❌ Python version {python_version.major}.{python_version.minor} is too old (need 3.8+)")
    
    # Check required files
    required_files = [
        "Dockerfile",
        "start_services.sh",
        "api.py",
        "app.py",
        "requirements.txt"
    ]
    
    print("\n📁 Checking required files:")
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} exists")
        else:
            issues.append(f"❌ {file} is missing")
    
    # Summary
    print("\n" + "=" * 60)
    if issues:
        print("❌ ISSUES FOUND:")
        for issue in issues:
            print(f"   {issue}")
        print("\n⚠️  Please fix these issues before deploying!")
        return False
    else:
        print("✅ All checks passed!")
        if warnings:
            print("\n⚠️  WARNINGS:")
            for warning in warnings:
                print(f"   {warning}")
        print("\n🚀 Ready to deploy!")
        return True

if __name__ == "__main__":
    success = check_environment()
    sys.exit(0 if success else 1)

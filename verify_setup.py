#!/usr/bin/env python3
"""
Verification script to check if all dependencies and setup are correct
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def check_files():
    """Check if required files exist"""
    required_files = [
        'backend/app.py',
        'backend/vcf_parser.py',
        'backend/pharmacogenomics.py',
        'backend/drug_risk_predictor.py',
        'backend/llm_explainer.py',
        'app/page.tsx',
        'package.json',
        'requirements.txt',
        '.env.example',
        'README.md'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ Missing: {file}")
            all_exist = False
    
    return all_exist

def check_directories():
    """Check if required directories exist"""
    required_dirs = [
        'backend',
        'app',
        'components',
        'types',
        'test_data'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✓ {dir_path}/")
        else:
            print(f"✗ Missing directory: {dir_path}/")
            all_exist = False
    
    return all_exist

def main():
    """Run all checks"""
    print("PharmaGuard Setup Verification\n")
    print("=" * 40)
    
    print("\n1. Python Version:")
    py_ok = check_python_version()
    
    print("\n2. Required Files:")
    files_ok = check_files()
    
    print("\n3. Required Directories:")
    dirs_ok = check_directories()
    
    print("\n" + "=" * 40)
    if py_ok and files_ok and dirs_ok:
        print("\n✓ All checks passed! Setup looks good.")
        print("\nNext steps:")
        print("1. Install Python dependencies: pip install -r requirements.txt")
        print("2. Install Node dependencies: npm install")
        print("3. Set up .env file with OPENAI_API_KEY")
        print("4. Start backend: cd backend && python app.py")
        print("5. Start frontend: npm run dev")
    else:
        print("\n✗ Some checks failed. Please review above.")
        sys.exit(1)

if __name__ == '__main__':
    main()

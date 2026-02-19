#!/usr/bin/env python3
"""
Simple API test script for PharmaGuard backend
Tests the /api/analyze endpoint with sample VCF file
"""

import requests
import os
import json

def test_api():
    """Test the PharmaGuard API"""
    
    backend_url = os.getenv('BACKEND_URL', 'http://localhost:5000')
    
    # Test health endpoint
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{backend_url}/api/health")
        print(f"✓ Health check: {response.json()}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return
    
    # Test analyze endpoint with sample file
    print("\nTesting analyze endpoint...")
    
    vcf_file_path = 'test_data/sample_patient.vcf'
    if not os.path.exists(vcf_file_path):
        print(f"✗ Test file not found: {vcf_file_path}")
        return
    
    try:
        with open(vcf_file_path, 'rb') as f:
            files = {'vcf_file': ('sample_patient.vcf', f, 'text/vcf')}
            data = {'drugs': 'CODEINE'}
            
            response = requests.post(
                f"{backend_url}/api/analyze",
                files=files,
                data=data
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✓ Analysis successful!")
                print(f"\nResult summary:")
                print(f"  Patient ID: {result['results']['patient_id']}")
                print(f"  Drug: {result['results']['drug']}")
                print(f"  Risk Label: {result['results']['risk_assessment']['risk_label']}")
                print(f"  Phenotype: {result['results']['pharmacogenomic_profile']['phenotype']}")
                print(f"\nFull JSON:")
                print(json.dumps(result, indent=2))
            else:
                print(f"✗ Analysis failed: {response.status_code}")
                print(f"  Error: {response.text}")
                
    except Exception as e:
        print(f"✗ Test failed: {e}")

if __name__ == '__main__':
    test_api()

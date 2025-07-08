#!/usr/bin/env python3
"""
Security Validation Script for QNN Financial Markets
Checks for potential security issues and sensitive data exposure
"""

import os
import re
import sys
from pathlib import Path

class SecurityValidator:
    def __init__(self):
        self.issues = []
        self.warnings = []
        
        # Patterns that might indicate sensitive data (but ignore obvious templates)
        self.sensitive_patterns = [
            (r'api_key\s*=\s*["\'][^"\']*[a-z0-9]{20,}[^"\']*["\']', 'Potential API key hardcoded'),
            (r'secret\s*=\s*["\'][^"\']*[a-z0-9]{20,}[^"\']*["\']', 'Potential secret hardcoded'),
            (r'password\s*=\s*["\'][^"\']*[a-z0-9]{8,}[^"\']*["\']', 'Potential password hardcoded'),
            (r'token\s*=\s*["\'][^"\']*[a-z0-9]{20,}[^"\']*["\']', 'Potential token hardcoded'),
            (r'[A-Za-z0-9+/]{40,}', 'Potential encoded secret or hash'),
        ]
        
        # Files that should not be committed
        self.sensitive_files = [
            '.env',
            'config.py',
            'secrets.txt',
            'api_keys.txt',
            'credentials.txt',
            '*.key',
            '*.pem',
            'trained_parameters.npy',
        ]
    
    def check_file_content(self, file_path):
        """Check file content for sensitive patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            for pattern, description in self.sensitive_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    self.issues.append(f"{file_path}: {description}")
                    
        except Exception as e:
            self.warnings.append(f"Could not read {file_path}: {e}")
    
    def check_git_status(self):
        """Check if sensitive files are tracked by git"""
        try:
            import subprocess
            result = subprocess.run(['git', 'ls-files'], 
                                  capture_output=True, text=True, cwd='.')
            tracked_files = result.stdout.strip().split('\n') if result.stdout else []
            
            for file_pattern in self.sensitive_files:
                for tracked_file in tracked_files:
                    if file_pattern.replace('*', '') in tracked_file or tracked_file.endswith(file_pattern.replace('*', '')):
                        self.issues.append(f"Sensitive file tracked by git: {tracked_file}")
                        
        except Exception as e:
            self.warnings.append(f"Could not check git status: {e}")
    
    def check_gitignore(self):
        """Check if .gitignore exists and contains essential patterns"""
        gitignore_path = '.gitignore'
        if not os.path.exists(gitignore_path):
            self.issues.append("No .gitignore file found")
            return
        
        essential_patterns = ['.env', '*.key', 'config.py', '*.npy', '*.log']
        
        try:
            with open(gitignore_path, 'r') as f:
                gitignore_content = f.read()
            
            for pattern in essential_patterns:
                if pattern not in gitignore_content:
                    self.warnings.append(f"Pattern '{pattern}' not found in .gitignore")
                    
        except Exception as e:
            self.warnings.append(f"Could not read .gitignore: {e}")
    
    def check_environment_setup(self):
        """Check if environment setup files exist"""
        if not os.path.exists('.env.template'):
            self.warnings.append("No .env.template file found")
        
        if not os.path.exists('config_template.py'):
            self.warnings.append("No config_template.py file found")
        
        if os.path.exists('.env'):
            self.warnings.append(".env file exists - ensure it's not committed to git")
        
        if os.path.exists('config.py'):
            self.warnings.append("config.py file exists - ensure it's not committed to git")
    
    def run_validation(self):
        """Run all security checks"""
        print("🔍 Running security validation...")
        
        # Check all Python files for sensitive patterns (except templates)
        for py_file in Path('.').rglob('*.py'):
            if py_file.name not in ['secure_config.py', 'security_check.py'] and 'template' not in py_file.name:
                self.check_file_content(py_file)
        
        # Check Jupyter notebooks
        for nb_file in Path('.').rglob('*.ipynb'):
            self.check_file_content(nb_file)
        
        # Check git and file system
        self.check_git_status()
        self.check_gitignore()
        self.check_environment_setup()
        
        # Report results
        print("\n📊 Security Validation Results:")
        
        if self.issues:
            print(f"\n❌ {len(self.issues)} Security Issues Found:")
            for issue in self.issues:
                print(f"  • {issue}")
            print("\n⚠️  Please address these issues before committing or deploying!")
        else:
            print("\n✅ No critical security issues found!")
        
        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} Warnings:")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        return len(self.issues) == 0

if __name__ == "__main__":
    validator = SecurityValidator()
    is_secure = validator.run_validation()
    
    if not is_secure:
        print("\n🚨 Security validation failed!")
        sys.exit(1)
    else:
        print("\n🎉 Security validation passed!")
        sys.exit(0)
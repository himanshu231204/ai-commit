#!/usr/bin/env python3
"""
AI Commit - Generate commit messages using local Ollama

Author: Himanshu Kumar
GitHub: https://github.com/himanshu231204/ai-commit
Email: himanshu231204@gmail.com
"""

import json
import subprocess
import sys
import argparse
from typing import Optional
import requests


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = None):
        self.base_url = base_url.rstrip('/')
        self.model = model  # Will be auto-selected if None
    
    def is_available(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def list_models(self) -> list:
        """List available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except requests.exceptions.RequestException:
            return []
    
    def auto_select_model(self) -> Optional[str]:
        """
        Auto-select the best available model.
        Priority: lighter/faster models first for better performance
        """
        available = self.list_models()
        
        if not available:
            return None
        
        # Priority order: lightest/fastest first
        # phi > mistral > codellama > llama2 > llama3 (larger models)
        priority_order = [
            'phi',           # Smallest, fastest
            'mistral',       # Fast and good quality
            'qwen',          # Fast alternative
            'gemma',         # Google's lightweight
            'codellama',     # Good for code
            'llama2',        # Larger but reliable
            'llama3',        # Largest, slowest
        ]
        
        # First, try to match exact priority
        for priority_model in priority_order:
            for available_model in available:
                if available_model.lower().startswith(priority_model):
                    return available_model
        
        # If no match, return first available
        return available[0]
    
    def generate(self, prompt: str) -> Optional[str]:
        """Generate text using Ollama"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120  # Increased to 2 minutes for larger models
            )
            
            if response.status_code == 200:
                return response.json().get('response', '').strip()
            else:
                print(f"{Colors.RED}Ollama returned status {response.status_code}{Colors.END}")
                return None
        except requests.exceptions.Timeout:
            print(f"{Colors.RED}Request timed out. Model '{self.model}' might be too large.{Colors.END}")
            print(f"{Colors.YELLOW}Try using a lighter model like 'phi' or 'mistral'{Colors.END}")
            return None
        except requests.exceptions.ConnectionError:
            print(f"{Colors.RED}Cannot connect to Ollama at {self.base_url}{Colors.END}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"{Colors.RED}Error: {e}{Colors.END}")
            return None


class GitService:
    """Service for Git operations"""
    
    @staticmethod
    def is_git_repo() -> bool:
        """Check if current directory is a git repository"""
        try:
            subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                capture_output=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    
    @staticmethod
    def get_staged_diff() -> Optional[str]:
        """Get diff of staged changes"""
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return None
    
    @staticmethod
    def has_staged_changes() -> bool:
        """Check if there are staged changes"""
        diff = GitService.get_staged_diff()
        return bool(diff and diff.strip())
    
    @staticmethod
    def commit(message: str) -> bool:
        """Create a git commit with the given message"""
        try:
            subprocess.run(
                ['git', 'commit', '-m', message],
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False


class CommitGenerator:
    """Generate commit messages using AI"""
    
    def __init__(self, ollama_client: OllamaClient):
        self.ollama = ollama_client
    
    def generate_message(self, diff: str, style: str = "conventional") -> Optional[str]:
        """Generate a commit message from git diff"""
        
        prompts = {
            "conventional": """You are a git commit message expert. Analyze the following git diff and generate a commit message following the Conventional Commits format.

Rules:
- Use format: <type>(<scope>): <subject>
- Types: feat, fix, docs, style, refactor, test, chore
- Subject should be lowercase, no period at end
- Keep it concise (max 50 characters for subject)
- If needed, add a body explaining what and why (not how)

Git diff:
{diff}

Generate ONLY the commit message, nothing else:""",
            
            "semantic": """You are a git commit message expert. Analyze the following git diff and generate a clear, semantic commit message.

Rules:
- Start with a verb (Add, Update, Fix, Remove, etc.)
- Be specific about what changed
- Keep it concise (max 72 characters)
- Use present tense

Git diff:
{diff}

Generate ONLY the commit message, nothing else:""",
            
            "detailed": """You are a git commit message expert. Analyze the following git diff and generate a detailed commit message.

Rules:
- First line: Brief summary (max 50 chars)
- Blank line
- Body: Explain what and why (not how)
- Use bullet points if multiple changes

Git diff:
{diff}

Generate ONLY the commit message, nothing else:"""
        }
        
        prompt = prompts.get(style, prompts["conventional"]).format(diff=diff[:3000])  # Limit diff size
        
        message = self.ollama.generate(prompt)
        
        if message:
            # Clean up the message
            message = message.strip()
            # Remove any markdown code blocks
            if message.startswith('```'):
                lines = message.split('\n')
                message = '\n'.join(lines[1:-1] if len(lines) > 2 else lines)
            message = message.strip()
        
        return message


def print_banner():
    """Print application banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════╗
║         🤖 AI Commit Message Tool         ║
║      Powered by Local Ollama 🦙           ║
╚═══════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)


def print_diff_summary(diff: str):
    """Print a summary of the diff"""
    lines = diff.split('\n')
    added = sum(1 for line in lines if line.startswith('+') and not line.startswith('+++'))
    removed = sum(1 for line in lines if line.startswith('-') and not line.startswith('---'))
    
    print(f"{Colors.YELLOW}📊 Changes:{Colors.END}")
    print(f"  {Colors.GREEN}+ {added} lines added{Colors.END}")
    print(f"  {Colors.RED}- {removed} lines removed{Colors.END}")
    print()


def get_user_choice(message: str) -> str:
    """Get user input for yes/no questions"""
    while True:
        choice = input(f"{message} {Colors.CYAN}[y/n/r/e]{Colors.END}: ").lower()
        if choice in ['y', 'n', 'r', 'e']:
            return choice
        print(f"{Colors.RED}Invalid choice. Use y (yes), n (no), r (regenerate), or e (edit){Colors.END}")


def main():
    """Main application entry point"""
    print_banner()
    
    # Check if we're in a git repository
    if not GitService.is_git_repo():
        print(f"{Colors.RED}❌ Error: Not a git repository{Colors.END}")
        print(f"{Colors.YELLOW}Please run this command in a git repository{Colors.END}")
        sys.exit(1)
    
    # Check for staged changes
    if not GitService.has_staged_changes():
        print(f"{Colors.YELLOW}⚠️  No staged changes found{Colors.END}")
        print(f"{Colors.CYAN}Please stage your changes first:{Colors.END}")
        print(f"  git add <files>")
        sys.exit(1)
    
    # Initialize Ollama client
    ollama = OllamaClient()
    
    # Check if Ollama is running
    print(f"{Colors.CYAN}🔍 Checking Ollama server...{Colors.END}")
    if not ollama.is_available():
        print(f"{Colors.RED}❌ Error: Cannot connect to Ollama{Colors.END}")
        print(f"{Colors.YELLOW}Please make sure Ollama is running:{Colors.END}")
        print(f"  ollama serve")
        sys.exit(1)
    
    print(f"{Colors.GREEN}✓ Ollama server is running{Colors.END}\n")
    
    # List available models
    available_models = ollama.list_models()
    
    if not available_models:
        print(f"{Colors.RED}❌ No Ollama models found{Colors.END}")
        print(f"{Colors.YELLOW}Please install a model first:{Colors.END}")
        print(f"  ollama pull phi          # Fastest, recommended")
        print(f"  ollama pull mistral      # Good balance")
        print(f"  ollama pull llama2       # Default")
        sys.exit(1)
    
    # Display available models
    print(f"{Colors.CYAN}Available models ({len(available_models)}):{Colors.END}")
    for model in available_models:
        print(f"  • {model}")
    print()
    
    # Auto-select the best (lightest/fastest) model
    selected_model = ollama.auto_select_model()
    if selected_model:
        ollama.model = selected_model
        print(f"{Colors.GREEN}✓ Auto-selected: {Colors.BOLD}{selected_model}{Colors.END}")
        print(f"{Colors.CYAN}  (Prioritizing lighter/faster models){Colors.END}\n")
    else:
        print(f"{Colors.YELLOW}Warning: Could not auto-select model, using first available{Colors.END}\n")
        ollama.model = available_models[0]
    
    # Get staged diff
    diff = GitService.get_staged_diff()
    if not diff:
        print(f"{Colors.RED}❌ Error: Could not get git diff{Colors.END}")
        sys.exit(1)
    
    print_diff_summary(diff)
    
    # Generate commit message
    generator = CommitGenerator(ollama)
    
    print(f"{Colors.CYAN}🤖 Generating commit message...{Colors.END}\n")
    
    while True:
        commit_message = generator.generate_message(diff, style="conventional")
        
        if not commit_message:
            print(f"{Colors.RED}❌ Failed to generate commit message{Colors.END}")
            sys.exit(1)
        
        # Display generated message
        print(f"{Colors.GREEN}{Colors.BOLD}Generated Commit Message:{Colors.END}")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.END}")
        print(f"{Colors.BOLD}{commit_message}{Colors.END}")
        print(f"{Colors.CYAN}{'─' * 50}{Colors.END}\n")
        
        # Ask user what to do
        print(f"{Colors.YELLOW}Options:{Colors.END}")
        print(f"  {Colors.GREEN}y{Colors.END} - Accept and commit")
        print(f"  {Colors.YELLOW}r{Colors.END} - Regenerate message")
        print(f"  {Colors.BLUE}e{Colors.END} - Edit message")
        print(f"  {Colors.RED}n{Colors.END} - Cancel")
        
        choice = get_user_choice("\nWhat would you like to do?")
        
        if choice == 'y':
            # Commit with the generated message
            print(f"\n{Colors.CYAN}📝 Creating commit...{Colors.END}")
            if GitService.commit(commit_message):
                print(f"{Colors.GREEN}✓ Commit created successfully!{Colors.END}")
                sys.exit(0)
            else:
                print(f"{Colors.RED}❌ Failed to create commit{Colors.END}")
                sys.exit(1)
        
        elif choice == 'r':
            # Regenerate
            print(f"\n{Colors.CYAN}🔄 Regenerating...{Colors.END}\n")
            continue
        
        elif choice == 'e':
            # Edit message
            print(f"\n{Colors.CYAN}✏️  Enter your commit message (press Ctrl+D when done):{Colors.END}")
            try:
                lines = []
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                edited_message = '\n'.join(lines).strip()
                if edited_message:
                    if GitService.commit(edited_message):
                        print(f"{Colors.GREEN}✓ Commit created successfully!{Colors.END}")
                        sys.exit(0)
                    else:
                        print(f"{Colors.RED}❌ Failed to create commit{Colors.END}")
                        sys.exit(1)
        
        elif choice == 'n':
            # Cancel
            print(f"\n{Colors.YELLOW}Operation cancelled{Colors.END}")
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Operation cancelled by user{Colors.END}")
        sys.exit(0)

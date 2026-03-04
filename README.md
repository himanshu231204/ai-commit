# 🤖 Ollama Git Commit - AI-Powered Commit Messages

[![PyPI version](https://badge.fury.io/py/ollama-git-commit.svg)](https://pypi.org/project/ollama-git-commit/)
[![Downloads](https://pepy.tech/badge/ollama-git-commit)](https://pepy.tech/project/ollama-git-commit)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/himanshu231204/ai-commit?style=social)](https://github.com/himanshu231204/ai-commit)

Generate intelligent git commit messages using your local Ollama instance. No API keys, completely free, and runs offline!

---

## ✨ Features

- 🤖 **AI-Powered**: Uses local Ollama models to generate commit messages
- 🔒 **Privacy First**: Everything runs locally, no data sent to external APIs
- 🎯 **Multiple Styles**: Conventional commits, semantic, or detailed formats
- 💰 **Free**: No API costs, uses your local Ollama instance
- ⚡ **Fast**: Quick generation with local models
- 🎨 **Interactive**: Review, regenerate, or edit messages before committing
- 🌐 **Offline**: Works completely offline

---

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install ollama-git-commit
```

### From Source

```bash
git clone https://github.com/himanshu231204/ai-commit.git
cd ai-commit
pip install -e .
```

---

## 📋 Prerequisites

Before using Ollama Git Commit, you need:

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **Git**
   ```bash
   git --version
   ```

3. **Ollama** - [Install Ollama](https://ollama.ai)
   ```bash
   # Install Ollama (macOS/Linux)
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull a model (e.g., llama2)
   ollama pull llama2
   
   # Start Ollama server
   ollama serve
   ```

---

## 💡 Usage

### Basic Usage

1. **Stage your changes**:
   ```bash
   git add .
   ```

2. **Generate commit message**:
   ```bash
   ai-commit
   ```

3. **Review and choose**:
   - `y` - Accept and commit
   - `r` - Regenerate message
   - `e` - Edit message manually
   - `n` - Cancel

### Example Workflow

```bash
# Make some changes to your code
echo "print('Hello World')" > hello.py

# Stage the changes
git add hello.py

# Generate AI commit message
ai-commit

# Output:
╔═══════════════════════════════════════════╗
║         🤖 AI Commit Message Tool         ║
║      Powered by Local Ollama 🦙           ║
╚═══════════════════════════════════════════╝

🔍 Checking Ollama server...
✓ Ollama server is running

📊 Changes:
  + 1 lines added
  - 0 lines removed

🤖 Generating commit message...

Generated Commit Message:
──────────────────────────────────────────────────
feat: add hello world script
──────────────────────────────────────────────────

Options:
  y - Accept and commit
  r - Regenerate message
  e - Edit message
  n - Cancel
```

---

## ⚙️ Configuration

### Custom Ollama Server

If your Ollama server is running on a different host/port, edit `ai_commit.py`:

```python
ollama = OllamaClient(base_url="http://192.168.1.100:11434")
```

### Change AI Model

```python
ollama = OllamaClient(model="codellama")  # or "mistral", "llama2", etc.
```

### Commit Message Styles

The tool supports three commit message styles:

1. **Conventional Commits** (default):
   ```
   feat(auth): add user login functionality
   ```

2. **Semantic**:
   ```
   Add user login functionality
   ```

3. **Detailed**:
   ```
   Add user authentication system
   
   - Implement JWT-based authentication
   - Add login and logout endpoints
   - Create user session management
   ```

---

## 🎨 Supported Ollama Models

Any Ollama model works, but these are recommended:

- **llama2** - Best overall performance
- **codellama** - Optimized for code
- **mistral** - Fast and efficient
- **phi** - Lightweight option
- **llama3** - Latest and most powerful

```bash
# Pull and use different models
ollama pull codellama
ollama pull mistral
ollama pull phi
```

---

## 📝 Examples

### Example 1: Adding a New Feature

```bash
$ git add new_feature.py
$ ai-commit

Generated: feat: add user profile management feature
```

### Example 2: Bug Fix

```bash
$ git add bug_fix.py
$ ai-commit

Generated: fix: resolve null pointer exception in login
```

### Example 3: Documentation

```bash
$ git add README.md
$ ai-commit

Generated: docs: update installation instructions
```

---

## 🐛 Troubleshooting

### Ollama Not Running
```
Error: Cannot connect to Ollama
Solution: Start Ollama server with `ollama serve`
```

### No Staged Changes
```
Error: No staged changes found
Solution: Stage your changes with `git add <files>`
```

### Model Not Found
```
Error: Model not found
Solution: Pull the model with `ollama pull llama2`
```

---

## 🤝 Contributing

Contributions are what make the open-source community amazing! Any contributions you make are **greatly appreciated**.

### How to Contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (when available)
5. Commit using ai-commit! 😄
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Ollama** - For making local LLMs accessible
- **Git** - The best version control system
- **Python** - For being awesome
- **You** - For using this tool!

---

## 🗺️ Roadmap

- [x] Initial release on PyPI
- [ ] Configuration file support (`.ai-commit.yml`)
- [ ] More commit message formats
- [ ] Interactive model selection
- [ ] Emoji support in commits 🎉
- [ ] Multiple language support
- [ ] Git hooks integration
- [ ] VSCode extension
- [ ] Custom prompt templates
- [ ] Commit message history
- [ ] Auto-detect commit type from files
- [ ] Batch commit support
- [ ] Integration with GitHub CLI

---

## 👨‍💻 Author

**Himanshu Kumar**

- 🌐 GitHub: [@himanshu231204](https://github.com/himanshu231204)
- 💼 LinkedIn: [himanshu231204](https://www.linkedin.com/in/himanshu231204)
- 🐦 Twitter/X: [@himanshu231204](https://twitter.com/himanshu231204)
- 📧 Email: himanshu231204@gmail.com

---

## 💖 Support

If you find this project helpful, please consider:

- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 🔀 Contributing code
- ☕ [Buy me a coffee](https://www.buymeacoffee.com/himanshu231204)
- 💝 [Sponsor on GitHub](https://github.com/sponsors/himanshu231204)

---

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/himanshu231204/ai-commit?style=social)
![GitHub forks](https://img.shields.io/github/forks/himanshu231204/ai-commit?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/himanshu231204/ai-commit?style=social)
![PyPI downloads](https://img.shields.io/pypi/dm/ollama-git-commit)

---

## 🔗 Links

- **PyPI Package**: https://pypi.org/project/ollama-git-commit/
- **Documentation**: [GitHub Wiki](https://github.com/himanshu231204/ai-commit/wiki)
- **Issues**: [GitHub Issues](https://github.com/himanshu231204/ai-commit/issues)
- **Discussions**: [GitHub Discussions](https://github.com/himanshu231204/ai-commit/discussions)
- **Releases**: [GitHub Releases](https://github.com/himanshu231204/ai-commit/releases)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=himanshu231204/ai-commit&type=Date)](https://star-history.com/#himanshu231204/ai-commit&Date)

---

## 📣 Show Your Support

Give a ⭐️ if this project helped you!

---

**Made with ❤️ by [Himanshu Kumar](https://github.com/himanshu231204)**

---

## 🚀 Quick Links

| Resource | Link |
|----------|------|
| 📦 **Install** | `pip install ollama-git-commit` |
| 📖 **Docs** | [GitHub](https://github.com/himanshu231204/ai-commit) |
| 🐛 **Issues** | [Report Bug](https://github.com/himanshu231204/ai-commit/issues/new?template=bug_report.md) |
| 💡 **Feature Request** | [Request Feature](https://github.com/himanshu231204/ai-commit/issues/new?template=feature_request.md) |
| 💬 **Discussions** | [Join Discussion](https://github.com/himanshu231204/ai-commit/discussions) |
| ⭐ **Star** | [Star on GitHub](https://github.com/himanshu231204/ai-commit) |

---


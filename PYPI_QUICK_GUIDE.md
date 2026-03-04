# 🚀 Quick PyPI Publishing Guide

## Step 1: Setup (One Time)

### Create Accounts
1. **PyPI**: https://pypi.org/account/register/
2. **TestPyPI**: https://test.pypi.org/account/register/

### Create API Tokens
1. Go to https://pypi.org/manage/account/
2. Click "Add API token"
3. Name: "ai-commit"
4. Copy token (starts with `pypi-`)

### Configure Credentials
```bash
cat > ~/.pypirc << 'EOF'
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-TOKEN-HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR-TESTPYPI-TOKEN-HERE
EOF

chmod 600 ~/.pypirc
```

---

## Step 2: Publish (Every Release)

### Quick Method (Use Script)
```bash
bash publish.sh
```

### Manual Method
```bash
# Install tools
pip install build twine

# Build
python3 -m build

# Check
twine check dist/*

# Upload to TestPyPI (test first!)
twine upload -r testpypi dist/*

# Test install
pip install --index-url https://test.pypi.org/simple/ollama-git-commit
pip install requests

# Upload to PyPI
twine upload dist/*
```

---

## Step 3: After Publishing

### Update README
```markdown
## Installation

```bash
pip install ollama-git-commit
```
```

### Create GitHub Release
```bash
git tag -a v0.1.0 -m "Initial release"
git push origin v0.1.0
```

---

## Version Updates

When releasing new version:

1. **Update version** in `setup.py` AND `pyproject.toml`
2. **Update** `CHANGELOG.md`
3. **Clean & rebuild**: `rm -rf dist/ build/; python3 -m build`
4. **Upload**: `twine upload dist/*`

---

## Troubleshooting

### "Package name exists"
Change `name="ollama-git-commit"` to something else in both files

### "Invalid credentials"
Check API token in `~/.pypirc`

### "File already exists"
Cannot re-upload same version - increment version number

---

## Links

- **PyPI**: https://pypi.org/project/ollama-git-commit/
- **TestPyPI**: https://test.pypi.org/project/ollama-git-commit/
- **Downloads**: https://pepy.tech/project/ollama-git-commit/

---

Done! Users can now install with: `pip install ollama-git-commit` 🎉

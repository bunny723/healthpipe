# Contributing to HealthPipe

Thank you for your interest in contributing to HealthPipe! We're building a community-driven solution to improve healthcare data quality for AI applications.

## 🌟 How You Can Help

- **Report Issues**: Found a bug or have a feature request? [Open an issue](https://github.com/praveenpolisetty/healthpipe/issues)
- **Submit PRs**: Have a fix or improvement? We welcome pull requests!
- **Add Validators**: Contribute clinical validation rules for your specialty
- **Documentation**: Help improve our docs or add examples
- **Testing**: Add test cases or test on your healthcare data

## 🏃 Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-improvement`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing improvement'`)
6. Push to the branch (`git push origin feature/amazing-improvement`)
7. Open a Pull Request

## 💻 Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/healthpipe.git
cd healthpipe

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
flake8 src/
black src/ --check
```

## 📝 Code Style

- We use [Black](https://github.com/psf/black) for code formatting
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Write docstrings for all public functions
- Add type hints where possible

## 🧪 Testing

- Write tests for new features
- Maintain or improve code coverage
- Test with both pandas and Spark DataFrames
- Include edge cases

## 📊 Adding Clinical Validators

Healthcare professionals can contribute domain expertise by adding clinical validation rules:

1. Create a new file in `src/healthpipe/validators/clinical/`
2. Define validation rules for your specialty
3. Include references to clinical guidelines
4. Add tests with realistic scenarios

Example:
```python
# src/healthpipe/validators/clinical/cardiology.py
BLOOD_PRESSURE_RANGES = {
    "systolic": {"min": 70, "max": 190},
    "diastolic": {"min": 40, "max": 120}
}
```

## 🏥 Healthcare Standards

When contributing:
- Ensure HIPAA compliance
- Follow FHIR R4 standards
- Reference clinical guidelines
- Consider international variations

## 📚 Documentation

- Update README.md if adding features
- Add docstrings with examples
- Include clinical context where relevant
- Update API documentation

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Remember we're working to improve healthcare

## 📄 License

By contributing, you agree that your contributions will be licensed under the Apache 2.0 License.

## 🙏 Recognition

Contributors will be recognized in:
- GitHub contributors page
- Project documentation
- Research papers (for significant contributions)

## ❓ Questions?

- Open a [discussion](https://github.com/praveenpolisetty/healthpipe/discussions)
- Email: praveen.polisetty2123@gmail.com

Thank you for helping improve healthcare data quality! 🏥💪
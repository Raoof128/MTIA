# Contributing to Multimodal Threat Intelligence AI

Thank you for your interest in contributing to the Multimodal Threat Intelligence AI project! We welcome contributions from the community to help improve this educational threat detection system.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

1.  **Fork the Repository**: Click the "Fork" button on the top right of the repository page.
2.  **Clone the Repository**: Clone your forked repository to your local machine.
    ```bash
    git clone https://github.com/Raoof128/MTIA.git
    ```
3.  **Create a Branch**: Create a new branch for your feature or bug fix.
    ```bash
    git checkout -b feature/your-feature-name
    ```
4.  **Make Changes**: Implement your changes, ensuring you follow the coding standards and add comments where necessary.
5.  **Run Tests**: Run the test suite to ensure your changes didn't break anything.
    ```bash
    make test
    ```
6.  **Commit Changes**: Commit your changes with a descriptive commit message.
    ```bash
    git commit -m "Add feature: your feature description"
    ```
7.  **Push to GitHub**: Push your branch to your forked repository.
    ```bash
    git push origin feature/your-feature-name
    ```
8.  **Submit a Pull Request**: Go to the original repository and submit a Pull Request (PR) from your forked branch.

## Coding Standards

*   **Python**: Follow PEP 8 style guidelines. Use type hints for all function signatures.
*   **JavaScript**: Use modern ES6+ syntax.
*   **Documentation**: Update README.md and add docstrings for new code.
*   **Testing**: Add unit tests for new features using `pytest`.
*   **Linting**: Ensure code passes `make lint` (flake8, mypy) and `make format` (black, isort).

## Reporting Issues

If you find a bug or have a feature request, please open an issue on the GitHub repository. Provide as much detail as possible, including steps to reproduce the issue.

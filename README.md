# 🏛️ OmniScope - Web Analysis Engine

**OmniScope** is a lightweight, portable, and single-command web analysis engine that evaluates any website across **6 engineering dimensions**. Designed with a "zero-configuration" philosophy, it turns your local machine into a standalone analysis tool—no cloud dependencies, no bloated files.

> 🎯 **Slogan:** *"Your machine, your private analysis tower."*

---

## 📋 Table of Contents

1. [Features](#-features)
2. [Requirements](#-requirements)
3. [Installation](#-installation)
4. [Execution Methods](#-execution-methods)
   - [CLI (Command Line Interface)](#-method-1-cli-command-line-interface---recommended)
   - [API Server (Optional)](#-method-2-api-server-mode-optional)
5. [How It Works (Technical Flow)](#-how-it-works-technical-flow)
6. [Sample Output](#-sample-output)
7. [Project Structure](#-project-structure)
8. [Security Policies](#-security-policies)
9. [Troubleshooting](#-troubleshooting)
10. [Roadmap](#-roadmap)
11. [License](#-license)

---

## ✨ Features

| Dimension | Description | Key Metrics |
| :--- | :--- | :--- |
| ⚡ **Performance** | Page loading speed and weight | TTFB, Total Size (KB), Gzip compression |
| 🔒 **Security** | Headers and SSL/TLS health | SSL validity, HSTS, X-Frame-Options, X-Content-Type |
| 📈 **SEO** | Search engine optimization basics | Title (length), Meta Description, H1 tags |
| ♿ **Accessibility (A11Y)** | Inclusive web standards | Image Alt attributes, HTML Lang, ARIA labels |
| 🧹 **Best Practices** | Modern web coding standards | Doctype, Charset, Inline CSS/JS count |
| 🌿 **Eco-Score** | Environmental impact simulation | Estimated CO₂ emissions, page size |

---

## 📦 Requirements

- **Python 3.11** or higher
- Internet connection (for analysis and initial setup)
- OS: Windows / macOS / Linux (fully platform-independent)

---

## ⚙️ Installation

Clone or download the project files, then run the automated setup:

```bash
python setup.py

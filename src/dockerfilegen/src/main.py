import os
import subprocess
import re

PROJECT_PATH = "/project"
IMAGE_NAME = "my_project"

def extract_imports():
    """Scans project files and extracts dependencies dynamically."""
    python_imports = set()
    js_imports = set()
    go_imports = set()
    rust_imports = set()
    ruby_imports = set()
    php_imports = set()
    java_imports = set()
    csharp_imports = set()
    elixir_imports = set()
    haskell_imports = set()
    perl_imports = set()
    html_files = []
    css_files = []

    for root, _, files in os.walk(PROJECT_PATH):
        for file in files:
            file_path = os.path.join(root, file)

            # Extract Python imports
            if file.endswith(".py"):
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        match = re.match(r"^\s*(?:import|from)\s+([\w\.]+)", line)
                        if match:
                            python_imports.add(match.group(1).split('.')[0])

            # Extract JavaScript imports
            elif file.endswith(".js"):
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        match = re.match(r".*require\(['\"]([\w\-]+)['\"]\)", line) or \
                                re.match(r".*import\s+.*\s+from\s+['\"]([\w\-]+)['\"]", line)
                        if match:
                            js_imports.add(match.group(1))

            # Extract Go imports
            elif file.endswith(".go"):
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        match = re.match(r"^\s*import\s+[\"`]([\w\/\-]+)[\"`]", line)
                        if match:
                            go_imports.add(match.group(1))

            # Extract Rust dependencies (Cargo.toml)
            elif file.endswith("Cargo.toml"):
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        match = re.match(r"^\s*([\w\-]+)\s*=\s*\"[\d\.]+\"", line)
                        if match:
                            rust_imports.add(match.group(1))

            # Extract Ruby dependencies (Gemfile)
            elif file.endswith("Gemfile"):
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        match = re.match(r"^\s*gem\s+[\"']([\w\-]+)[\"']", line)
                        if match:
                            ruby_imports.add(match.group(1))

            # Extract PHP dependencies (composer.json)
            elif file.endswith("composer.json"):
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        match = re.search(r"\"([\w\-]+)\":\s*\"[\d\.]+\"", line)
                        if match:
                            php_imports.add(match.group(1))

            # Extract Java dependencies (pom.xml or build.gradle)
            elif file.endswith("pom.xml") or file.endswith("build.gradle"):
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        match = re.match(r"^\s*<dependency>\s*<groupId>([\w\.\-]+)</groupId>", line)
                        if match:
                            java_imports.add(match.group(1))

            # Extract C# dependencies (.csproj or project.json)
            elif file.endswith(".csproj") or file.endswith("project.json"):
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        match = re.match(r"^\s*<PackageReference\s+Include=\"([\w\.\-]+)\"", line)
                        if match:
                            csharp_imports.add(match.group(1))

            # Extract Elixir dependencies (mix.exs)
            elif file.endswith("mix.exs"):
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        match = re.match(r"^\s*{:([\w\-]+),", line)
                        if match:
                            elixir_imports.add(match.group(1))

            # Extract Haskell dependencies (.cabal)
            elif file.endswith(".cabal"):
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        match = re.match(r"^\s*build-depends:\s*([\w\-]+)", line)
                        if match:
                            haskell_imports.add(match.group(1))

            # Extract Perl dependencies (cpanfile or Makefile.PL)
            elif file.endswith("cpanfile") or file.endswith("Makefile.PL"):
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        match = re.match(r"^\s*requires\s+['\"]([\w\-]+)['\"]", line)
                        if match:
                            perl_imports.add(match.group(1))

            # Detect HTML and CSS files
            elif file.endswith(".html") or file.endswith(".htm"):
                html_files.append(file_path)
            elif file.endswith(".css"):
                css_files.append(file_path)

    return python_imports, js_imports, go_imports, rust_imports, ruby_imports, php_imports, java_imports, csharp_imports, elixir_imports, haskell_imports, perl_imports, html_files, css_files

def detect_language_and_framework(imports, html_files, css_files):
    """Detects the programming language and framework based on extracted imports."""
    language = None
    framework = None

    if imports[0]:  # Python imports
        language = "python"
        if "flask" in imports[0]:
            framework = "flask"
        elif "django" in imports[0]:
            framework = "django"

    elif imports[1]:  # JavaScript imports
        language = "node"
        if "express" in imports[1]:
            framework = "express"

    elif imports[2]:  # Go imports
        language = "go"

    elif imports[3]:  # Rust imports
        language = "rust"

    elif imports[4]:  # Ruby imports
        language = "ruby"

    elif imports[5]:  # PHP imports
        language = "php"

    elif imports[6]:  # Java imports
        language = "java"

    elif imports[7]:  # C# imports
        language = "csharp"

    elif imports[8]:  # Elixir imports
        language = "elixir"

    elif imports[9]:  # Haskell imports
        language = "haskell"

    elif imports[10]:  # Perl imports
        language = "perl"

    elif html_files or css_files:  # HTML or CSS files detected
        language = "html"
        framework = "nginx"

    return language, framework

def generate_dockerfile(language, framework, imports, html_files, css_files):
    """Generates an optimized Dockerfile based on detected language and dependencies."""
    dockerfile_lines = []

    if language == "python":
        dockerfile_lines.append("FROM python:3.9-slim")
        dockerfile_lines.append("WORKDIR /app")
        dockerfile_lines.append("COPY . .")
        if imports[0]:
            dockerfile_lines.append("RUN pip install --no-cache-dir " + " ".join(imports[0]))
        if framework == "flask":
            dockerfile_lines.append('CMD ["python", "app.py"]')
        elif framework == "django":
            dockerfile_lines.append('CMD ["gunicorn", "-b", "0.0.0.0:8000", "project.wsgi:application"]')
        else:
            dockerfile_lines.append('CMD ["python", "main.py"]')

    elif language == "node":
        dockerfile_lines.append("FROM node:18-alpine")
        dockerfile_lines.append("WORKDIR /app")
        dockerfile_lines.append("COPY . .")
        if imports[1]:
            dockerfile_lines.append("RUN npm install " + " ".join(imports[1]))
        dockerfile_lines.append('CMD ["node", "server.js"]')

    elif language == "go":
        dockerfile_lines.append("FROM golang:1.18-alpine")
        dockerfile_lines.append("WORKDIR /app")
        dockerfile_lines.append("COPY . .")
        if imports[2]:
            dockerfile_lines.append("RUN go get " + " ".join(imports[2]))
        dockerfile_lines.append("RUN go build -o main .")
        dockerfile_lines.append('CMD ["./main"]')

    elif language == "rust":
        dockerfile_lines.append("FROM rust:latest")
        dockerfile_lines.append("WORKDIR /app")
        dockerfile_lines.append("COPY . .")
        dockerfile_lines.append("RUN cargo build --release")
        dockerfile_lines.append('CMD ["./target/release/app"]')

    elif language == "ruby":
        dockerfile_lines.append("FROM ruby:latest")
        dockerfile_lines.append("WORKDIR /app")
        dockerfile_lines.append("COPY . .")
        if imports[4]:
            dockerfile_lines.append("RUN gem install " + " ".join(imports[4]))
        dockerfile_lines.append('CMD ["ruby", "app.rb"]')

    elif language == "php":
        dockerfile_lines.append("FROM php:8.0-apache")
        dockerfile_lines.append("WORKDIR /var/www/html")
        dockerfile_lines.append("COPY . .")
        if imports[5]:
            dockerfile_lines.append("RUN composer require " + " ".join(imports[5]))
        dockerfile_lines.append('CMD ["apache2-foreground"]')

    elif language == "java":
        dockerfile_lines.append("FROM openjdk:11-jdk-slim")
        dockerfile_lines.append("WORKDIR /app")
        dockerfile_lines.append("COPY . .")
        if imports[6]:
            dockerfile_lines.append("RUN mvn install " + " ".join(imports[6]))
        dockerfile_lines.append('CMD ["java", "-jar", "app.jar"]')

    elif language == "csharp":
        dockerfile_lines.append("FROM mcr.microsoft.com/dotnet/core/sdk:3.1")
        dockerfile_lines.append("WORKDIR /app")
        dockerfile_lines.append("COPY . .")
        if imports[7]:
            dockerfile_lines.append("RUN dotnet restore " + " ".join(imports[7]))
        dockerfile_lines.append('CMD ["dotnet", "run"]')

    elif language == "elixir":
        dockerfile_lines.append("FROM elixir:latest")
        dockerfile_lines.append("WORKDIR /app")
        dockerfile_lines.append("COPY . .")
        if imports[8]:
            dockerfile_lines.append("RUN mix deps.get " + " ".join(imports[8]))
        dockerfile_lines.append('CMD ["mix", "phx.server"]')

    elif language == "html":
        dockerfile_lines.append("FROM nginx:alpine")
        dockerfile_lines.append("COPY . /usr/share/nginx/html")
        dockerfile_lines.append("EXPOSE 80")
        dockerfile_lines.append('CMD ["nginx", "-g", "daemon off;"]')

    dockerfile_lines.append("EXPOSE 80")

    # Write the Dockerfile to a file
    with open('Dockerfile', 'w') as f:
        for line in dockerfile_lines:
            f.write(line + "\n")
 
    print("Dockerfile generated successfully!")

def build_and_transfer():
    """Builds the Docker image, runs the container, and transfers output files to the host."""
    print("Building Docker image...")
    subprocess.run(["docker", "build", "-t", IMAGE_NAME, "."], check=True)

    print("Running Docker container...")
    container_id = subprocess.check_output(["docker", "run", "-d", IMAGE_NAME]).decode().strip()

    print("Copying output files from container to host...")
    os.makedirs("output", exist_ok=True)
    subprocess.run(["docker", "cp", f"{container_id}:/app/output", "output"], check=True)

    print("Stopping and removing container...")
    subprocess.run(["docker", "stop", container_id], check=True)
    subprocess.run(["docker", "rm", container_id], check=True)

    print("Process completed successfully!")

# Example usage:
imports, html_files, css_files = extract_imports()
language, framework = detect_language_and_framework(imports, html_files, css_files)
generate_dockerfile(language, framework, imports, html_files, css_files)
build_and_transfer()

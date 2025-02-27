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
    web_files = set()

    for root, _, files in os.walk(PROJECT_PATH):
        for file in files:
            file_path = os.path.join(root, file)

            # Extract imports logic...

    return (
        python_imports, js_imports, go_imports, rust_imports, ruby_imports,
        php_imports, java_imports, csharp_imports, elixir_imports, haskell_imports,
        perl_imports, web_files
    )

def detect_language_and_framework(imports):
    """Detects the programming language and framework based on extracted imports."""
    language = None
    framework = None

    # Check each language's imports (adjusted for the actual number of elements in the imports tuple)
    if len(imports) > 0 and imports[0]:  # Python imports
        language = "Python"
        framework = "Flask" if "flask" in imports[0] else "Django" if "django" in imports[0] else "None"
    elif len(imports) > 1 and imports[1]:  # JavaScript imports
        language = "JavaScript"
        framework = "React" if "react" in imports[1] else "Node.js" if "express" in imports[1] else "None"
    elif len(imports) > 2 and imports[2]:  # Go imports
        language = "Go"
    elif len(imports) > 3 and imports[3]:  # Rust imports
        language = "Rust"
    elif len(imports) > 4 and imports[4]:  # Ruby imports
        language = "Ruby"
        framework = "Rails" if "rails" in imports[4] else "None"
    elif len(imports) > 5 and imports[5]:  # PHP imports
        language = "PHP"
        framework = "Laravel" if "laravel" in imports[5] else "None"
    elif len(imports) > 6 and imports[6]:  # Java imports
        language = "Java"
        framework = "Spring" if "spring" in imports[6] else "None"
    elif len(imports) > 7 and imports[7]:  # C# imports
        language = "C#"
        framework = "ASP.NET" if "asp.net" in imports[7] else "None"
    elif len(imports) > 8 and imports[8]:  # Elixir imports
        language = "Elixir"
        framework = "Phoenix" if "phoenix" in imports[8] else "None"
    elif len(imports) > 9 and imports[9]:  # Haskell imports
        language = "Haskell"
    elif len(imports) > 10 and imports[10]:  # Perl imports
        language = "Perl"
    elif len(imports) > 11 and imports[11]:  # HTML or CSS files detected
        language = "Web"

    if language is None:  # Fallback to "Web" if nothing is detected
        language = "Web"

    return language, framework

def generate_dockerfile(language, framework):
    """Generates a Dockerfile based on the detected language and framework."""
    dockerfile_content = ""

    if language == "Python":
        dockerfile_content += "FROM python:3.8-slim\n"
        if framework == "Flask":
            dockerfile_content += "RUN pip install flask\n"
        elif framework == "Django":
            dockerfile_content += "RUN pip install django\n"
    elif language == "JavaScript":
        dockerfile_content += "FROM node:14\n"
        if framework == "React":
            dockerfile_content += "RUN npm install react\n"
        elif framework == "Node.js":
            dockerfile_content += "RUN npm install express\n"
    elif language == "Web":
        dockerfile_content += "FROM nginx:alpine\n"
        dockerfile_content += "COPY . /usr/share/nginx/html\n"
        dockerfile_content += "EXPOSE 80\n"
    else:
        dockerfile_content += "FROM ubuntu:20.04\n"

    dockerfile_content += 'CMD ["nginx", "-g", "daemon off;"] \n'
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
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
all_imports = extract_imports()
html_files = all_imports[-2]  # Second last item in returned tuple
css_files = all_imports[-1]   # Last item in returned tuple
imports = all_imports[:-2]  # Everything except the last two items

language, framework = detect_language_and_framework(imports)
generate_dockerfile(language, framework)
#build_and_transfer()

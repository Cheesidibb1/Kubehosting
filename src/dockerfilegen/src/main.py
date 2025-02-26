import os
import subprocess

PROJECT_PATH = "/project"  # The path inside the container where the project is mounted

def analyze_project():
    """Detects the project type and returns a Dockerfile"""
    if os.path.exists(os.path.join(PROJECT_PATH, "requirements.txt")) or os.path.exists(os.path.join(PROJECT_PATH, "pyproject.toml")):
        return generate_python_dockerfile()
    elif os.path.exists(os.path.join(PROJECT_PATH, "package.json")):
        return generate_node_dockerfile()
    elif os.path.exists(os.path.join(PROJECT_PATH, "pom.xml")) or os.path.exists(os.path.join(PROJECT_PATH, "build.gradle")):
        return generate_java_dockerfile()
    elif os.path.exists(os.path.join(PROJECT_PATH, "go.mod")):
        return generate_go_dockerfile()
    elif os.path.exists(os.path.join(PROJECT_PATH, "Cargo.toml")):
        return generate_rust_dockerfile()
    else:
        raise ValueError("Unsupported project type. No recognized dependency files found.")

def generate_python_dockerfile():
    return [
        "FROM python:3.9-slim",
        "WORKDIR /app",
        "COPY . .",
        "RUN pip install --no-cache-dir -r requirements.txt" if os.path.exists(os.path.join(PROJECT_PATH, "requirements.txt")) else "RUN pip install poetry && poetry install",
        'CMD ["python", "app.py"]'
    ]

def generate_node_dockerfile():
    return [
        "FROM node:18",
        "WORKDIR /app",
        "COPY package*.json ./",
        "RUN npm install",
        "COPY . .",
        'CMD ["npm", "start"]'
    ]

def generate_java_dockerfile():
    dockerfile = [
        "FROM openjdk:17",
        "WORKDIR /app",
        "COPY . .",
    ]
    if os.path.exists(os.path.join(PROJECT_PATH, "pom.xml")):
        dockerfile.append("RUN mvn package")
        dockerfile.append('CMD ["java", "-jar", "target/myapp.jar"]')
    elif os.path.exists(os.path.join(PROJECT_PATH, "build.gradle")):
        dockerfile.append("RUN ./gradlew build")
        dockerfile.append('CMD ["java", "-jar", "build/libs/myapp.jar"]')
    return dockerfile

def generate_go_dockerfile():
    return [
        "FROM golang:1.20",
        "WORKDIR /app",
        "COPY . .",
        "RUN go build -o myapp",
        'CMD ["./myapp"]'
    ]

def generate_rust_dockerfile():
    return [
        "FROM rust:1.71",
        "WORKDIR /app",
        "COPY . .",
        "RUN cargo build --release",
        'CMD ["./target/release/myapp"]'
    ]

def save_dockerfile(dockerfile_lines):
    """Saves the Dockerfile inside the mounted project"""
    dockerfile_path = os.path.join(PROJECT_PATH, "Dockerfile")
    with open(dockerfile_path, "w") as file:
        file.write("\n".join(dockerfile_lines))
    print(f"Dockerfile generated at: {dockerfile_path}")

def build_docker_image():
    """Builds the Docker image using Docker-in-Docker"""
    try:
        image_name = "my_project"
        subprocess.run(["docker", "build", "-t", image_name, PROJECT_PATH], check=True)
        print(f"Docker image '{image_name}' built successfully!")
    except subprocess.CalledProcessError as e:
        print("Error during Docker build:", e)
def transfer_docker_image():
    """Transfers the built image from the container to the host without saving a tar file."""
    image_name = "my_project"
    try:
        # Save and transfer the image in a live stream
        subprocess.run(
            "docker save my_project | docker exec -i $(docker ps -qf 'name=host-container-name') docker load",
            shell=True,
            check=True
        )
        print(f"Docker image '{image_name}' transferred to the host!")
    except subprocess.CalledProcessError as e:
        print("Error transferring Docker image:", e)

if __name__ == "__main__":
    try:
        dockerfile_lines = analyze_project()
        save_dockerfile(dockerfile_lines)
        build_docker_image()
        transfer_docker_image()  # Automate the transfer step
    except ValueError as e:
        print("Error:", e)

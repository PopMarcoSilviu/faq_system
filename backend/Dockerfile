FROM continuumio/miniconda3

WORKDIR /backend_app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy everything
COPY . /backend_app
RUN echo "Files copied into image"

# Create environment
RUN echo "Starting conda env create..." && \
    conda env create -f environment.yml && \
    echo "Conda environment created"

EXPOSE 8000

WORKDIR /backend_app/src
CMD ["conda", "run", "-n", "semantic-faq-assistant", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

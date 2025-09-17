FROM continuumio/miniconda3

WORKDIR /backend_app
COPY . /backend_app
RUN conda env create -f environment.yml
EXPOSE 8000

WORKDIR /backend_app/src
CMD ["conda", "run", "-n", "semantic-faq-assistant", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
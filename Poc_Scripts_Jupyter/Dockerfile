FROM quay.io/jupyter/base-notebook
# Impede o Python de escrever ficheiros pyc para o disco (equivalente à opção python -B)
ENV PYTHONDONTWRITEBYTECODE 1
# assegura que a saída Python é enviada diretamente para o terminal sem a colocar em buffer primeiro
ENV PYTHONUNBUFFERED 1

WORKDIR /home/jovyan/work

# Permitir que o utilizador jovyan escreva na pasta work
USER jovyan

RUN mkdir /home/jovyan/work/src/

RUN chmod 777 /home/jovyan/work/src/

RUN pip install requests feature_engine

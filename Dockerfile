FROM postgres
ARG WORK_DIR
WORKDIR $WORK_DIR/data/sql
RUN service postgresql start
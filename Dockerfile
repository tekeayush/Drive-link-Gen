FROM ubuntu:latest
COPY . .
RUN apt -qq update && apt-get install -y --no-install-recommends python3 python3-pip git wget
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["bash","start.sh"]

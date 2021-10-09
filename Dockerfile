# python:alpine is 3.{latest}
FROM python:alpine

LABEL maintainer="zhaoshengchong@gmail.com"
RUN pip install flask ldap3 pymysql
ADD . /app/ 
WORKDIR /app
EXPOSE 80

CMD ["python", "/app/app.py"]

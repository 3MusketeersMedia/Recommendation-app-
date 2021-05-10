FROM node:14

WORKDIR /usr/src/app

COPY . . 

RUN npm install  

CMD HOST=0.0.0.0 npm run start & HOST=0.0.0.0 npm run server
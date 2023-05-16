FROM node
WORKDIR /new-app
COPY package.json .
RUN npm install
RUN npm install react-router-dom -S
RUN npm install axios -S
COPY . .
EXPOSE 3000
CMD [ "npm", "start" ]

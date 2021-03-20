FROM node:14

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY ./app/package*.json /app/

WORKDIR /app

RUN npm install
# If you are building your code for production
# RUN npm ci --only=production

COPY ./app /app

EXPOSE 8080

# Start the server
CMD [ "node", "server.js" ]
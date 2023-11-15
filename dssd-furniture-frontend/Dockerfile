# Use the official Node.js image as the base image
FROM node:latest

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . .

# Build the Vue.js app
RUN npm run build

# Expose the port your app runs on
EXPOSE 3000

# Start the app with --host 0.0.0.0 to make it externally accessible
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
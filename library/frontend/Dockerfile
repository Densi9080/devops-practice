from node:20-slim
copy . /frontend
run npm install
workdir /frontend
expose 5173
cmd ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
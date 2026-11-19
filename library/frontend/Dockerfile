from node:20-slim
copy . /frontend
workdir /frontend
run npm install
expose 5173
cmd ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
You need 3 terminal windows running at the same time. 
# Terminal 1: Ollama (The AI Brain)
What it does: Runs the local AI model that answers questions and summarizes documents
How to start:  
bash  
ollama serve  

What you'll see: Messages about the server starting Leave it running! Don't close this window

# Terminal 2: Backend (The Middleman) 🔧
What it does: Receives files from your website, detects PII, talks to Ollama, sends results back.  
How to start:  
bash  
export PATH="/usr/local/bin:$PATH"  
cd ~/clairos/pii-demo-project/backend  
uvicorn server:app --reload --port 8000  
What you'll see: "Uvicorn running on http://127.0.0.1:8000" Leave it running! Don't close this window

# Terminal 3: Frontend (The Website)
What it does: Shows the pretty interface you see in your browser.  
How to start:  
bash  
export PATH="/usr/local/bin:$PATH"  
cd ~/clairos/pii-demo-project  
npm run dev  
What you'll see: "Local: http://localhost:5173/" Leave it running! Don't close this window

# Step 4: Open Your Browser 🌍
Go to: http://localhost:5173/  
Now you can upload files and ask questions!


# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

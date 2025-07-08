# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)


##########################################################################################################################################################




# 🧠 Cappy AI Web App — React + Terraform + AWS

This project is a beginner-friendly example of how to build a simple web app using React and deploy it to the cloud using Terraform and AWS.

It’s designed to help non-programmers and new developers understand every part of a full-stack deployment workflow.

---

## 📁 Project Structure: `bedrock-bot`

This project has two main parts:

1. A **frontend web app** (built with React)
2. **Infrastructure setup** (using Terraform to deploy to AWS)

Below is a full breakdown of all the folders and files in this project.

```
bedrock-bot/
├── frontend/       <- The web app (user interface)
├── terraform/      <- The AWS cloud setup (infrastructure code)
├── .gitignore      <- Tells Git which files to ignore
├── README.md       <- You're reading it! Explains the project
└── .git/           <- Git's hidden folder for version tracking
```

---

## 🖥️ 1. Frontend App: `frontend/`

This folder contains the React web app — the part of the project users see and interact with in the browser.

```
frontend/
├── public/         <- Static files like HTML template
│   └── index.html  <- Main HTML template used by React
├── src/            <- The React source code
│   ├── App.js      <- The main screen (what you see on the webpage)
│   └── index.js    <- The entry point: starts the app
├── build/          <- ⚠️ Auto-created: contains final web files for deployment
├── package.json    <- Lists app dependencies & scripts
└── .gitignore      <- Tells Git to ignore folders like build/
```

### What Each Part Does:

| Folder/File        | Purpose                                                                 |
|--------------------|-------------------------------------------------------------------------|
| `public/index.html`| This is the HTML shell React will fill in with dynamic content.         |
| `src/App.js`       | This is your main web page layout — buttons, dropdowns, tabs, etc.      |
| `src/index.js`     | This file starts the app and connects it to the browser.                |
| `build/`           | This folder is **auto-generated** when you run `npm run build`. It contains the **ready-to-deploy** version of your website. |
| `package.json`     | This file lists all the tools (called "dependencies") your web app needs to run. |
| `.gitignore`       | Keeps Git from saving unnecessary or sensitive files like `node_modules` or `build/`. |

---

## ☁️ 2. AWS Infrastructure: `terraform/`

This folder contains code that **automates the setup of AWS services**, like:

- Hosting your website (using Amazon S3)
- Creating buckets to store web files

```
terraform/
├── main.tf         <- Main config: defines the AWS resources to create
└── variables.tf     <- Optional: defines reusable input values (bucket names, region, etc.)
```

### What These Files Do:

| File              | Purpose                                                                  |
|-------------------|--------------------------------------------------------------------------|
| `main.tf`         | This is the main setup file. It tells AWS: "Create a website bucket", "Upload my web files", etc. |
| `variables.tf`    | (Optional) This file lets you define values like `region = "us-east-1"` in one place for reuse. |

When you run:

```bash
terraform apply
```

Terraform reads these files, talks to AWS, and **builds your cloud infrastructure automatically**.

---

## 🔗 How Everything Connects Together

1. **You build the web app** using React (`npm run build`)
2. **The `build/` folder** is created — this has your final website files
3. **Terraform reads `build/`** and uploads those files into an **Amazon S3 bucket**
4. **You get a live website** URL like:
   ```
   http://my-bucket-name.s3-website-us-east-1.amazonaws.com
   ```

---

## 🧠 Beginner Notes

- You **only edit `src/App.js`** to change what the user sees
- You **don’t edit `build/`** — it’s generated automatically
- `main.tf` is like a recipe for AWS — you tell it what to build, and it does the work for you
- This setup uses **no servers** — it’s 100% static and hosted via **S3 (Simple Storage Service)**

---

## 🛠 Example Use Case

This project could be used to:

- Show a data dashboard for your team
- Provide download links for files
- Navigate datasets
- Create a prototype for customer-facing UIs

All **without writing any backend/server code.**

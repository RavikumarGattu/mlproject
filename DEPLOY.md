# Deploying to AWS Elastic Beanstalk via CodePipeline

This document shows the recommended, minimal steps to connect your GitHub repository to AWS CodePipeline which builds the app with CodeBuild and deploys to Elastic Beanstalk (EB).

Files included in this repo (already added):
- `Procfile` — tells EB/Gunicorn how to start the app
- `runtime.txt` — python runtime to use on EB
- `buildspec.yml` — CodeBuild spec that installs deps, runs tests, and packages `deploy.zip`
- `.ebextensions/python.config` — optional EB customizations (if present)

Quick checklist (preparations)
1. Confirm `requirements.txt` contains all runtime packages. EB/CodeBuild will install from it.
2. Ensure `app.py` exposes the WSGI `application` object (this repo does: `application = Flask(__name__)`).
3. Make sure `Procfile` contains the correct module/object: `web: gunicorn app:application --bind 0.0.0.0:$PORT --workers 3`.

High-level steps
1. Create an Elastic Beanstalk application & environment (optional now — CodePipeline can create it for you):
   - Console → Elastic Beanstalk → Create application → Platform: Python (choose version compatible with `runtime.txt`).
   - Configure an environment (Single instance for dev, Load-balanced for prod). Choose Immutable or Rolling with additional batch for safer updates.

2. Create a GitHub connection (recommended) or use OAuth access via CodePipeline:
   - AWS Console → Developer Tools → Connections → Create connection → choose GitHub and authorize.

3. Create a CodeBuild project (used by CodePipeline):
   - Console → CodeBuild → Create project
   - Source provider: CodePipeline (or GitHub for testing)
   - Environment image: Managed image, Runtime: Standard, Image: Amazon Linux 2 (or as needed), Runtime: Python 3.10
   - Buildspec: Use `buildspec.yml` from repo (CodeBuild will pick it when triggered by pipeline)
   - Artifacts: Let the pipeline manage artifacts (CodePipeline will read `deploy.zip` produced by buildspec).

4. Create CodePipeline:
   - Console → CodePipeline → Create pipeline
   - Source stage: Choose GitHub (via the connection created) and select the repo & branch (main)
   - Build stage: Choose the CodeBuild project created above
   - Deploy stage: Choose Elastic Beanstalk — select existing application & environment, or create new

5. IAM roles and permissions (console will propose roles but verify them):
   - CodePipeline service role must allow CodeBuild & EB deploy actions (AWS Console usually creates this)
   - CodeBuild role must allow S3, CloudWatch Logs, and optionally EB actions if your build interacts with EB directly
   - Elastic Beanstalk service role and EC2 instance profile must exist (console usually creates them). Ensure instance profile can read S3 (for your artifacts) and write CloudWatch logs.

6. Environment variables & secrets
   - Do NOT commit secrets to repo. Use EB Console (Configuration → Software) to set environment variables, or store secrets in AWS Systems Manager Parameter Store / Secrets Manager and have your app load them at runtime.

7. Run the pipeline
   - Start the pipeline manually or push to GitHub. Confirm that CodeBuild produces `deploy.zip` and CodePipeline deploys to EB.
   - Watch CodeBuild logs and EB events for deployment progress.

Important files explanation
- `buildspec.yml` (root) installs requirements, runs tests if present, and packages `deploy.zip` containing all application files minus typical excludes.
- `Procfile` keeps EB/Gunicorn configuration explicit and portable.
- `.ebextensions/python.config` (optional) is used for instance-level config. For AL2, you may prefer `.platform/hooks` for post-deploy scripts.

Recommended deployment strategy
- Use Immutable or Rolling with additional batch for production to minimize downtime and rollback risk.
- Use ALB + HTTPS (ACM) for secure public access.

Troubleshooting tips
- If CodeBuild fails: inspect the build logs in CloudWatch via Console → CodeBuild project → Build run → View logs.
- If EB fails to deploy: check EB Console → Events and EB logs (Logs → Full logs) for stack traces.
- If `deploy.zip` is not found: verify `artifacts` produced by `buildspec.yml` and that `deploy.zip` is included in the artifact.

Advanced automation
- For full infra-as-code: generate CloudFormation or CDK templates to create EB application/environment, CodePipeline, CodeBuild, and IAM roles. Ask me and I can generate a starter template tailored to this repo.

If you want, I can now:
- Create CloudFormation or CDK templates to fully provision the pipeline and EB resources.
- Provide sample IAM policy JSON for CodeBuild/CodePipeline roles to paste into the console.
- Walk you through the Console steps interactively.

---
Generated: automated DEPLOY.md by assistant

# &lt;PROJECT NAME&gt;

This is a base template for use with SWAT, if you are unsure what that means, you probably don't need this repository ;)

A description of the project and it's deliverables here, along with the existing site URLS.

## ☁️ Hosting

Details about where the site is hosted and any special considerations.

### Environments

| Environment                                         | Branch    | Main purpose  | Description                           |
|-----------------------------------------------------|-----------|---------------|---------------------------------------|
| [QA](http://project.tugboatqa.com/)                 | feature/X | ImageX QA     | Tugboat env, QA on PR's (optional).   |
| [DEV](http://project.prod.acquia-sites.com/)        | master    | ImageX DEV    | Contains code approved by Lead Dev.   |
| [STAGE](http://project.prod.acquia-sites.com/)      | stage     | Client UAT    | Contains code approved on DEV by QA.  |
| [PRODUCTION](http://project.prod.acquia-sites.com/) | prod      | Content entry | Code and Database/Content that will be launched

## 🔥 DEVELOPMENT

Brief explanation of development special considerations.

#### Workflow

1. Developer works on a feature branch created from master
2. Developer create a Pull Request from feature-branch -> master
3. ....
4. ...
5. ..
6. .

#### Getting Started

List out the commands needed for a developer to start this project. (i.e. clone xx, ddev init, etc)

#### Full remote sync

Run this command to sync the sanitized remote database, files, and configuration:

```shell
ddev sync
```

### 🛠 Integrations and Custom Bits

Describe anything of note that a developer might find useful.

```shell
drush my:command --isgreat
```

### 🎨 Frontend

See [FRONTEND.md](FRONTEND.md) for more information.

### ✅ Validation

#### Linters

```shell
ddev yarn lint # Run code linters.
ddev yarn lint:fix # Run code linters and automatically fix issues.
```

> **IMPORTANT:** Validation errors prevent remote pushes and cause CI/CD pipelines failures.

#### Spellcheck

```shell
ddev yarn spellcheck # Run spellcheck.
ddev yarn spellcheck:dictionary # Generate new project dictionary words.
```

> **IMPORTANT:** Generate project dictionary words only after running the spellchecker.

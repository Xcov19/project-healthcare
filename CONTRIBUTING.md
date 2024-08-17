
# Contributing to Project-Healthcare🩺 

Thank you for your interest in making a difference in healthcare through Project-Healthcare!  This guide will help you get started on your contribution journey.

## Project Setup 🚀  🚀 

### 1. Clone the Repository

Use Git to clone the Project-Healthcare repository to your local machine:


`git clone https://github.com/your-username/project-healthcare.git`

### 2. Navigate to the Project Directory

Change directories into the newly cloned project-healthcare folder:

`cd project-healthcare`

## Setting Up Your Development Environment
### - Install Dependencies:

#### Set Up the Development Environment

Run this command to use Poetry for installing all necessary tools and libraries in your virtual environment, ensuring everything works correctly with pre-commit:

`make install` 

#### Install Code Quality Tools

Use this command to set up automatic checks that will help catch errors in your code before you commit it:

`pre-commit install`
 
### - Configure Your Editor (Optional):

Set up your preferred code editor or IDE for a smooth development experience. Consider installing extensions or plugins for syntax highlighting, code completion, and debugging specific to the programming languages used in the project.

## Reporting Bugs 🐞

Before reporting a bug, please determine the type of issue you're encountering:

- Security or Vulnerability Issue: If your bug involves a security vulnerability, such as a potential breach or unauthorized access, please follow our [Security Template](https://github.com/Xcov19/project-healthcare/security/advisories/new).

- Non-Security Related Bug: For all other types of bugs, please use the [C4GT Community Template](https://github.com/Xcov19/project-healthcare/issues/new?assignees=&labels=&projects=&template=c4gt_community.yml&title=%5BC4GT+Community%5D%3A+).

Your accurate classification helps us address issues more efficiently.

### 1. Search Existing Issues  🔍:

Go through the [open issues](https://github.com/Xcov19/project-healthcare/issues) to see if the issue has already been reported.

### 2. If the Issue Isn't Reported📝:

Open a new issue on GitHub by following the most appropriate template as mentioned above. Provide clear and concise details to help the team understand and reproduce the bug.

## Submitting a Patch

#### 1. Create a Branch🌿:

Create a new branch for your bug fix or new feature. Use a descriptive branch name that reflects the change you're making. Here's an example command:

`
git checkout -b new-branch-name`

#### 2. Make Your Changes and Commit Them:

Edit the code to address the bug or implement the new feature.

**Testing Your Changes 🧪** 

To ensure your changes align with our guidelines, please follow these steps to test them:

Testing Framework: We use pytest as our test runner. This helps us ensure that the codebase remains reliable and any new changes are correctly implemented. 

Locate Test Files: You can find the test files in the [tests directory](./xcov19/tests).

Run Tests: Set up a virtual environment and run the following command. This will install all required dependencies, including those needed for testing.

`
make install
`

Navigate to the [tests directory](./xcov19/tests) and run the tests with the command 

`
pytest
`

Pytest will automatically discover and execute all the test files and functions.
View Results: After running the tests, review the output to ensure all tests pass. If there are any issues, please address them before submitting your pull request.

**Stage and commit your changes using Git✅:** 

`git add path/to/specific/file`

`git commit -m "Descriptive message about changes in that file"`

(Use descriptive commit messages that start with an action verb and clearly explain what you changed.)

#### 3. Push Your Branch🛠️:

Once all tests pass without any issues push your branch to the remote repository on GitHub, referencing the issue it addresses. Use the following command:

`
git push origin branch-name`

Additionally, include a note in your pull request (PR) indicating whether it will fix, close, or address the linked issue. Every PR should be associated with at least one issue.

#### 4. Open a Pull Request (PR)📦:

On GitHub, navigate to your repository and go to the "Pull requests" tab.

Click on "New pull request" and select your branch to create a PR.

Provide a clear and concise title and description for your PR.

Briefly explain the changes you made and address any related issues in the description.

### Proposing New Features🛠️

### 1. Open an Issue📝:

To propose new features, please use the [C4GT Community Template](https://github.com/Xcov19/project-healthcare/issues/new?assignees=&labels=&projects=&template=c4gt_community.yml&title=%5BC4GT+Community%5D%3A+). This template helps ensure that all necessary details are included and makes it easier for us to review and prioritize your suggestions.

### 2. Get Feedback and Collaborate💬:

Engage in discussions with the Project-Healthcare team on the issue.

Get feedback on your proposal and refine it based on the team's suggestions.

This collaborative process helps ensure the new feature aligns with the project's direction and technical feasibility.

## Join the Team!
We appreciate your contributions to Project-Healthcare! Your efforts help us make a positive impact on healthcare.

Thank you! ❤️ ❤️

— The Project-Healthcare Team





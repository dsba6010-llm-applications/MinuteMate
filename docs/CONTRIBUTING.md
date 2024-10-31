
### Getting started with Git

* Git is commonly described as a version control system.  It is also the core component a system for managing changes from one version to another.
* Everyone uses Git, but [nobody understands it](https://xkcd.com/1597/) due to counterintuitive terminology.  This is fine.  Follow the instructions, and after a few iterations, you'll get the hang of it.
* Watch this pretty-good [explanation](https://www.youtube.com/watch?v=ziA-JE-g8wM) of Git as used at the command line.
* But don't use the command line, use Visual Studio Code and its integrated Git functionality.  It's easier and paves over some of the complexity while you're getting started.
* Remember that you must select which branch you're on. 
* Control + Shift + P to open Git commands

### Steps to make a contribution to the project

1. **Clone or rebase** Clone the main branch of the repository to a project folder on your local drive.  This copies the entire project to a local repository on your hard drive.  If you already have the main branch cloned, rebase to the most up-to-date version of the main branch.
2. **Create new branch** From the local clone of the main branch, create a new branch for your changes.  Use a new branch for each contribution.  Name branches using snake-case.  Use short, meaningful, descriptive names related to the change you're making.
3. **Make changes** Make your desired changes to the new branch locally. If you have any local tests to run, do so regularly to catch any surprises early.
4. **Publish branch and push changes** Save and commit your changes locally, then publish your new branch to the shared repository and push committed changes.
5. **Checks and fixes** If your branch fails automated continuous integration (CI) checks, make changes until it meets the requirements.  You can make changes locally and push them to your new branch in the shared repository as many times as you need to in order to pass these checks.
6. **Pull request (PR)** Initiate a pull request from your new branch to merge the changes into the main branch.  In general, you should only initiate a PR if your branch passes all CI checks.  If you think it's okay to merge the changes despite CI checks failing, explain why.
7. **Review and merge** Prompt **someone else** on the team to review the changes made by your new branch.  If the changes make sense, the reviewer will merge the changes into the main branch and delete the new branch.
8. **Cleanup**.  Delete branches which have been merged, both on the shared remote repository and on your local drive.  Pull (rebase) the main branch so that your local repository will reflect the changes. 

TODO: Merge conflicts aren't addressed here yet

### Key Terms & Context

**.gitignore** - this file indicates what files/folders will *not* be uploaded to GitHub.

**.env and similar files** - these files contain keys and other sensitive information. They should never be published to GitHub.

**Continuous integration** - a set of practices that enables fast, safe development, even in very complex projects.  These practices emphasize integrating small, simple changes quickly, and making this practice safer through the use of fast automated code tests.  These automated tests generally consist of two main types: general, off-the-shelf tests that catch common problems like code style or security issues, and project-specific tests that look for expected functionality.

**Guidelines for CI-CD** - CI/CD, which stands for continuous integration and continuous delivery/deployment, aims to streamline and accelerate the software development lifecycle. Continuous integration (CI) refers to the practice of automatically and frequently integrating code changes into a shared source code repository. 

TODO: Expand list of terms, add FAQ
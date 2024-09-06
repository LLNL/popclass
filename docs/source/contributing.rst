============
Contributing
============

**We need your help** This section walks you through how to become a popclass developer.
We want your help. No, really. There may be a little voice inside your head that
is telling you that you're not ready to be an open source contributor; that your
skills aren't nearly good enough to contribute. What could you possibly offer a
project like this one?

We assure you - the little voice in your head is wrong. If you can write code or
documentation, you can contribute code to open source. Contributing to open
source projects is a fantastic way to advance one's coding and open source
workflow skills. Writing perfect code isn't the measure of a good developer
(that would disqualify all of us!); it's trying to create something, making
mistakes, and learning from those mistakes. That's how we all improve, and we
are happy to help others learn.

Being an open source contributor doesn't just mean writing code, either. You can
help out by writing documentation, tests, or even giving feedback about the
project (and yes - that includes giving feedback about the contribution
process). Some of these contributions may be the most valuable to the project
as a whole, because you're coming to the project with fresh eyes, so you can
see the errors and assumptions that seasoned contributors have glossed over.

.. note::
    This text was originally written by Adrienne Lowe for a PyCon talk,
    and was adapted by popclass based on its use in the README file for the MetPy
    project and `Astropy <https://www.astropy.org>`_ project.

Code of conduct
---------------

**Our Pledge** In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our
project and our community a harassment-free experience for everyone,
regardless of age, body size, disability, ethnicity, gender identity
and expression, level of experience, nationality, personal appearance,
race, religion, or sexual identity and orientation.

**Our Standards** Examples of behavior that contributes to creating a positive
environment include:

  - Using welcoming and inclusive language
  - Being respectful of differing viewpoints and experiences
  - Gracefully accepting constructive criticism
  - Focusing on what is best for the community
  - Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

  - The use of sexualized language or imagery and unwelcome sexual attention or advances
  - Trolling, insulting/derogatory comments, and personal or political attacks
  - Public or private harassment
  - Publishing others' private information, such as a physical or electronic address,
    without explicit permission
  - Other conduct which could reasonably be considered inappropriate in a professional setting

**Our Responsibilities** Project maintainers are responsible for clarifying the
standards of acceptable behavior and are expected to take appropriate and fair
corrective action in response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove,
edit, or reject comments, commits, code, wiki edits, issues,
and other contributions that are not aligned to this Code of
Conduct, or to ban temporarily or permanently any contributor
for other behaviors that they deem inappropriate, threatening,
offensive, or harmful.

**Scope** This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the popclass project or its community.
Examples of representing the project or community include using an official
project e-mail address, posting via an official social media account, or
acting as an appointed representative at an online or offline event.
Representation of the project may be further defined and clarified by
popclass maintainers.

**Enforcement** Instances of abusive, harassing, or otherwise unacceptable behavior may
be reported by contacting the LLNL GitHub Admins at github-admin@llnl.gov. The project
team will review and investigate all complaints, and will respond in a way that it
deems appropriate to the circumstances. The project team is obligated to maintain
confidentiality with regard to the reporter of an incident. Further details of
specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct
in good faith may face temporary or permanent repercussions as
determined by other members of the project or organization's leadership.

.. note::
    This Code of Conduct is adapted from the
    `Contributor Covenant <https://www.contributor-covenant.org/>`_
    `version 1.4 <http://contributor-covenant.org/version/1/4>`_ and
    the `ssapy <https://github.com/LLNL/SSAPy>`_ code of conduct.

Developer workflow
------------------

To add or change code on popclass we use Git and GitHub. The normal develop
workflow is to branch off main, commit and push changes, and then merge
into the main branch with a pull request. Finally, after the pull request
has been approved and your changes have been merged you can delete your branch.

Starting from scratch, the typical development workflow would be the following.

1. Clone the popclass Git repository

.. code:: none

    git clone https://github.com/LLNL/popclass.git

2. Create your own branch with the following naming convention.

.. code:: none

    git checkout -b -<one or two word description of what you are doing>

For example, if wanted to contribute to documentation
your branch might be called docs.

3. Set the remote of your new branch to GitHub.

.. code:: none

    git push --set-upstream origin <your branch name>

This means you can push changes to GitHub where they can be saved before you
are ready for a pull request. Now you can make your changes and additions to the
code and push changes to GitHub.

4. Next go to to the Blast GitHub repository page and go to the pull requests tab.
Then open a new draft pull request.

5. Create a pull request with your branch and main.

6. Fill in the title and describe what you are trying to do in the description, and
open a draft pull request.

7. As you commit and push changes to your branch on GitHub they will show up
in the draft pull request. On every commit some checks will be performed on
your code.

The Continuous integration test checks if any of the code you changed failed
any of the popclass tests. All checks must pass for your code changes if
you want them to be accepted!

When you are a happy for you changes to be reviewed
and then eventually merged into main, click ready for review. Your code
will now be reviewed and when it is accepted it will be merged into
main.

8. After your branch has been merged, delete the branch from your local
repository.

.. code:: none

    git branch -d <your branch name>

9. Then delete the branch from GitHub.

.. code:: none

    git push -d origin <your branch name>

To start work on a new feature, re-follow the developer workflow from step 2.

**New dependencies**

If any of your chages require new or updated package dependancies update the requirements.txt file and
Dockerfile acordinginly.

**What to work on?**

So you’ve read the developer guide, now you want to know what exactly to
work on. The best place to start is the `issues tab <https://github.com/LLNL/popclass/issues>`_
on the popclass GitHub page. Here you will find a list of tasks
that need to be worked on for popclass. If you find a bug or would
like to request a feature please open a new issue.
